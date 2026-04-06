from __future__ import annotations
"""Whiteboards resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_paginated, normalize_single, normalize_list
from ..types import PaginatedResponse, Whiteboard


# ─── Async ───────────────────────────────────────────────────────────────────


class WhiteboardsResource:
    """Async whiteboards resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Whiteboard]:
        """List whiteboards (requires read:whiteboards scope)."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if search:
            params["search"] = search

        response = await self._http.get("/whiteboards", params=params)
        return PaginatedResponse[Whiteboard](**normalize_paginated(response, 'whiteboards', Whiteboard, limit=limit, offset=(page - 1) * limit))

    async def get(self, whiteboard_id: str) -> Whiteboard:
        """Get a single whiteboard by ID (requires read:whiteboards scope)."""
        response = await self._http.get(f"/whiteboards/{whiteboard_id}")
        return normalize_single(response, 'whiteboard', Whiteboard)

    async def create(
        self,
        title: str,
        description: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        is_public: bool = False,
    ) -> Whiteboard:
        """Create a new whiteboard (requires write:whiteboards scope)."""
        data: Dict[str, Any] = {"title": title, "is_public": is_public}
        if description:
            data["description"] = description
        if content is not None:
            data["content"] = content

        response = await self._http.post("/whiteboards", json_data=data)
        return normalize_single(response, 'whiteboard', Whiteboard)

    async def update(
        self,
        whiteboard_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        is_public: Optional[bool] = None,
    ) -> Whiteboard:
        """Update a whiteboard (requires write:whiteboards scope)."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if content is not None:
            data["content"] = content
        if is_public is not None:
            data["is_public"] = is_public

        response = await self._http.put(f"/whiteboards/{whiteboard_id}", json_data=data)
        return normalize_single(response, 'whiteboard', Whiteboard)

    async def delete(self, whiteboard_id: str) -> None:
        """Delete a whiteboard (requires write:whiteboards scope)."""
        await self._http.delete(f"/whiteboards/{whiteboard_id}")


# ─── Sync ────────────────────────────────────────────────────────────────────


class SyncWhiteboardsResource:
    """Synchronous whiteboards resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Whiteboard]:
        """List whiteboards."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if search:
            params["search"] = search

        response = self._http.get("/whiteboards", params=params)
        return PaginatedResponse[Whiteboard](**normalize_paginated(response, 'whiteboards', Whiteboard, limit=limit, offset=(page - 1) * limit))

    def get(self, whiteboard_id: str) -> Whiteboard:
        """Get a single whiteboard by ID."""
        response = self._http.get(f"/whiteboards/{whiteboard_id}")
        return normalize_single(response, 'whiteboard', Whiteboard)

    def create(
        self,
        title: str,
        description: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        is_public: bool = False,
    ) -> Whiteboard:
        """Create a new whiteboard."""
        data: Dict[str, Any] = {"title": title, "is_public": is_public}
        if description:
            data["description"] = description
        if content is not None:
            data["content"] = content

        response = self._http.post("/whiteboards", json_data=data)
        return normalize_single(response, 'whiteboard', Whiteboard)

    def update(
        self,
        whiteboard_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        is_public: Optional[bool] = None,
    ) -> Whiteboard:
        """Update a whiteboard."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if content is not None:
            data["content"] = content
        if is_public is not None:
            data["is_public"] = is_public

        response = self._http.put(f"/whiteboards/{whiteboard_id}", json_data=data)
        return normalize_single(response, 'whiteboard', Whiteboard)

    def delete(self, whiteboard_id: str) -> None:
        """Delete a whiteboard."""
        self._http.delete(f"/whiteboards/{whiteboard_id}")
