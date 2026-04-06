"""Response normalization helpers for the Kairos SDK.

The Kairos microservice workers return resource-specific response shapes
(e.g. ``{"tasks": [...], "count": N, "total": N, "hasMore": bool}``) rather
than the generic ``{"data": [...], "pagination": {...}}`` envelope the SDK
exposes to callers.  These helpers bridge the gap.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar("T")


def normalize_paginated(
    raw: Dict[str, Any],
    key: str,
    model: Type[T],
    limit: int = 20,
    offset: int = 0,
) -> Dict[str, Any]:
    """Return a normalized paginated dict matching PaginatedResponse schema.

    Args:
        raw:    Raw JSON dict returned by the worker.
        key:    Resource-specific array key (e.g. "tasks", "goals").
        model:  Pydantic model class to instantiate each item.
        limit:  Requested page size (used to compute page number).
        offset: Requested offset.

    Returns a dict suitable for ``PaginatedResponse[T](**result)``.
    """
    items_raw: List[Any] = raw.get(key) or raw.get("data") or []
    items = [model(**item) for item in items_raw]

    total = int(raw.get("total") or raw.get("total_count") or raw.get("count") or 0)
    resolved_limit = int(raw.get("limit") or limit)
    resolved_offset = int(raw.get("offset") or offset)
    page = (resolved_offset // resolved_limit + 1) if resolved_limit > 0 else 1
    # Some workers (e.g. documents, whiteboards) only return total_count without
    # a hasMore/has_more field — compute it from total vs. returned items.
    explicit_has_more = raw.get("hasMore") if raw.get("hasMore") is not None else raw.get("has_more")
    if explicit_has_more is not None:
        has_more = bool(explicit_has_more)
    else:
        has_more = total > 0 and (resolved_offset + len(items)) < total

    return {
        "data": items,
        "pagination": {
            "page": page,
            "limit": resolved_limit,
            "total": total,
            "has_more": has_more,
        },
    }


def normalize_single(raw: Dict[str, Any], key: str, model: Type[T]) -> T:
    """Instantiate *model* from the resource-specific key in *raw*.

    Args:
        raw:   Raw JSON dict returned by the worker.
        key:   Resource-specific key (e.g. "task", "goal", "document").
        model: Pydantic model class to instantiate.
    """
    obj = raw.get(key) or raw.get("data")
    if obj is None:
        raise ValueError(f"Expected key '{key}' in response: {raw!r}")
    return model(**obj)


def normalize_list(raw: Any, key: str, model: Type[T]) -> List[T]:
    """Extract a plain list from a response that may be keyed or bare.

    Args:
        raw:   Raw JSON dict (or list) returned by the worker.
        key:   Resource-specific key if response is a dict.
        model: Pydantic model class to instantiate each item.
    """
    if isinstance(raw, list):
        return [model(**item) for item in raw]
    if isinstance(raw, dict):
        items = raw.get(key) or raw.get("data") or []
        return [model(**item) for item in items]
    return []
