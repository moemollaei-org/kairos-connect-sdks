"""Tests for the Kairos client."""

import os

import pytest
import respx
from httpx import Response

from kairos import Kairos, KairosSync


def test_kairos_missing_api_key():
    """Test that ValueError is raised if api_key is missing."""
    # Ensure env var is not set
    os.environ.pop("KAIROS_API_KEY", None)

    with pytest.raises(ValueError, match="api_key is required"):
        Kairos()


def test_kairos_env_var_fallback():
    """Test that KAIROS_API_KEY env var is used as fallback."""
    os.environ["KAIROS_API_KEY"] = "test_env_key"
    try:
        client = Kairos()
        assert client._api_key == "test_env_key"
        client.close()
    finally:
        os.environ.pop("KAIROS_API_KEY", None)


@respx.mock
async def test_kairos_me_endpoint():
    """Test the /me endpoint."""
    respx.get("https://gateway.thekairos.app/v1/me").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "team_id": "team_1",
                    "scopes": ["tasks:read", "tasks:write", "goals:read"],
                    "rate_limit_per_minute": 60,
                    "rate_limit_per_hour": 3600,
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        me = await client.me()
        assert me.team_id == "team_1"
        assert len(me.scopes) == 3
        assert "tasks:read" in me.scopes
        assert me.rate_limit_per_minute == 60


@respx.mock
async def test_kairos_context_manager():
    """Test using Kairos as an async context manager."""
    respx.get("https://gateway.thekairos.app/v1/me").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "team_id": "team_1",
                    "scopes": ["tasks:read"],
                    "rate_limit_per_minute": 60,
                    "rate_limit_per_hour": 3600,
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        me = await client.me()
        assert me.team_id == "team_1"


def test_kairos_sync_missing_api_key():
    """Test that ValueError is raised if api_key is missing in sync client."""
    os.environ.pop("KAIROS_API_KEY", None)

    with pytest.raises(ValueError, match="api_key is required"):
        KairosSync()


def test_kairos_sync_env_var_fallback():
    """Test that KAIROS_API_KEY env var is used as fallback in sync client."""
    os.environ["KAIROS_API_KEY"] = "test_env_key"
    try:
        client = KairosSync()
        assert client._api_key == "test_env_key"
        client.close()
    finally:
        os.environ.pop("KAIROS_API_KEY", None)


@respx.mock
def test_kairos_sync_me_endpoint():
    """Test the /me endpoint synchronously."""
    respx.get("https://gateway.thekairos.app/v1/me").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "team_id": "team_1",
                    "scopes": ["tasks:read", "tasks:write"],
                    "rate_limit_per_minute": 60,
                    "rate_limit_per_hour": 3600,
                }
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        me = client.me()
        assert me.team_id == "team_1"
        assert len(me.scopes) == 2


@respx.mock
def test_kairos_sync_context_manager():
    """Test using KairosSync as a context manager."""
    respx.get("https://gateway.thekairos.app/v1/me").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "team_id": "team_1",
                    "scopes": ["tasks:read"],
                    "rate_limit_per_minute": 60,
                    "rate_limit_per_hour": 3600,
                }
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        me = client.me()
        assert me.team_id == "team_1"


@respx.mock
async def test_kairos_api_key_precedence():
    """Test that explicit api_key takes precedence over env var."""
    os.environ["KAIROS_API_KEY"] = "env_key"
    try:
        client = Kairos(api_key="explicit_key")
        assert client._api_key == "explicit_key"
        await client.close()
    finally:
        os.environ.pop("KAIROS_API_KEY", None)


@respx.mock
async def test_kairos_custom_base_url():
    """Test using a custom base URL."""
    respx.get("https://custom.kairos.app/tasks").mock(
        return_value=Response(
            200,
            json={
                "data": [],
                "pagination": {"page": 1, "limit": 20, "total": 0, "has_more": False},
            },
        )
    )

    async with Kairos(
        api_key="test_key",
        base_url="https://custom.kairos.app",
    ) as client:
        result = await client.tasks.list()
        assert len(result.data) == 0


def test_kairos_client_initialization():
    """Test basic client initialization."""
    client = Kairos(api_key="test_key")
    assert client._api_key == "test_key"
    assert hasattr(client, "tasks")
    assert hasattr(client, "goals")
    assert hasattr(client, "team")
    assert hasattr(client, "documents")
    client.close()


def test_kairos_sync_client_initialization():
    """Test basic sync client initialization."""
    client = KairosSync(api_key="test_key")
    assert client._api_key == "test_key"
    assert hasattr(client, "tasks")
    assert hasattr(client, "goals")
    assert hasattr(client, "team")
    assert hasattr(client, "documents")
    client.close()
