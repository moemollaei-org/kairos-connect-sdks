from __future__ import annotations
"""Documents resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_paginated, normalize_single, normalize_list
from ..types import Comment, Document, PaginatedResponse


# ─── Async ───────────────────────────────────────────────────────────────────


class DocumentsResource:
    """Async documents resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        teamspace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Document]:
        """List documents with optional filtering (requires read:documents scope)."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if teamspace_id:
            params["teamspace_id"] = teamspace_id
        if parent_id:
            params["parent_id"] = parent_id
        if type:
            params["type"] = type
        if search:
            params["search"] = search

        response = await self._http.get("/documents", params=params)
        return PaginatedResponse[Document](**normalize_paginated(response, 'documents', Document, limit=limit, offset=(page - 1) * limit))

    async def get(self, document_id: str) -> Document:
        """Get a single document by ID (requires read:documents scope)."""
        response = await self._http.get(f"/documents/{document_id}")
        return normalize_single(response, 'document', Document)

    async def create(
        self,
        title: str,
        content: Optional[Dict[str, Any]] = None,
        teamspace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        type: str = "document",
        icon: Optional[str] = None,
    ) -> Document:
        """Create a new document (requires write:documents scope)."""
        data: Dict[str, Any] = {"title": title, "type": type}
        if content is not None:
            data["content"] = content
        if teamspace_id:
            data["teamspace_id"] = teamspace_id
        if parent_id:
            data["parent_id"] = parent_id
        if icon:
            data["icon"] = icon

        response = await self._http.post("/documents", json_data=data)
        return normalize_single(response, 'document', Document)

    async def update(
        self,
        document_id: str,
        title: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        icon: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> Document:
        """Update a document (requires write:documents scope)."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if icon is not None:
            data["icon"] = icon
        if parent_id is not None:
            data["parent_id"] = parent_id

        response = await self._http.put(f"/documents/{document_id}", json_data=data)
        return normalize_single(response, 'document', Document)

    async def delete(self, document_id: str) -> None:
        """Delete a document (requires write:documents scope)."""
        await self._http.delete(f"/documents/{document_id}")

    # Comments -----------------------------------------------------------------

    async def list_comments(
        self, document_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a document (requires read:comments scope)."""
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/documents/{document_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    async def add_comment(
        self, document_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a document (requires write:comments scope)."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = await self._http.post(f"/documents/{document_id}/comments", json_data=data)
        return normalize_single(response, 'comment', Comment)

    async def update_comment(self, comment_id: str, content: str) -> Comment:
        """Update a comment (requires write:comments scope)."""
        response = await self._http.put(
            f"/comments/{comment_id}", json_data={"content": content}
        )
        return normalize_single(response, 'comment', Comment)

    async def delete_comment(self, comment_id: str) -> None:
        """Delete a comment (requires write:comments scope)."""
        await self._http.delete(f"/comments/{comment_id}")


# ─── Sync ────────────────────────────────────────────────────────────────────


class SyncDocumentsResource:
    """Synchronous documents resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        teamspace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Document]:
        """List documents with optional filtering."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if teamspace_id:
            params["teamspace_id"] = teamspace_id
        if parent_id:
            params["parent_id"] = parent_id
        if type:
            params["type"] = type
        if search:
            params["search"] = search

        response = self._http.get("/documents", params=params)
        return PaginatedResponse[Document](**normalize_paginated(response, 'documents', Document, limit=limit, offset=(page - 1) * limit))

    def get(self, document_id: str) -> Document:
        """Get a single document by ID."""
        response = self._http.get(f"/documents/{document_id}")
        return normalize_single(response, 'document', Document)

    def create(
        self,
        title: str,
        content: Optional[Dict[str, Any]] = None,
        teamspace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        type: str = "document",
        icon: Optional[str] = None,
    ) -> Document:
        """Create a new document."""
        data: Dict[str, Any] = {"title": title, "type": type}
        if content is not None:
            data["content"] = content
        if teamspace_id:
            data["teamspace_id"] = teamspace_id
        if parent_id:
            data["parent_id"] = parent_id
        if icon:
            data["icon"] = icon

        response = self._http.post("/documents", json_data=data)
        return normalize_single(response, 'document', Document)

    def update(
        self,
        document_id: str,
        title: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        icon: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> Document:
        """Update a document."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if icon is not None:
            data["icon"] = icon
        if parent_id is not None:
            data["parent_id"] = parent_id

        response = self._http.put(f"/documents/{document_id}", json_data=data)
        return normalize_single(response, 'document', Document)

    def delete(self, document_id: str) -> None:
        """Delete a document."""
        self._http.delete(f"/documents/{document_id}")

    # Comments -----------------------------------------------------------------

    def list_comments(
        self, document_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a document."""
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/documents/{document_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    def add_comment(
        self, document_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a document."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = self._http.post(f"/documents/{document_id}/comments", json_data=data)
        return normalize_single(response, 'comment', Comment)

    def update_comment(self, comment_id: str, content: str) -> Comment:
        """Update a comment."""
        response = self._http.put(
            f"/comments/{comment_id}", json_data={"content": content}
        )
        return normalize_single(response, 'comment', Comment)

    def delete_comment(self, comment_id: str) -> None:
        """Delete a comment."""
        self._http.delete(f"/comments/{comment_id}")
