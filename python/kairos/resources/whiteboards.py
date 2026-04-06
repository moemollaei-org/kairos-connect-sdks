from __future__ import annotations
"""Whiteboards resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_paginated, normalize_single, normalize_list
from ..types import Comment, PaginatedResponse, Whiteboard


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

        response = await self._http.patch(f"/whiteboards/{whiteboard_id}", json_data=data)
        return normalize_single(response, 'whiteboard', Whiteboard)

    async def delete(self, whiteboard_id: str) -> None:
        """Delete a whiteboard (requires write:whiteboards scope)."""
        await self._http.delete(f"/whiteboards/{whiteboard_id}")

    # Comments -----------------------------------------------------------------

    async def list_comments(
        self, whiteboard_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a whiteboard (requires read:comments scope)."""
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/whiteboards/{whiteboard_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    async def add_comment(
        self, whiteboard_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a whiteboard (requires write:comments scope)."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = await self._http.post(f"/whiteboards/{whiteboard_id}/comments", json_data=data)
        return normalize_single(response, 'comment', Comment)

    async def update_comment(self, comment_id: str, content: str) -> Comment:
        """Update a comment (requires write:comments scope)."""
        response = await self._http.patch(
            f"/comments/{comment_id}", json_data={"content": content}
        )
        return normalize_single(response, 'comment', Comment)

    async def delete_comment(self, comment_id: str) -> None:
        """Delete a comment (requires write:comments scope)."""
        await self._http.delete(f"/comments/{comment_id}")


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

        response = self._http.patch(f"/whiteboards/{whiteboard_id}", json_data=data)
        return normalize_single(response, 'whiteboard', Whiteboard)

    def delete(self, whiteboard_id: str) -> None:
        """Delete a whiteboard."""
        self._http.delete(f"/whiteboards/{whiteboard_id}")

    # Comments -----------------------------------------------------------------

    def list_comments(
        self, whiteboard_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a whiteboard."""
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/whiteboards/{whiteboard_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    def add_comment(
        self, whiteboard_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a whiteboard."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = self._http.post(f"/whiteboards/{whiteboard_id}/comments", json_data=data)
        return normalize_single(response, 'comment', Comment)

    def update_comment(self, comment_id: str, content: str) -> Comment:
        """Update a comment."""
        response = self._http.patch(
            f"/comments/{comment_id}", json_data={"content": content}
        )
        return normalize_single(response, 'comment', Comment)

    def delete_comment(self, comment_id: str) -> None:
        """Delete a comment."""
        self._http.delete(f"/comments/{comment_id}")
