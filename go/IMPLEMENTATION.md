# Kairos Go SDK - Implementation Details

## Architecture Overview

The Kairos Go SDK is a lightweight, idiomatic Go client for the Kairos API with zero external dependencies. It follows Go best practices and conventions.

## Project Structure

```
kairos-sdk-go/
├── go.mod                 # Module definition (Go 1.21+, no external dependencies)
├── kairos.go              # Main client and initialization
├── types.go               # All struct definitions
├── errors.go              # Error handling and type checking
├── http.go                # HTTP transport and request/response handling
├── tasks.go               # Task service implementation
├── goals.go               # Goal service implementation
├── team.go                # Team service implementation
├── documents.go           # Documents service implementation
├── tasks_test.go          # Task service tests
├── goals_test.go          # Goal service tests
├── team_test.go           # Team service tests
├── documents_test.go      # Documents service tests
├── kairos_test.go         # Client initialization and Me() tests
├── README.md              # User-facing documentation
└── IMPLEMENTATION.md      # This file
```

## Core Components

### 1. Client (`kairos.go`)

The `Client` struct is the main entry point for the SDK. It:
- Holds API key and configuration
- Manages HTTP client
- Exposes service clients (Tasks, Goals, Team, Documents)
- Provides convenience methods like `Me()`

Key features:
- Thread-safe for concurrent use
- Configurable via options pattern
- Supports environment variable `KAIROS_API_KEY`
- Default timeout of 30 seconds
- Configurable retry logic (default 3 retries)

### 2. HTTP Transport (`http.go`)

Implements the HTTP layer with:
- Request marshaling/unmarshaling
- Authorization header injection
- Retry logic for 429 responses with exponential backoff
- Rate limit header parsing
- Query parameter encoding
- Error response handling

Methods:
- `do()` - Core request execution
- `get()`, `post()`, `patch()`, `delete()` - HTTP verb helpers
- `encodeQueryParams()` - Converts structs to URL query parameters
- `parseRateLimit()` - Extracts rate limit info from headers
- `parseRetryAfter()` - Handles retry timing

### 3. Error Handling (`errors.go`)

- `KairosError` struct wraps API errors with status codes and request IDs
- Helper functions: `IsAuthError()`, `IsForbiddenError()`, `IsNotFoundError()`, `IsRateLimitError()`
- Proper error formatting for debugging

### 4. Type Definitions (`types.go`)

All data models with JSON tags:
- `Task` - Task with all fields including timestamps
- `Goal` - Goal object
- `Comment` - Task comment
- `Team` - Team metadata
- `TeamMember` - Team member with role
- `Document` - Document with content
- `Pagination` - Pagination info (page, limit, total, has_more)
- `ListOptions`, `ListTasksOptions` - Query parameter objects
- `RateLimit` - Rate limit info from headers
- `MeResponse` - Auth validation response

All pointer fields for optional API values use `*string`, `*time.Time`, etc.

### 5. Service Implementations

#### TasksService (`tasks.go`)
- `List(ctx, opts)` - Get paginated list with filters
- `Get(ctx, id)` - Get single task
- `Create(ctx, input)` - Create new task
- `Update(ctx, id, input)` - Update task fields
- `Delete(ctx, id)` - Delete task
- `ListComments(ctx, taskID, opts)` - Get task comments
- `AddComment(ctx, taskID, content)` - Add comment to task

#### GoalsService (`goals.go`)
- `List(ctx, opts)` - Get paginated list
- `Get(ctx, id)` - Get single goal
- `Create(ctx, input)` - Create new goal
- `Update(ctx, id, input)` - Update goal
- `ListTasks(ctx, goalID, opts)` - Get tasks for goal

#### TeamService (`team.go`)
- `Get(ctx)` - Get team info
- `ListMembers(ctx, opts)` - Get paginated member list

#### DocumentsService (`documents.go`)
- `List(ctx, opts)` - Get paginated document list
- `Get(ctx, id)` - Get single document

## Design Principles

### 1. Idiomatic Go
- Uses standard library only (no external dependencies)
- Follows Go naming conventions and style
- Error handling via `(result, error)` pattern
- Context-first method signatures

