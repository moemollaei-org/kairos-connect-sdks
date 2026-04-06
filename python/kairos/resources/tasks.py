from __future__ import annotations
"""Tasks resource for Kairos SDK."""

from typing import Any, Dict, List, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types import Comment, PaginatedResponse, Task


class TasksResource:
    """Async tasks resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        goal_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
    ) -> PaginatedResponse[Task]:
        """List tasks with optional filtering.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            status: Filter by status
            goal_id: Filter by goal ID
            assigned_to: Filter by assignee user ID

        Returns:
            Paginated list of tasks
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if goal_id:
            params["goal_id"] = goal_id
        if assigned_to:
            params["assigned_to"] = assigned_to

        response = await self._http.get("/tasks", params=params)
        return PaginatedResponse[Task](
            data=[Task(**task) for task in response["data"]],
            pagination=response["pagination"],
        )

    async def get(self, task_id: str) -> Task:
        """Get a single task.

        Args:
            task_id: The task ID

        Returns:
            Task object

        Raises:
            NotFoundError: If task doesn't exist
        """
        response = await self._http.get(f"/tasks/{task_id}")
        return Task(**response["data"])

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
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title
            description: Task description
            type: Task type (task, sub_task, bug, story, epic)
            status: Task status
            priority: Task priority
            goal_id: Associated goal ID
            parent_task_id: Parent task ID (for subtasks)
            assigned_to: User ID to assign to
            estimated_hours: Estimated hours
            due_date: Due date (ISO 8601)

        Returns:
            Created task
        """
        data = {
            "title": title,
            "type": type,
            "status": status,
            "priority": priority,
        }
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

        response = await self._http.post("/tasks", json_data=data)
        return Task(**response["data"])

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
    ) -> Task:
        """Update a task.

        Args:
            task_id: The task ID
            title: New title
            description: New description
            type: New type
            status: New status
            priority: New priority
            assigned_to: New assignee
            estimated_hours: New estimated hours
            due_date: New due date

        Returns:
            Updated task

        Raises:
            NotFoundError: If task doesn't exist
        """
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

        response = await self._http.patch(f"/tasks/{task_id}", json_data=data)
        return Task(**response["data"])

    async def delete(self, task_id: str) -> None:
        """Delete a task.

        Args:
            task_id: The task ID

        Raises:
            NotFoundError: If task doesn't exist
        """
        await self._http.delete(f"/tasks/{task_id}")

    async def list_comments(
        self,
        task_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[Comment]:
        """List comments on a task.

        Args:
            task_id: The task ID
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Paginated list of comments

        Raises:
            NotFoundError: If task doesn't exist
        """
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/tasks/{task_id}/comments", params=params)
        return PaginatedResponse[Comment](
            data=[Comment(**comment) for comment in response["data"]],
            pagination=response["pagination"],
        )

    async def add_comment(self, task_id: str, content: str) -> Comment:
        """Add a comment to a task.

        Args:
            task_id: The task ID
            content: Comment content

        Returns:
            Created comment

        Raises:
            NotFoundError: If task doesn't exist
        """
        response = await self._http.post(
            f"/tasks/{task_id}/comments",
            json_data={"content": content},
        )
        return Comment(**response["data"])


class SyncTasksResource:
    """Synchronous tasks resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        goal_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
    ) -> PaginatedResponse[Task]:
        """List tasks with optional filtering.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            status: Filter by status
            goal_id: Filter by goal ID
            assigned_to: Filter by assignee user ID

        Returns:
            Paginated list of tasks
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if goal_id:
            params["goal_id"] = goal_id
        if assigned_to:
            params["assigned_to"] = assigned_to

        response = self._http.get("/tasks", params=params)
        return PaginatedResponse[Task](
            data=[Task(**task) for task in response["data"]],
            pagination=response["pagination"],
        )

    def get(self, task_id: str) -> Task:
        """Get a single task.

        Args:
            task_id: The task ID

        Returns:
            Task object

        Raises:
            NotFoundError: If task doesn't exist
        """
        response = self._http.get(f"/tasks/{task_id}")
        return Task(**response["data"])

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
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title
            description: Task description
            type: Task type (task, sub_task, bug, story, epic)
            status: Task status
            priority: Task priority
            goal_id: Associated goal ID
            parent_task_id: Parent task ID (for subtasks)
            assigned_to: User ID to assign to
            estimated_hours: Estimated hours
            due_date: Due date (ISO 8601)

        Returns:
            Created task
        """
        data = {
            "title": title,
            "type": type,
            "status": status,
            "priority": priority,
        }
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

        response = self._http.post("/tasks", json_data=data)
        return Task(**response["data"])

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
    ) -> Task:
        """Update a task.

        Args:
            task_id: The task ID
            title: New title
            description: New description
            type: New type
            status: New status
            priority: New priority
            assigned_to: New assignee
            estimated_hours: New estimated hours
            due_date: New due date

        Returns:
            Updated task

        Raises:
            NotFoundError: If task doesn't exist
        """
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

        response = self._http.patch(f"/tasks/{task_id}", json_data=data)
        return Task(**response["data"])

    def delete(self, task_id: str) -> None:
        """Delete a task.

        Args:
            task_id: The task ID

        Raises:
            NotFoundError: If task doesn't exist
        """
        self._http.delete(f"/tasks/{task_id}")

    def list_comments(
        self,
        task_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[Comment]:
        """List comments on a task.

        Args:
            task_id: The task ID
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Paginated list of comments

        Raises:
            NotFoundError: If task doesn't exist
        """
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/tasks/{task_id}/comments", params=params)
        return PaginatedResponse[Comment](
            data=[Comment(**comment) for comment in response["data"]],
            pagination=response["pagination"],
        )

    def add_comment(self, task_id: str, content: str) -> Comment:
        """Add a comment to a task.

        Args:
            task_id: The task ID
            content: Comment content

        Returns:
            Created comment

        Raises:
            NotFoundError: If task doesn't exist
        """
        response = self._http.post(
            f"/tasks/{task_id}/comments",
            json_data={"content": content},
        )
        return Comment(**response["data"])
