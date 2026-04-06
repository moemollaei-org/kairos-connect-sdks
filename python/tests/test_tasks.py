"""Tests for the tasks resource."""

import pytest
import respx
from httpx import Response

from kairos import Kairos, KairosSync
from kairos.errors import AuthError, ForbiddenError, NotFoundError, RateLimitError


@respx.mock
async def test_tasks_list():
    """Test listing tasks."""
    respx.get("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "task_1",
                        "team_id": "team_1",
                        "title": "First task",
                        "status": "to_do",
                        "priority": "medium",
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
        result = await client.tasks.list()
        assert len(result.data) == 1
        assert result.data[0].id == "task_1"
        assert result.data[0].title == "First task"
        assert result.pagination.total == 1
        assert result.pagination.has_more is False


@respx.mock
async def test_tasks_get():
    """Test getting a single task."""
    respx.get("https://gateway.thekairos.app/v1/tasks/task_1").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "task_1",
                    "team_id": "team_1",
                    "title": "Single task",
                    "status": "in_progress",
                    "priority": "high",
                    "created_by": "user_1",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        task = await client.tasks.get("task_1")
        assert task.id == "task_1"
        assert task.title == "Single task"
        assert task.status == "in_progress"


@respx.mock
async def test_tasks_get_not_found():
    """Test getting a non-existent task."""
    respx.get("https://gateway.thekairos.app/v1/tasks/missing").mock(
        return_value=Response(
            404,
            json={
                "error": {
                    "code": "not_found",
                    "message": "Task not found",
                    "request_id": "req_123",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        with pytest.raises(NotFoundError) as exc_info:
            await client.tasks.get("missing")
        assert exc_info.value.status_code == 404


@respx.mock
async def test_tasks_create():
    """Test creating a task."""
    respx.post("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            201,
            json={
                "data": {
                    "id": "task_new",
                    "team_id": "team_1",
                    "title": "New task",
                    "description": "Task description",
                    "status": "to_do",
                    "priority": "medium",
                    "created_by": "user_1",
                    "created_at": "2024-01-02T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        task = await client.tasks.create(
            title="New task",
            description="Task description",
        )
        assert task.id == "task_new"
        assert task.title == "New task"
        assert task.description == "Task description"


@respx.mock
async def test_tasks_update():
    """Test updating a task."""
    respx.patch("https://gateway.thekairos.app/v1/tasks/task_1").mock(
        return_value=Response(
            200,
            json={
                "data": {
                    "id": "task_1",
                    "team_id": "team_1",
                    "title": "Updated task",
                    "status": "completed",
                    "priority": "low",
                    "created_by": "user_1",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        task = await client.tasks.update(
            "task_1",
            title="Updated task",
            status="completed",
            priority="low",
        )
        assert task.title == "Updated task"
        assert task.status == "completed"


@respx.mock
async def test_tasks_delete():
    """Test deleting a task."""
    respx.delete("https://gateway.thekairos.app/v1/tasks/task_1").mock(
        return_value=Response(204)
    )

    async with Kairos(api_key="test_key") as client:
        await client.tasks.delete("task_1")


@respx.mock
async def test_tasks_auth_error():
    """Test that 401 raises AuthError."""
    respx.get("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            401,
            json={
                "error": {
                    "code": "unauthorized",
                    "message": "Invalid API key",
                    "request_id": "req_123",
                }
            },
        )
    )

    async with Kairos(api_key="invalid_key") as client:
        with pytest.raises(AuthError) as exc_info:
            await client.tasks.list()
        assert exc_info.value.status_code == 401


@respx.mock
async def test_tasks_forbidden_error():
    """Test that 403 raises ForbiddenError."""
    respx.get("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            403,
            json={
                "error": {
                    "code": "forbidden",
                    "message": "No permission",
                    "request_id": "req_123",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        with pytest.raises(ForbiddenError) as exc_info:
            await client.tasks.list()
        assert exc_info.value.status_code == 403


@respx.mock
async def test_tasks_rate_limit_error():
    """Test that 429 raises RateLimitError with retry_after."""
    respx.get("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            429,
            json={
                "error": {
                    "code": "rate_limit_exceeded",
                    "message": "Rate limit exceeded",
                    "request_id": "req_123",
                }
            },
            headers={"Retry-After": "60"},
        )
    )

    async with Kairos(api_key="test_key", max_retries=0) as client:
        with pytest.raises(RateLimitError) as exc_info:
            await client.tasks.list()
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60


@respx.mock
async def test_tasks_list_comments():
    """Test listing comments on a task."""
    respx.get("https://gateway.thekairos.app/v1/tasks/task_1/comments").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "comment_1",
                        "task_id": "task_1",
                        "team_id": "team_1",
                        "content": "Great task!",
                        "created_by": "user_2",
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-01T12:00:00Z",
                    }
                ],
                "pagination": {"page": 1, "limit": 20, "total": 1, "has_more": False},
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        result = await client.tasks.list_comments("task_1")
        assert len(result.data) == 1
        assert result.data[0].content == "Great task!"


@respx.mock
async def test_tasks_add_comment():
    """Test adding a comment to a task."""
    respx.post("https://gateway.thekairos.app/v1/tasks/task_1/comments").mock(
        return_value=Response(
            201,
            json={
                "data": {
                    "id": "comment_new",
                    "task_id": "task_1",
                    "team_id": "team_1",
                    "content": "New comment",
                    "created_by": "user_1",
                    "created_at": "2024-01-02T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    async with Kairos(api_key="test_key") as client:
        comment = await client.tasks.add_comment("task_1", "New comment")
        assert comment.id == "comment_new"
        assert comment.content == "New comment"


# Synchronous tests
@respx.mock
def test_tasks_list_sync():
    """Test listing tasks synchronously."""
    respx.get("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            200,
            json={
                "data": [
                    {
                        "id": "task_1",
                        "team_id": "team_1",
                        "title": "First task",
                        "status": "to_do",
                        "priority": "medium",
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
        result = client.tasks.list()
        assert len(result.data) == 1
        assert result.data[0].id == "task_1"


@respx.mock
def test_tasks_create_sync():
    """Test creating a task synchronously."""
    respx.post("https://gateway.thekairos.app/v1/tasks").mock(
        return_value=Response(
            201,
            json={
                "data": {
                    "id": "task_new",
                    "team_id": "team_1",
                    "title": "New task",
                    "status": "to_do",
                    "priority": "medium",
                    "created_by": "user_1",
                    "created_at": "2024-01-02T00:00:00Z",
                    "updated_at": "2024-01-02T00:00:00Z",
                }
            },
        )
    )

    with KairosSync(api_key="test_key") as client:
        task = client.tasks.create(title="New task")
        assert task.id == "task_new"
