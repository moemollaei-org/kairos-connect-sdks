# Kairos SDK Structure

## Project Layout

```
kairos-sdk-python/
├── kairos/                          # Main SDK package
│   ├── __init__.py                 # Public API exports
│   ├── client.py                   # Kairos and KairosSync clients
│   ├── types.py                    # Pydantic models (Task, Goal, etc.)
│   ├── errors.py                   # Custom exception classes
│   ├── _http.py                    # AsyncHttpClient and SyncHttpClient
│   └── resources/                  # API resource modules
│       ├── __init__.py
│       ├── tasks.py                # Tasks and SyncTasks resources
│       ├── goals.py                # Goals and SyncGoals resources
│       ├── team.py                 # Team and SyncTeam resources
│       └── documents.py            # Documents and SyncDocuments resources
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_client.py             # Client initialization, auth, /me
│   ├── test_tasks.py              # Tasks resource tests
│   ├── test_goals.py              # Goals resource tests
│   ├── test_team.py               # Team resource tests
│   └── test_documents.py          # Documents resource tests
├── pyproject.toml                 # Project configuration (hatch, dependencies, pytest)
├── README.md                      # Complete user documentation
└── .gitignore                     # Git ignore rules
```

## Key Components

### 1. Client Classes
- **Kairos**: Async client with context manager support
- **KairosSync**: Synchronous wrapper for non-async environments

### 2. HTTP Client
- **AsyncHttpClient**: Handles async HTTP with retry logic for 429s
- **SyncHttpClient**: Synchronous variant using httpx.Client

### 3. Resource Classes
- **TasksResource / SyncTasksResource**: CRUD operations on tasks
- **GoalsResource / SyncGoalsResource**: CRUD operations on goals
- **TeamResource / SyncTeamResource**: Team access
- **DocumentsResource / SyncDocumentsResource**: Document access

### 4. Data Models (Pydantic v2)
- Task, Goal, Comment, Team, TeamMember, Document, MeResponse
- Pagination, PaginatedResponse, SingleResponse

### 5. Error Handling
- KairosError (base)
- AuthError (401)
- ForbiddenError (403)
- NotFoundError (404)
- ValidationError (400)
- RateLimitError (429) with retry_after
- InternalError (500+)

## API Endpoints Covered

### Tasks
- GET /tasks (list with pagination)
- GET /tasks/{id} (get single)
- POST /tasks (create)
- PATCH /tasks/{id} (update)
- DELETE /tasks/{id} (delete)
- GET /tasks/{id}/comments (list comments)
- POST /tasks/{id}/comments (add comment)

### Goals
- GET /goals (list)
- GET /goals/{id} (get single)
- POST /goals (create)
- PATCH /goals/{id} (update)
- GET /goals/{id}/tasks (list tasks for goal)

### Team
- GET /team (get team info)
- GET /team/members (list members with pagination)

### Documents
- GET /documents (list)
- GET /documents/{id} (get single)

### Auth
- GET /me (current auth info)

## Features

### Async First
- Full async/await support with AsyncHttpClient
- Context manager support for resource cleanup
- Proper async error handling

### Synchronous Support
- KairosSync provides sync wrapper for all operations
- Same API as async client, just without await
- Context manager support

### Error Handling
- Status code mapped to specific exception types
- Automatic retry on 429 (rate limit) with Retry-After header
- Request IDs included in errors for debugging

### Type Safety
- Full type hints throughout
- Pydantic v2 for data validation
- Generic types for pagination

### Pagination
- Automatic pagination metadata in responses
- Access via .pagination attribute on list responses
- Support for page and limit parameters

## Testing

### Test Coverage
- **test_client.py**: Client initialization, env vars, /me endpoint
- **test_tasks.py**: All task operations, comments, error handling
- **test_goals.py**: Goal operations
- **test_team.py**: Team access
- **test_documents.py**: Document access

### Test Tools
- pytest with pytest-asyncio
- respx for HTTP mocking
- pytest-cov for coverage reports

## Dependencies

### Runtime
- httpx >= 0.27.0 (async HTTP client)
- pydantic >= 2.0.0 (data validation)

### Development
- pytest >= 8.0.0
- pytest-asyncio >= 0.23.0
- respx >= 0.21.0 (HTTP mocking)
- pytest-cov >= 5.0.0