### 2. Zero Dependencies
- Only uses Go standard library:
  - `net/http` - HTTP client
  - `encoding/json` - JSON marshaling
  - `context` - Request lifecycle
  - `time` - Timeouts and timestamps
  - `net/url` - Query parameters
  - `fmt` - Error messages
  - `os` - Environment variables
  - `io` - Request/response I/O
  - `bytes` - Buffer handling
  - `strconv` - String conversion

### 3. Thread-Safe
- `Client` instance can be shared across goroutines
- No global state
- `http.Client` is thread-safe

### 4. Retry Logic
- Automatic retry on 429 (Too Many Requests)
- Respects `Retry-After` header
- Configurable max retries (default 3)
- Maintains request body for retries

### 5. Context Support
- All API methods accept `context.Context`
- Enables timeouts, deadlines, cancellation
- Properly propagates context errors

## Testing Strategy

All test files use `net/http/httptest` for HTTP mocking:

- **tasks_test.go**: 9 tests covering CRUD, comments, auth, rate limiting
- **goals_test.go**: 4 tests covering goal operations
- **team_test.go**: 2 tests for team and members
- **documents_test.go**: 2 tests for document operations
- **kairos_test.go**: 5 tests for client initialization and Me()

Total: 22 comprehensive tests with no external dependencies

Tests verify:
- Successful operations
- Pagination handling
- Error responses (404, 401, 429)
- Rate limit retry behavior
- Request header injection
- Response marshaling

## API Response Format

All responses follow the standard envelope format:

### Single resource:
```json
{
  "data": { /* resource */ }
}
```

### List resources:
```json
{
  "data": [ /* array */ ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "has_more": true
  }
}
```

### Errors:
```json
{
  "error": {
    "code": "not_found",
    "message": "Resource not found",
    "request_id": "req-123"
  }
}
```

## Configuration Options

The `ClientOption` pattern enables flexible configuration:

```go
client, err := kairos.New(apiKey,
    kairos.WithBaseURL(url),
    kairos.WithHTTPClient(httpClient),
    kairos.WithMaxRetries(5),
    kairos.WithTimeout(60*time.Second),
)
```

Each option is a function that modifies the client before initialization.

## Rate Limiting

The SDK extracts rate limit info from response headers:
- `X-RateLimit-Limit-Minute`
- `X-RateLimit-Remaining-Minute`
- `X-RateLimit-Limit-Hour`
- `X-RateLimit-Remaining-Hour`
- `X-RateLimit-Reset`

Rate limit info is available in `*RateLimit` returned by transport methods.

## Query Parameters

Query parameters are handled with a custom struct-to-URL conversion that:
- Only includes non-empty fields
- Uses proper URL encoding
- Supports both `ListOptions` and `ListTasksOptions`

## Authentication

- Bearer token authentication: `Authorization: Bearer kairos_sk_...`
- API key from argument or `KAIROS_API_KEY` env var
- Validated by `Me()` endpoint

## Backward Compatibility

The SDK is designed for easy versioning:
- Version constant in `kairos.go`
- User-Agent header includes version
- No breaking changes expected in minor versions
- Struct tags use `omitempty` for forward compatibility

## Performance Considerations

- Single HTTP client with configurable timeout
- Connection pooling via standard library
- Minimal memory allocations
- No goroutine spawning for normal operations
- Automatic compression (standard library)

## Error Recovery

- Automatic retry on 429 with backoff
- Proper error type checking via `IsAuthError()` etc
- Full error information (code, message, request ID, status)
- Context cancellation respected

## Future Enhancements

Possible additions without breaking changes:
- Webhook client
- Batch operations
- Streaming responses
- Custom middleware hooks
- Metrics collection
- Request validation

## Getting Started with Development

To work with this SDK:

```bash
# Clone and enter directory
cd kairos-sdk-go

# Run tests
go test -v ./...

# Build example
go build ./example

# Format code
go fmt ./...

# Run linter
golangci-lint run

# Check for issues
go vet ./...
```

## License

Copyright (c) Kairos. All rights reserved.
