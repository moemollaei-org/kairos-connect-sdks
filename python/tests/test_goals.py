"""Tests for the goals resource."""

import pytest
import respx
from httpx import Response

from kairos import Kairos, KairosSync
from kairos.errors import NotFoundError


@respx.mock
async def test_goals_list():
    """Test listing goals."""
    respx.get("https://gateway.thekairos.app/v1/goals").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "goal_1",
                        "team_id": "team_1",
                        "title": "Q1 2024 Goals",
                        "description": "Goals for Q1",
                        "status": "active",
                        "progress": 0.5,
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
        result = await client.goals.list()
        assert len(result.data) == 1
        assert result.data[0].id == "goal_1"
        assert result.data[0].title == "Q1 2024 Goals"
        assert result.data[0].progress == 0.5


@respx.mock
async def test_goals_get():
    """Test getting a single goal."""
    respx.get("https://gateway.thekairos.app/v1/goals/goal_1").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "goal_1",
                    "team_id": "team_1",
                    "title": "Q1 2024 Goals",
                    "status": "active",
                    "progress": 0.75,
                    "created_by": "user_1",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-15T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        goal = await client.goals.get("goal_1")
        assert goal.id == "goal_1"
        assert goal.title == "Q1 2024 Goals"
        assert goal.progress == 0.75


@respx.mock
async def test_goals_get_not_found():
    """Test getting a non-existent goal."""
    respx.get("https://gateway.thekairos.app/v1/goals/missing").mock(
        return_value=Response(
            404,
            json={
                "error": {
                    "code": "not_found",
                    "message": "Goal not found",
                    "request_id": "req_123",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        with pytest.raises(NotFoundError):
            await client.goals.get("missing")


@respx.mock
async def test_goals_create():
    """Test creating a goal."""
    respx.post("https://gateway.thekairos.app/v1/goals").mock(
        return_value=Response(
            201,
            json={
                "data": {
                    "id": "goal_new",
                    "team_id": "team_1",
                    "title": "New Goal",
                    "description": "A new goal",
                    "status": "active",
                    "progress": 0.0,
                    "created_by": "user_1",
                    "created_at": "2024-01-02T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        goal = await client.goals.create(
            title="New Goal",
            description="A new goal",
        )
        assert goal.id == "goal_new"
        assert goal.title == "New Goal"


@respx.mock
async def test_goals_update():
    """Test updating a goal."""
    respx.patch("https://gateway.thekairos.app/v1/goals/goal_1").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "goal_1",
                    "team_id": "team_1",
                    "title": "Updated Goal",
                    "status": "completed",
                    "progress": 1.0,
                    "created_by": "user_1",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        goal = await client.goals.update(
            "goal_1",
            title="Updated Goal",
            status="completed",
            progress=1.0,
        )
        assert goal.title == "Updated Goal"
        assert goal.status == "completed"
        assert goal.progress == 1.0


@respx.mock
async def test_goals_list_tasks():
    """Test listing tasks for a goal."""
    respx.get("https://gateway.thekairos.app/v1/goals/goal_1/tasks").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "task_1",
                        "team_id": "team_1",
                        "goal_id": "goal_1",
                        "title": "Task 1",
                        "status": "completed",
                        "priority": "high",
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
        result = await client.goals.list_tasks("goal_1")
        assert len(result.data) == 1
        assert result.data[0].goal_id == "goal_1"


# Synchronous tests
@respx.mock
def test_goals_list_sync():
    """Test listing goals synchronously."""
    respx.get("https://gateway.thekairos.app/v1/goals").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "goal_1",
                        "team_id": "team_1",
                        "title": "Q1 2024 Goals",
                        "status": "active",
                        "progress": 0.5,
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
        result = client.goals.list()
        assert len(result.data) == 1
        assert result.data[0].id == "goal_1"


@respx.mock
def test_goals_create_sync():
    """Test creating a goal synchronously."""
    respx.post("https://gateway.thekairos.app/v1/goals").mock(
        return_value=Response(
            201,
            json={
                "data": {
                    "id": "goal_new",
                    "team_id": "team_1",
                    "title": "New Goal",
                    "status": "active",
                    "progress": 0.0,
                    "created_by": "user_1",
                    "created_at": "2024-01-02T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        goal = client.goals.create(title="New Goal")
        assert goal.id == "goal_new"
