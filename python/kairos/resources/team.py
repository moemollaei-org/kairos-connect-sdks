"""Team resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types import PaginatedResponse, Team, TeamMember


class TeamResource:
    """Async team resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    async def get(self) -> Team:
        """Get current team information.

        Returns:
            Team object
        """
        response = await self._http.get("/team")
        return Team(**response["data"])

    async def list_members(
        self,
        page: int = 1,
        limit: int = 20,
        role: Optional[str] = None,
    ) -> PaginatedResponse[TeamMember]:
        """List team members.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            role: Filter by role

        Returns:
            Paginated list of team members
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if role:
            params["role"] = role

        response = await self._http.get("/team/members", params=params)
        return PaginatedResponse[TeamMember](
            data=[TeamMember(**member) for member in response["data"]],
            pagination=response["pagination"],
        )


class SyncTeamResource:
    """Synchronous team resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    def get(self) -> Team:
        """Get current team information.

        Returns:
            Team object
        """
        response = self._http.get("/team")
        return Team(**response["data"])

    def list_members(
        self,
        page: int = 1,
        limit: int = 20,
        role: Optional[str] = None,
    ) -> PaginatedResponse[TeamMember]:
        """List team members.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            role: Filter by role

        Returns:
            Paginated list of team members
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if role:
            params["role"] = role

        response = self._http.get("/team/members", params=params)
        return PaginatedResponse[TeamMember](
            data=[TeamMember(**member) for member in response["data"]],
            pagination=response["pagination"],
        )
