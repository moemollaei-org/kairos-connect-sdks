# Kairos Go SDK - File Index

## Quick Navigation

### Starting Points
- **README.md** - Start here for user-facing documentation and examples
- **BUILD_SUMMARY.txt** - Overview of what was built
- **QUICKREF.md** - Quick reference for common operations

### Implementation
- **IMPLEMENTATION.md** - Deep technical details
- **MANIFEST.md** - Complete file listing with stats

## File Directory

### Configuration
```
go.mod                          Module definition (52 bytes)
```

### Core Library (9 files, 842 lines)
```
kairos.go                       Main client (2.1K)
  • Client struct
  • New() initialization
  • Me() endpoint
  • ClientOption pattern

types.go                        Data structures (4.8K)
  • Task, Goal, Comment
  • Team, TeamMember
  • Document
  • Pagination, RateLimit
  • Input types

errors.go                       Error handling (1.1K)
  • KairosError struct
  • IsAuthError()
  • IsForbiddenError()
  • IsNotFoundError()
  • IsRateLimitError()

http.go                         HTTP transport (5.5K)
  • do() request execution
  • get(), post(), patch(), delete()
  • Request/response marshaling
  • Retry logic for 429
  • Rate limit parsing
  • Query encoding

tasks.go                        Task operations (2.5K)
  • TasksService
  • List(), Get(), Create(), Update(), Delete()
  • ListComments(), AddComment()

goals.go                        Goal operations (1.9K)
  • GoalsService
  • List(), Get(), Create(), Update()
  • ListTasks()

team.go                         Team operations (851 bytes)
  • TeamService
  • Get()
  • ListMembers()

documents.go                    Document operations (884 bytes)
  • DocumentsService
  • List(), Get()
```

### Test Suite (6 files, 1,030 lines)
```
kairos_test.go                  Client tests (2.7K)
  • Test New() with API key
  • Test New() with env var
  • Test New() error handling
  • Test New() with options
  • Test Me() endpoint
  • Test service initialization

tasks_test.go                   Task tests (11K)
  • Test List() with pagination
  • Test Get() success
  • Test Get() 404 error
  • Test Create()
  • Test Update()
  • Test Delete()
  • Test 401 auth error
  • Test 429 rate limit retry
  • Test AddComment()
  • Test ListComments()

goals_test.go                   Goal tests (5.5K)
  • Test List()
  • Test Get()
  • Test Create()
  • Test Update()
  • Test ListTasks()

team_test.go                    Team tests (2.6K)
  • Test Get()
  • Test ListMembers()

documents_test.go               Document tests (2.3K)
  • Test List()
  • Test Get()

example_test.go                 Usage examples (3.2K)
  • ExampleClient_New()
  • ExampleClient_New_withOptions()
  • ExampleTasksService_Create()
  • ExampleTasksService_Update()
  • ExampleGoalsService_Create()
  • ExampleTasksService_List()
  • ExampleKairosError_IsNotFoundError()
  • ExampleClient_Services()
  • ExampleContext_Timeout()
```

### Documentation (5 files)
```
README.md                       User guide (4.9K)
  • Installation
  • Quick start example
  • Context support
  • Error handling
  • Configuration
  • API key management
  • Rate limiting
  • Thread safety
  • Supported resources
  • Testing

IMPLEMENTATION.md               Technical guide (8.2K)
  • Architecture overview
  • Project structure
  • Core components
  • Design principles
  • Testing strategy
  • API response format
  • Configuration options
  • Performance considerations
  • Future enhancements

QUICKREF.md                     Quick reference (7.8K)
  • Installation
  • Basic usage
  • Tasks operations
  • Goals operations
  • Team operations
  • Documents operations
  • Authentication
  • Error handling
  • Configuration
  • Context usage
  • Pagination
  • Rate limiting
  • Structs reference
  • Error types
  • Helper functions
  • Testing
  • Concurrency
  • Common patterns

MANIFEST.md                     File manifest (9.3K)
  • Complete file listing
  • Statistics
  • Features summary
  • Quality metrics
  • Code breakdown
  • Usage summary
  • Deployment notes

BUILD_SUMMARY.txt               Build overview (8.3K)
  • Project info
  • Files delivered
  • Statistics
  • Features
  • Error handling
  • Testing
  • Code quality
  • Usage example
  • Configuration options
  • Next steps
  • Verification results

INDEX.md                        This file
```

## How to Use This SDK

### For Users
1. Read **README.md** for installation and basic usage
2. Check **QUICKREF.md** for common operations
3. Run tests with `go test -v ./...`

### For Developers
1. Study **IMPLEMENTATION.md** for architecture
2. Review **kairos.go** and **http.go** for core logic
3. Check test files for usage patterns
4. Read inline comments in code

### For Integration
1. Copy files to your project or use `go get`
2. Import `github.com/moemollaei-org/kairos-connect-sdks/go`
3. Create a client: `client, _ := kairos.New(apiKey)`
4. Use services: `client.Tasks.List()`, `client.Goals.Create()`, etc.

## API Services Reference

### Tasks Service
```
List(ctx, opts)          - Get paginated tasks
Get(ctx, id)             - Get single task
Create(ctx, input)       - Create new task
Update(ctx, id, input)   - Update task
Delete(ctx, id)          - Delete task
ListComments(...)        - Get task comments
AddComment(...)          - Add comment to task
```

### Goals Service
```
List(ctx, opts)          - Get paginated goals
Get(ctx, id)             - Get single goal
Create(ctx, input)       - Create new goal
Update(ctx, id, input)   - Update goal
ListTasks(...)           - Get goal's tasks
```

### Team Service
```
Get(ctx)                 - Get team info
ListMembers(ctx, opts)   - Get team members
```

### Documents Service
```
List(ctx, opts)          - Get paginated documents
Get(ctx, id)             - Get single document
```

### Client
```
New(apiKey, opts...)     - Create client
Me(ctx)                  - Validate API key
```

## Feature Checklist

- [x] Zero external dependencies
- [x] All CRUD operations
- [x] Pagination support
- [x] Error handling with helpers
- [x] Automatic retry on 429
- [x] Rate limit header parsing
- [x] Context support
- [x] Thread-safe client
- [x] Configuration options
- [x] Environment variable support
- [x] Comprehensive tests (25 tests)
- [x] Complete documentation
- [x] Example code

## Statistics at a Glance

| Metric | Count |
|--------|-------|
| Total Files | 20 |
| Go Files | 14 |
| Test Files | 6 |
| Lines of Code | 3,100+ |
| Test Functions | 25 |
| API Endpoints | 11 |
| Documentation Pages | 5 |
| External Dependencies | 0 |

## Getting Started

```bash
# Installation
go get github.com/moemollaei-org/kairos-connect-sdks/go

# Basic usage
package main
import "github.com/moemollaei-org/kairos-connect-sdks/go"

func main() {
    client, _ := kairos.New("kairos_sk_...")
    tasks, _, _ := client.Tasks.List(ctx, nil)
}
```

## Support

For issues or questions:
1. Check QUICKREF.md for quick answers
2. Review IMPLEMENTATION.md for technical details
3. Look at test files for usage examples
4. Check README.md for common scenarios

## Version

- SDK Version: 0.1.0
- Go Version: 1.21+
- API Base: https://gateway.thekairos.app/v1

---

**Last Updated**: April 5, 2026
**Status**: Production Ready
**Dependencies**: None (Standard Library Only)
