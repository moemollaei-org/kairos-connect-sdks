"""Main Kairos client module."""

import os
from typing import Optional

from ._http import AsyncHttpClient, SyncHttpClient
from .resources.documents import DocumentsResource, SyncDocumentsResource
from .resources.goals import GoalsResource, SyncGoalsResource
from .resources.tasks import SyncTasksResource, TasksResource
from .resources.team import SyncTeamResource, TeamResource
from .types import MeResponse

BASE_URL = "https://gateway.thekairos.app/v1"


class Kairos:
    """Async Kairos client for the Kairos API.

    Example:
        async with Kairos() as kairos:
            tasks = await kairos.tasks.list()
            task = await kairos.tasks.get("task_123")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize the Kairos async client.

        Args:
            api_key: API key. If not provided, uses KAIROS_API_KEY env var.
            base_url: Base URL for API. Defaults to production.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Max retries for rate limits. Defaults to 3.

        Raises:
            ValueError: If api_key is not provided and KAIROS_API_KEY env var is not set.
        """
        self._api_key = api_key or os.environ.get("KAIROS_API_KEY") or ""
        if not self._api_key:
            raise ValueError(
                "api_key is required. Set KAIROS_API_KEY env var or pass api_key parameter"
            )

        self._http = AsyncHttpClient(self._api_key, base_url, timeout, max_retries)

        # Initialize resources
        self.tasks = TasksResource(self._http)
        self.goals = GoalsResource(self._http)
        self.team = TeamResource(self._http)
        self.documents = DocumentsResource(self._http)

    async def me(self) -> MeResponse:
        """Get current authenticated user/token information.

        Returns:
            Current user info with team_id, scopes, and rate limits
        """
        response = await self._http.get("/me")
        return MeResponse(**response["data"])

    async def close(self) -> None:
        """Close the HTTP client and clean up resources."""
        await self._http.close()

    async def __aenter__(self):
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager."""
        await self.close()


class KairosSync:
    """Synchronous Kairos client for the Kairos API.

    Use this for non-async environments (e.g., scripts, Django views).

    Example:
        with KairosSync() as kairos:
            tasks = kairos.tasks.list()
            task = kairos.tasks.get("task_123")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize the Kairos synchronous client.

        Args:
            api_key: API key. If not provided, uses KAIROS_API_KEY env var.
            base_url: Base URL for API. Defaults to production.
            timeout: Request timeout in seconds. Defaults to 30.
            max_retries: Max retries for rate limits. Defaults to 3.

        Raises:
            ValueError: If api_key is not provided and KAIROS_API_KEY env var is not set.
        """
        self._api_key = api_key or os.environ.get("KAIROS_API_KEY") or ""
        if not self._api_key:
            raise ValueError(
                "api_key is required. Set KAIROS_API_KEY env var or pass api_key parameter"
            )

        self._http = SyncHttpClient(self._api_key, base_url, timeout, max_retries)

        # Initialize resources
        self.tasks = SyncTasksResource(self._http)
        self.goals = SyncGoalsResource(self._http)
        self.team = SyncTeamResource(self._http)
        self.documents = SyncDocumentsResource(self._http)

    def me(self) -> MeResponse:
        """Get current authenticated user/token information.

        Returns:
            Current user info with team_id, scopes, and rate limits
        """
        response = self._http.get("/me")
        return MeResponse(**response["data"])

    def close(self) -> None:
        """Close the HTTP client and clean up resources."""
        self._http.close()

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.close()
