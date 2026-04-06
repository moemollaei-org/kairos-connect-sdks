"""Tests for the team resource."""

import respx
from httpx import Response

from kairos import Kairos, KairosSync


@respx.mock
async def test_team_get():
    """Test getting team information."""
    respx.get("https://gateway.thekairos.app/v1/team").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "team_1",
                    "name": "Engineering Team",
                    "slug": "engineering-team",
                    "description": "Main engineering team",
                    "avatar_url": "https://example.com/avatar.png",
                    "created_at": "2024-01-01T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        team = await client.team.get()
        assert team.id == "team_1"
        assert team.name == "Engineering Team"
        assert team.slug == "engineering-team"


@respx.mock
async def test_team_list_members():
    """Test listing team members."""
    respx.get("https://gateway.thekairos.app/v1/team/members").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "user_id": "user_1",
                        "email": "alice@example.com",
                        "name": "Alice",
                        "avatar_url": "https://example.com/alice.png",
                        "role": "admin",
                        "joined_at": "2024-01-01T00:00:00Z",
                    },
                    {
                        "user_id": "user_2",
                        "email": "bob@example.com",
                        "name": "Bob",
                        "avatar_url": "https://example.com/bob.png",
                        "role": "member",
                        "joined_at": "2024-01-05T00:00:00Z",
                    },
                ],
                "pagination": {"page": 1, "limit": 20, "total": 2, "has_more": False},
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        result = await client.team.list_members()
        assert len(result.data) == 2
        assert result.data[0].name == "Alice"
        assert result.data[0].role == "admin"
        assert result.data[1].name == "Bob"


# Synchronous tests
@respx.mock
def test_team_get_sync():
    """Test getting team information synchronously."""
    respx.get("https://gateway.thekairos.app/v1/team").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "team_1",
                    "name": "Engineering Team",
                    "slug": "engineering-team",
                    "description": "Main engineering team",
                    "created_at": "2024-01-01T00:00:00Z",
                }
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        team = client.team.get()
        assert team.id == "team_1"
        assert team.name == "Engineering Team"


@respx.mock
def test_team_list_members_sync():
    """Test listing team members synchronously."""
    respx.get("https://gateway.thekairos.app/v1/team/members").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "user_id": "user_1",
                        "email": "alice@example.com",
                        "name": "Alice",
                        "role": "admin",
                        "joined_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "pagination": {"page": 1, "limit": 20, "total": 1, "has_more": False},
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        result = client.team.list_members()
        assert len(result.data) == 1
        assert result.data[0].name == "Alice"
