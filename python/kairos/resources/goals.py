from __future__ import annotations
"""Goals resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_paginated, normalize_single, normalize_list
from ..types import Comment, Goal, PaginatedResponse, Task


# ─── Async ───────────────────────────────────────────────────────────────────


class GoalsResource:
    """Async goals resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Goal]:
        """List goals with optional filtering."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status

        response = await self._http.get("/goals", params=params)
        return PaginatedResponse[Goal](**normalize_paginated(response, 'goals', Goal, limit=limit, offset=(page - 1) * limit))

    async def get(self, goal_id: str) -> Goal:
        """Get a single goal by ID."""
        response = await self._http.get(f"/goals/{goal_id}")
        return normalize_single(response, 'goal', Goal)

    async def create(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> Goal:
        """Create a new goal."""
        data: Dict[str, Any] = {"title": title}
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date
        if start_date:
            data["start_date"] = start_date
        if owner_id:
            data["owner_id"] = owner_id

        response = await self._http.post("/goals", json_data=data)
        return normalize_single(response, 'goal', Goal)

    async def update(
        self,
        goal_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> Goal:
        """Update a goal."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if status is not None:
            data["status"] = status
        if progress is not None:
            data["progress"] = progress
        if due_date is not None:
            data["due_date"] = due_date
        if start_date is not None:
            data["start_date"] = start_date
        if owner_id is not None:
            data["owner_id"] = owner_id

        response = await self._http.patch(f"/goals/{goal_id}", json_data=data)
        return normalize_single(response, 'goal', Goal)

    async def delete(self, goal_id: str) -> None:
        """Delete a goal (requires write:goals scope)."""
        await self._http.delete(f"/goals/{goal_id}")

    # Tasks --------------------------------------------------------------------

    async def list_tasks(
        self, goal_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Task]:
        """List tasks associated with a goal (requires read:tasks scope)."""
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/goals/{goal_id}/tasks", params=params)
        return PaginatedResponse[Task](**normalize_paginated(response, 'tasks', Task, limit=limit, offset=(page - 1) * limit))

    # Comments -----------------------------------------------------------------

    async def list_comments(
        self, goal_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a goal (requires read:comments scope)."""
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/goals/{goal_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    async def add_comment(
        self, goal_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a goal (requires write:comments scope)."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = await self._http.post(f"/goals/{goal_id}/comments", json_data=data)
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


class SyncGoalsResource:
    """Synchronous goals resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Goal]:
        """List goals with optional filtering."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status

        response = self._http.get("/goals", params=params)
        return PaginatedResponse[Goal](**normalize_paginated(response, 'goals', Goal, limit=limit, offset=(page - 1) * limit))

    def get(self, goal_id: str) -> Goal:
        """Get a single goal by ID."""
        response = self._http.get(f"/goals/{goal_id}")
        return normalize_single(response, 'goal', Goal)

    def create(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> Goal:
        """Create a new goal."""
        data: Dict[str, Any] = {"title": title}
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date
        if start_date:
            data["start_date"] = start_date
        if owner_id:
            data["owner_id"] = owner_id

        response = self._http.post("/goals", json_data=data)
        return normalize_single(response, 'goal', Goal)

    def update(
        self,
        goal_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> Goal:
        """Update a goal."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if status is not None:
            data["status"] = status
        if progress is not None:
            data["progress"] = progress
        if due_date is not None:
            data["due_date"] = due_date
        if start_date is not None:
            data["start_date"] = start_date
        if owner_id is not None:
            data["owner_id"] = owner_id

        response = self._http.patch(f"/goals/{goal_id}", json_data=data)
        return normalize_single(response, 'goal', Goal)

    def delete(self, goal_id: str) -> None:
        """Delete a goal."""
        self._http.delete(f"/goals/{goal_id}")

    # Tasks --------------------------------------------------------------------

    def list_tasks(
        self, goal_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Task]:
        """List tasks associated with a goal."""
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/goals/{goal_id}/tasks", params=params)
        return PaginatedResponse[Task](**normalize_paginated(response, 'tasks', Task, limit=limit, offset=(page - 1) * limit))

    # Comments -----------------------------------------------------------------

    def list_comments(
        self, goal_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a goal."""
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/goals/{goal_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    def add_comment(
        self, goal_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a goal."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = self._http.post(f"/goals/{goal_id}/comments", json_data=data)
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
