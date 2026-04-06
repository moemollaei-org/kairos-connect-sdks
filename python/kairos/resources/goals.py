from __future__ import annotations
"""Goals resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types import Goal, PaginatedResponse, Task


class GoalsResource:
    """Async goals resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Goal]:
        """List goals with optional filtering.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            status: Filter by status (active, completed, archived)

        Returns:
            Paginated list of goals
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status

        response = await self._http.get("/goals", params=params)
        return PaginatedResponse[Goal](
            data=[Goal(**goal) for goal in response["data"]],
            pagination=response["pagination"],
        )

    async def get(self, goal_id: str) -> Goal:
        """Get a single goal.

        Args:
            goal_id: The goal ID

        Returns:
            Goal object

        Raises:
            NotFoundError: If goal doesn't exist
        """
        response = await self._http.get(f"/goals/{goal_id}")
        return Goal(**response["data"])

    async def create(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "active",
        due_date: Optional[str] = None,
    ) -> Goal:
        """Create a new goal.

        Args:
            title: Goal title
            description: Goal description
            status: Goal status (active, completed, archived)
            due_date: Due date (ISO 8601)

        Returns:
            Created goal
        """
        data = {
            "title": title,
            "status": status,
        }
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date

        response = await self._http.post("/goals", json_data=data)
        return Goal(**response["data"])

    async def update(
        self,
        goal_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        due_date: Optional[str] = None,
    ) -> Goal:
        """Update a goal.

        Args:
            goal_id: The goal ID
            title: New title
            description: New description
            status: New status
            progress: New progress (0.0-1.0)
            due_date: New due date

        Returns:
            Updated goal

        Raises:
            NotFoundError: If goal doesn't exist
        """
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

        response = await self._http.patch(f"/goals/{goal_id}", json_data=data)
        return Goal(**response["data"])

    async def list_tasks(
        self,
        goal_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[Task]:
        """List tasks for a goal.

        Args:
            goal_id: The goal ID
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Paginated list of tasks

        Raises:
            NotFoundError: If goal doesn't exist
        """
        params = {"page": page, "limit": limit}
        response = await self._http.get(f"/goals/{goal_id}/tasks", params=params)
        return PaginatedResponse[Task](
            data=[Task(**task) for task in response["data"]],
            pagination=response["pagination"],
        )


class SyncGoalsResource:
    """Synchronous goals resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Goal]:
        """List goals with optional filtering.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            status: Filter by status (active, completed, archived)

        Returns:
            Paginated list of goals
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status

        response = self._http.get("/goals", params=params)
        return PaginatedResponse[Goal](
            data=[Goal(**goal) for goal in response["data"]],
            pagination=response["pagination"],
        )

    def get(self, goal_id: str) -> Goal:
        """Get a single goal.

        Args:
            goal_id: The goal ID

        Returns:
            Goal object

        Raises:
            NotFoundError: If goal doesn't exist
        """
        response = self._http.get(f"/goals/{goal_id}")
        return Goal(**response["data"])

    def create(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "active",
        due_date: Optional[str] = None,
    ) -> Goal:
        """Create a new goal.

        Args:
            title: Goal title
            description: Goal description
            status: Goal status (active, completed, archived)
            due_date: Due date (ISO 8601)

        Returns:
            Created goal
        """
        data = {
            "title": title,
            "status": status,
        }
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date

        response = self._http.post("/goals", json_data=data)
        return Goal(**response["data"])

    def update(
        self,
        goal_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        due_date: Optional[str] = None,
    ) -> Goal:
        """Update a goal.

        Args:
            goal_id: The goal ID
            title: New title
            description: New description
            status: New status
            progress: New progress (0.0-1.0)
            due_date: New due date

        Returns:
            Updated goal

        Raises:
            NotFoundError: If goal doesn't exist
        """
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

        response = self._http.patch(f"/goals/{goal_id}", json_data=data)
        return Goal(**response["data"])

    def list_tasks(
        self,
        goal_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[Task]:
        """List tasks for a goal.

        Args:
            goal_id: The goal ID
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Paginated list of tasks

        Raises:
            NotFoundError: If goal doesn't exist
        """
        params = {"page": page, "limit": limit}
        response = self._http.get(f"/goals/{goal_id}/tasks", params=params)
        return PaginatedResponse[Task](
            data=[Task(**task) for task in response["data"]],
            pagination=response["pagination"],
        )
