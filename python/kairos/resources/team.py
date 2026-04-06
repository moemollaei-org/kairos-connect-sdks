from __future__ import annotations
"""Team resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from .._normalize import normalize_list, normalize_single
from ..types import PaginatedResponse, Team, TeamMember


class TeamResource:
    """Async team resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    async def get(self) -> Team:
        """Get the current API key's team.

        Worker returns { teams: [...] } — returns the first team.
        """
        response = await self._http.get("/teams")
        teams = normalize_list(response, "teams", Team)
        if not teams:
            raise ValueError("No team found for this API key")
        return teams[0]

    async def list_members(
        self,
        team_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> PaginatedResponse[TeamMember]:
        """List members of a team.

        Args:
            team_id: Team UUID
            limit: Items per page
            offset: Pagination offset

        Returns:
            Paginated list of team members
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        # Worker returns { members: [...] }
        response = await self._http.get(f"/teams/{team_id}/members", params=params)
        members = normalize_list(response, "members", TeamMember)
        return PaginatedResponse[TeamMember](
            data=members,
            pagination={"page": 1, "limit": limit, "total": len(members), "has_more": False},
        )


class SyncTeamResource:
    """Synchronous team resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    def get(self) -> Team:
        """Get the current API key's team.

        Worker returns { teams: [...] } — returns the first team.
        """
        response = self._http.get("/teams")
        teams = normalize_list(response, "teams", Team)
        if not teams:
            raise ValueError("No team found for this API key")
        return teams[0]

    def list_members(
        self,
        team_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> PaginatedResponse[TeamMember]:
        """List members of a team.

        Args:
            team_id: Team UUID
            limit: Items per page
            offset: Pagination offset

        Returns:
            Paginated list of team members
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = self._http.get(f"/teams/{team_id}/members", params=params)
        members = normalize_list(response, "members", TeamMember)
        return PaginatedResponse[TeamMember](
            data=members,
            pagination={"page": 1, "limit": limit, "total": len(members), "has_more": False},
        )
