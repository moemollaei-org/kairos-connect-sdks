# Kairos SDK for Python

The official Python SDK for the Kairos API. Build task management, goal tracking, and team collaboration features into your Python applications with a simple, intuitive interface.

## Installation

### Using pip

```bash
pip install kairos-sdk
```

### Using uv

```bash
uv add kairos-sdk
```

## Authentication

The SDK uses API key authentication. Get your API key from the Kairos dashboard and pass it to the client:

```python
from kairos import Kairos

# Explicit API key
client = Kairos(api_key="kairos_sk_...")
```

Or set the `KAIROS_API_KEY` environment variable:

```python
import os
os.environ["KAIROS_API_KEY"] = "kairos_sk_..."

from kairos import Kairos

# Uses KAIROS_API_KEY automatically
client = Kairos()
```

## Quick Start

### Async Usage

```python
import asyncio
from kairos import Kairos

async def main():
    async with Kairos(api_key="kairos_sk_...") as kairos:
        # Get current user info
        me = await kairos.me()
        print(f"Team: {me.team_id}")

        # List tasks
        tasks = await kairos.tasks.list()
        print(f"Found {tasks.pagination.total} tasks")

        # Get a single task
        task = await kairos.tasks.get("task_123")
        print(f"Task: {task.title} ({task.status})")

        # Create a new task
        new_task = await kairos.tasks.create(
            title="Implement auth",
            priority="high",
            due_date="2024-12-31"
        )
        print(f"Created task: {new_task.id}")

asyncio.run(main())
```

### Synchronous Usage

Use `KairosSync` for non-async environments:

```python
from kairos import KairosSync

with KairosSync(api_key="kairos_sk_...") as kairos:
    # Get current user info
    me = kairos.me()
    print(f"Team: {me.team_id}")

    # List tasks
    tasks = kairos.tasks.list()
    print(f"Found {tasks.pagination.total} tasks")

    # Get a single task
    task = kairos.tasks.get("task_123")
    print(f"Task: {task.title}")

    # Create a new task
    new_task = kairos.tasks.create(
        title="Implement auth",
        priority="high"
    )
    print(f"Created task: {new_task.id}")
```

## API Resources

### Tasks

Manage project tasks and subtasks.

```python
# List tasks
tasks = await kairos.tasks.list(
    page=1,
    limit=20,
    status="in_progress",
    goal_id="goal_123"
)

# Get a task
task = await kairos.tasks.get("task_123")

# Create a task
task = await kairos.tasks.create(
    title="Build dashboard",
    description="Create main dashboard UI",
    type="task",
    status="to_do",
    priority="high",
    goal_id="goal_123",
    assigned_to="user_456",
    estimated_hours=8.0,
    due_date="2024-12-31"
)

# Update a task
updated = await kairos.tasks.update(
    "task_123",
    status="completed",
    priority="low"
)

# Delete a task
await kairos.tasks.delete("task_123")

# List comments on a task
comments = await kairos.tasks.list_comments("task_123", page=1, limit=10)

# Add a comment
comment = await kairos.tasks.add_comment(
    "task_123",
    content="@alice - can you review this?"
)
```

### Goals

Create and manage organizational goals.

```python
# List goals
goals = await kairos.goals.list(page=1, limit=20, status="active")

# Get a goal
goal = await kairos.goals.get("goal_123")

# Create a goal
goal = await kairos.goals.create(
    title="Launch v2.0",
    description="Major platform update",
    status="active",
    due_date="2024-06-30"
)

# Update a goal
updated = await kairos.goals.update(
    "goal_123",
    progress=0.5,
    status="completed"
)

# List tasks for a goal
tasks = await kairos.goals.list_tasks("goal_123", page=1, limit=20)
```

### Team

Access team information and member management.

```python
# Get team info
team = await kairos.team.get()
print(f"Team: {team.name}")

# List team members
members = await kairos.team.list_members(page=1, limit=20, role="admin")
for member in members.data:
    print(f"{member.name} ({member.email}) - {member.role}")
```

### Documents

Access shared team documents.

```python
# List documents
docs = await kairos.documents.list(page=1, limit=20)

# Get a document
doc = await kairos.documents.get("doc_123")
print(f"Document: {doc.title}")
print(doc.content)
```

### Current User

Get information about your API key and authentication:

```python
# Get current auth info
me = await kairos.me()
print(f"Team: {me.team_id}")
print(f"Scopes: {me.scopes}")
print(f"Rate limit: {me.rate_limit_per_minute} requests/min")
```

## Pagination

List endpoints return paginated results:

```python
result = await kairos.tasks.list()

# Access pagination info
print(f"Page: {result.pagination.page}")
print(f"Limit: {result.pagination.limit}")
print(f"Total: {result.pagination.total}")
print(f"Has more: {result.pagination.has_more}")

# Iterate through items
for task in result.data:
    print(task.title)

# Get next page
next_page = await kairos.tasks.list(page=result.pagination.page + 1)
```

## Error Handling

The SDK raises specific exceptions for different error scenarios:

