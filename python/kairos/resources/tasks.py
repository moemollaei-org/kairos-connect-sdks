from __future__ import annotations
"""Tasks resource for Kairos SDK."""

from typing import Any, Dict, List, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_paginated, normalize_single, normalize_list
from ..types import Comment, PaginatedResponse, Task, TaskLabel


# ─── Async ───────────────────────────────────────────────────────────────────


class TasksResource:
    """Async tasks resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        goal_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Task]:
        """List tasks with optional filtering."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if goal_id:
            params["goal_id"] = goal_id
        if parent_task_id:
            params["parent_task_id"] = parent_task_id
        if assigned_to:
            params["assigned_to"] = assigned_to
        if type:
            params["type"] = type
        if search:
            params["search"] = search

        response = await self._http.get("/tasks", params=params)
        return PaginatedResponse[Task](**normalize_paginated(response, 'tasks', Task, limit=limit, offset=(page - 1) * limit))

    async def get(self, task_id: str) -> Task:
        """Get a single task by ID."""
        response = await self._http.get(f"/tasks/{task_id}")
        return normalize_single(response, 'task', Task)

    async def create(
        self,
        title: str,
        description: Optional[str] = None,
        type: str = "task",
        status: str = "to_do",
        priority: str = "medium",
        goal_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
    ) -> Task:
        """Create a new task."""
        data: Dict[str, Any] = {"title": title, "type": type, "status": status, "priority": priority}
        if description:
            data["description"] = description
        if goal_id:
            data["goal_id"] = goal_id
        if parent_task_id:
            data["parent_task_id"] = parent_task_id
        if assigned_to:
            data["assigned_to"] = assigned_to
        if estimated_hours is not None:
            data["estimated_hours"] = estimated_hours
        if due_date:
            data["due_date"] = due_date
        if start_date:
            data["start_date"] = start_date

        response = await self._http.post("/tasks", json_data=data)
        return normalize_single(response, 'task', Task)

    async def update(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
    ) -> Task:
        """Update a task."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if type is not None:
            data["type"] = type
        if status is not None:
            data["status"] = status
        if priority is not None:
            data["priority"] = priority
        if assigned_to is not None:
            data["assigned_to"] = assigned_to
        if estimated_hours is not None:
            data["estimated_hours"] = estimated_hours
        if due_date is not None:
            data["due_date"] = due_date
        if start_date is not None:
            data["start_date"] = start_date

        response = await self._http.put(f"/tasks/{task_id}", json_data=data)
        return normalize_single(response, 'task', Task)

    async def delete(self, task_id: str) -> None:
        """Delete a task."""
        await self._http.delete(f"/tasks/{task_id}")

    # Labels -------------------------------------------------------------------

    async def list_labels(self, task_id: str) -> List[TaskLabel]:
        """List all labels on a task (requires read:tasks scope)."""
        response = await self._http.get(f"/tasks/{task_id}/labels")
        return normalize_list(response, 'labels', TaskLabel)

    async def add_label(self, task_id: str, label_id: str) -> TaskLabel:
        """Add a label to a task (requires write:tasks scope)."""
        response = await self._http.post(
            f"/tasks/{task_id}/labels/{label_id}",
        )
        return normalize_single(response, 'label', TaskLabel)

    async def remove_label(self, task_id: str, label_id: str) -> None:
        """Remove a label from a task (requires write:tasks scope)."""
        await self._http.delete(f"/tasks/{task_id}/labels/{label_id}")

    # Comments -----------------------------------------------------------------

    async def list_comments(
        self, task_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a task (requires read:comments scope)."""
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/tasks/{task_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    async def add_comment(
        self, task_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a task (requires write:comments scope)."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = await self._http.post(f"/tasks/{task_id}/comments", json_data=data)
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


class SyncTasksResource:
    """Synchronous tasks resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    # Core CRUD ----------------------------------------------------------------

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        goal_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Task]:
        """List tasks with optional filtering."""
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if goal_id:
            params["goal_id"] = goal_id
        if parent_task_id:
            params["parent_task_id"] = parent_task_id
        if assigned_to:
            params["assigned_to"] = assigned_to
        if type:
            params["type"] = type
        if search:
            params["search"] = search

        response = self._http.get("/tasks", params=params)
        return PaginatedResponse[Task](**normalize_paginated(response, 'tasks', Task, limit=limit, offset=(page - 1) * limit))

    def get(self, task_id: str) -> Task:
        """Get a single task by ID."""
        response = self._http.get(f"/tasks/{task_id}")
        return normalize_single(response, 'task', Task)

    def create(
        self,
        title: str,
        description: Optional[str] = None,
        type: str = "task",
        status: str = "to_do",
        priority: str = "medium",
        goal_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
    ) -> Task:
        """Create a new task."""
        data: Dict[str, Any] = {"title": title, "type": type, "status": status, "priority": priority}
        if description:
            data["description"] = description
        if goal_id:
            data["goal_id"] = goal_id
        if parent_task_id:
            data["parent_task_id"] = parent_task_id
        if assigned_to:
            data["assigned_to"] = assigned_to
        if estimated_hours is not None:
            data["estimated_hours"] = estimated_hours
        if due_date:
            data["due_date"] = due_date
        if start_date:
            data["start_date"] = start_date

        response = self._http.post("/tasks", json_data=data)
        return normalize_single(response, 'task', Task)

    def update(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
    ) -> Task:
        """Update a task."""
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if type is not None:
            data["type"] = type
        if status is not None:
            data["status"] = status
        if priority is not None:
            data["priority"] = priority
        if assigned_to is not None:
            data["assigned_to"] = assigned_to
        if estimated_hours is not None:
            data["estimated_hours"] = estimated_hours
        if due_date is not None:
            data["due_date"] = due_date
        if start_date is not None:
            data["start_date"] = start_date

        response = self._http.put(f"/tasks/{task_id}", json_data=data)
        return normalize_single(response, 'task', Task)

    def delete(self, task_id: str) -> None:
        """Delete a task."""
        self._http.delete(f"/tasks/{task_id}")

    # Labels -------------------------------------------------------------------

    def list_labels(self, task_id: str) -> List[TaskLabel]:
        """List all labels on a task."""
        response = self._http.get(f"/tasks/{task_id}/labels")
        return normalize_list(response, 'labels', TaskLabel)

    def add_label(self, task_id: str, label_id: str) -> TaskLabel:
        """Add a label to a task."""
        response = self._http.post(
            f"/tasks/{task_id}/labels/{label_id}",
        )
        return normalize_single(response, 'label', TaskLabel)

    def remove_label(self, task_id: str, label_id: str) -> None:
        """Remove a label from a task."""
        self._http.delete(f"/tasks/{task_id}/labels/{label_id}")

    # Comments -----------------------------------------------------------------

    def list_comments(
        self, task_id: str, page: int = 1, limit: int = 20
    ) -> PaginatedResponse[Comment]:
        """List comments on a task."""
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/tasks/{task_id}/comments", params=params)
        return PaginatedResponse[Comment](**normalize_paginated(response, 'comments', Comment, limit=limit, offset=(page - 1) * limit))

    def add_comment(
        self, task_id: str, content: str, parent_comment_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to a task."""
        data: Dict[str, Any] = {"content": content}
        if parent_comment_id:
            data["parent_comment_id"] = parent_comment_id
        response = self._http.post(f"/tasks/{task_id}/comments", json_data=data)
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
