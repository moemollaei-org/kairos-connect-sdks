"""Tests for the documents resource."""

import respx
from httpx import Response

from kairos import Kairos, KairosSync
from kairos.errors import NotFoundError
import pytest


@respx.mock
async def test_documents_list():
    """Test listing documents."""
    respx.get("https://gateway.thekairos.app/v1/documents").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "doc_1",
                        "team_id": "team_1",
                        "title": "Engineering Guidelines",
                        "content": "# Guidelines",
                        "created_by": "user_1",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "pagination": {"page": 1, "limit": 20, "total": 1, "has_more": False},
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        result = await client.documents.list()
        assert len(result.data) == 1
        assert result.data[0].id == "doc_1"
        assert result.data[0].title == "Engineering Guidelines"


@respx.mock
async def test_documents_get():
    """Test getting a single document."""
    respx.get("https://gateway.thekairos.app/v1/documents/doc_1").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "doc_1",
                    "team_id": "team_1",
                    "title": "Engineering Guidelines",
                    "content": "# Guidelines\n\nFollow these standards...",
                    "created_by": "user_1",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-15T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        doc = await client.documents.get("doc_1")
        assert doc.id == "doc_1"
        assert doc.title == "Engineering Guidelines"
        assert "Guidelines" in doc.content


@respx.mock
async def test_documents_get_not_found():
    """Test getting a non-existent document."""
    respx.get("https://gateway.thekairos.app/v1/documents/missing").mock(
        return_value=Response(
            404,
            json={
                "error": {
                    "code": "not_found",
                    "message": "Document not found",
                    "request_id": "req_123",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        with pytest.raises(NotFoundError):
            await client.documents.get("missing")


# Synchronous tests
@respx.mock
def test_documents_list_sync():
    """Test listing documents synchronously."""
    respx.get("https://gateway.thekairos.app/v1/documents").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "doc_1",
                        "team_id": "team_1",
                        "title": "Engineering Guidelines",
                        "content": "# Guidelines",
                        "created_by": "user_1",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "pagination": {"page": 1, "limit": 20, "total": 1, "has_more": False},
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        result = client.documents.list()
        assert len(result.data) == 1
        assert result.data[0].id == "doc_1"


@respx.mock
def test_documents_get_sync():
    """Test getting a document synchronously."""
    respx.get("https://gateway.thekairos.app/v1/documents/doc_1").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "doc_1",
                    "team_id": "team_1",
                    "title": "Engineering Guidelines",
                    "content": "# Guidelines",
                    "created_by": "user_1",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        doc = client.documents.get("doc_1")
        assert doc.id == "doc_1"