```python
from kairos import (
    Kairos,
    AuthError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    KairosError,
)

async with Kairos(api_key="...") as kairos:
    try:
        task = await kairos.tasks.get("invalid_id")
    except NotFoundError as e:
        print(f"Task not found: {e.message}")
        print(f"Request ID: {e.request_id}")
    except AuthError as e:
        print(f"Authentication failed: {e.message}")
    except ForbiddenError as e:
        print(f"Permission denied: {e.message}")
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after} seconds")
    except ValidationError as e:
        print(f"Invalid request: {e.message}")
    except KairosError as e:
        print(f"API error ({e.code}): {e.message}")
        print(f"Status: {e.status_code}")
```

## Type Hints

The SDK includes complete type hints for IDE autocomplete and type checking:

```python
from kairos import Kairos
from kairos.types import Task, Goal, Comment

async with Kairos(api_key="...") as kairos:
    # Type hints help with autocomplete
    tasks: list[Task] = (await kairos.tasks.list()).data
    goal: Goal = await kairos.goals.get("goal_123")
    comment: Comment = await kairos.tasks.add_comment("task_123", "Great work!")
```

## Context Managers

Both `Kairos` and `KairosSync` support context managers for automatic cleanup:

```python
# Async context manager
async with Kairos(api_key="...") as kairos:
    tasks = await kairos.tasks.list()
# Client is automatically closed

# Sync context manager
with KairosSync(api_key="...") as kairos:
    tasks = kairos.tasks.list()
# Client is automatically closed

# Manual cleanup
client = Kairos(api_key="...")
try:
    tasks = await client.tasks.list()
finally:
    await client.close()
```

## Configuration

### Custom Base URL

For testing or private deployments:

```python
client = Kairos(
    api_key="...",
    base_url="https://custom.kairos.app/v1"
)
```

### Custom Timeout

Adjust request timeout (default 30 seconds):

```python
client = Kairos(
    api_key="...",
    timeout=60.0  # 60 second timeout
)
```

### Retry Configuration

Adjust max retries for rate limits (default 3):

```python
client = Kairos(
    api_key="...",
    max_retries=5  # Retry up to 5 times
)
```

## Data Models

### Task

```python
from kairos.types import Task

task = await kairos.tasks.get("task_123")

# Task properties
print(task.id)                # Task ID
print(task.team_id)           # Team ID
print(task.goal_id)           # Associated goal (optional)
print(task.parent_task_id)    # Parent task for subtasks (optional)
print(task.title)             # Task title
print(task.description)       # Task description (optional)
print(task.type)              # task, sub_task, bug, story, epic
print(task.status)            # to_do, in_progress, in_review, completed, cancelled
print(task.priority)          # low, medium, high, urgent
print(task.assigned_to)       # Assignee user ID (optional)
print(task.estimated_hours)   # Estimated hours (optional)
print(task.due_date)          # Due date ISO 8601 (optional)
print(task.completed_at)      # Completion timestamp (optional)
print(task.created_by)        # Creator user ID
print(task.created_at)        # Created timestamp
print(task.updated_at)        # Last updated timestamp
```

### Goal

```python
from kairos.types import Goal

goal = await kairos.goals.get("goal_123")

# Goal properties
print(goal.id)           # Goal ID
print(goal.team_id)      # Team ID
print(goal.title)        # Goal title
print(goal.description)  # Goal description (optional)
print(goal.status)       # active, completed, archived
print(goal.progress)     # Progress 0.0-1.0
print(goal.due_date)     # Due date ISO 8601 (optional)
print(goal.created_by)   # Creator user ID
print(goal.created_at)   # Created timestamp
print(goal.updated_at)   # Last updated timestamp
```

### Team

```python
from kairos.types import Team, TeamMember

team = await kairos.team.get()

# Team properties
print(team.id)           # Team ID
print(team.name)         # Team name
print(team.slug)         # Team slug
print(team.description)  # Team description (optional)
print(team.avatar_url)   # Avatar URL (optional)
print(team.created_at)   # Created timestamp

members = await kairos.team.list_members()
for member in members.data:
    print(member.user_id)     # User ID
    print(member.email)       # Email
    print(member.name)        # Name
    print(member.role)        # Role (admin, member, etc.)
    print(member.avatar_url)  # Avatar URL (optional)
    print(member.joined_at)   # Join timestamp
```

## Examples

### Create a task for a goal

```python
async with Kairos(api_key="...") as kairos:
    # Create a goal
    goal = await kairos.goals.create(
        title="Q1 2024 Roadmap",
        status="active"
    )

    # Create tasks for the goal
    for i in range(3):
        task = await kairos.tasks.create(
            title=f"Task {i+1}",
            goal_id=goal.id,
            priority="high"
        )
        print(f"Created {task.title}")
```

### Batch update tasks

```python
async with Kairos(api_key="...") as kairos:
    # List all in-progress tasks
    tasks = await kairos.tasks.list(status="in_progress")

    # Mark them as completed
    for task in tasks.data:
        await kairos.tasks.update(
            task.id,
            status="completed"
        )
        print(f"Completed {task.title}")
```

### Monitor team activity

```python
async with Kairos(api_key="...") as kairos:
    # Get team info
    team = await kairos.team.get()
    members = await kairos.team.list_members()

    # Get task stats
    tasks = await kairos.tasks.list()

    print(f"Team: {team.name}")
    print(f"Members: {len(members.data)}")
    print(f"Total tasks: {tasks.pagination.total}")
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=kairos

# Run async tests
pytest -v
```

## License

MIT License. See LICENSE file for details.

## Support

For issues, questions, or contributions, visit the GitHub repository.
