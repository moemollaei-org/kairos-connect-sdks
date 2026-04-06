"""Documents resource for Kairos SDK."""

from typing import Any, Dict, Optional

from .._http import AsyncHttpClient, SyncHttpClient
from ..types import Document, PaginatedResponse


class DocumentsResource:
    """Async documents resource."""

    def __init__(self, http_client: AsyncHttpClient):
        self._http = http_client

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[Document]:
        """List documents.

        Args:
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Paginated list of documents
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        response = await self._http.get("/documents", params=params)
        return PaginatedResponse[Document](
            data=[Document(**doc) for doc in response["data"]],
            pagination=response["pagination"],
        )

    async def get(self, document_id: str) -> Document:
        """Get a single document.

        Args:
            document_id: The document ID

        Returns:
            Document object

        Raises:
            NotFoundError: If document doesn't exist
        """
        response = await self._http.get(f"/documents/{document_id}")
        return Document(**response["data"])


class SyncDocumentsResource:
    """Synchronous documents resource."""

    def __init__(self, http_client: SyncHttpClient):
        self._http = http_client

    def list(
        self,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedResponse[Document]:
        """List documents.

        Args:
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Paginated list of documents
        """
        params: Dict[str, Any] = {"page": page, "limit": limit}
        response = self._http.get("/documents", params=params)
        return PaginatedResponse[Document](
            data=[Document(**doc) for doc in response["data"]],
            pagination=response["pagination"],
        )

    def get(self, document_id: str) -> Document:
        """Get a single document.

        Args:
            document_id: The document ID

        Returns:
            Document object

        Raises:
            NotFoundError: If document doesn't exist
        """
        response = self._http.get(f"/documents/{document_id}")
        return Document(**response["data"])
