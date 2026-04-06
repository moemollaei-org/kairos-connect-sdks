# Kairos Go SDK - Quick Reference

## Installation
```bash
go get github.com/moemollaei-org/kairos-connect-sdks/go
```

## Basic Usage
```go
client, err := kairos.New("kairos_sk_...")
if err != nil {
    log.Fatal(err)
}
ctx := context.Background()
```

## Tasks

### List Tasks
```go
tasks, pagination, err := client.Tasks.List(ctx, &kairos.ListTasksOptions{
    Status: "open",
    Priority: "high",
})
```

### Get Task
```go
task, err := client.Tasks.Get(ctx, "task-id")
```

### Create Task
```go
task, err := client.Tasks.Create(ctx, kairos.CreateTaskInput{
    Title: "New Task",
    Priority: stringPtr("high"),
    Status: stringPtr("open"),
})
```

### Update Task
```go
task, err := client.Tasks.Update(ctx, "task-id", kairos.UpdateTaskInput{
    Status: stringPtr("completed"),
})
```

### Delete Task
```go
err := client.Tasks.Delete(ctx, "task-id")
```

### Task Comments
```go
// List comments
comments, pagination, err := client.Tasks.ListComments(ctx, "task-id", nil)

// Add comment
comment, err := client.Tasks.AddComment(ctx, "task-id", "Great work!")
```

## Goals

### List Goals
```go
goals, pagination, err := client.Goals.List(ctx, &kairos.ListOptions{
    Limit: 10,
    Offset: 0,
})
```

### Get Goal
```go
goal, err := client.Goals.Get(ctx, "goal-id")
```

### Create Goal
```go
goal, err := client.Goals.Create(ctx, kairos.CreateGoalInput{
    Title: "Q1 Objectives",
})
```

### Update Goal
```go
goal, err := client.Goals.Update(ctx, "goal-id", kairos.UpdateGoalInput{
    Status: stringPtr("completed"),
})
```

### Goal Tasks
```go
tasks, pagination, err := client.Goals.ListTasks(ctx, "goal-id", &kairos.ListTasksOptions{
    Status: "open",
})
```

## Team

### Get Team
```go
team, err := client.Team.Get(ctx)
```

### List Members
```go
members, pagination, err := client.Team.ListMembers(ctx, &kairos.ListOptions{
    Limit: 20,
})
```

## Documents

### List Documents
```go
docs, pagination, err := client.Documents.List(ctx, nil)
```

### Get Document
```go
doc, err := client.Documents.Get(ctx, "doc-id")
```

## Authentication

### Validate API Key
```go
me, err := client.Me(ctx)
if err != nil {
    // Authentication failed
}
fmt.Println("Team ID:", me.TeamID)
fmt.Println("Scopes:", me.Scopes)
```

### API Key from Environment
```go
client, err := kairos.New("")  // Reads from KAIROS_API_KEY env var
```

## Error Handling

```go
task, err := client.Tasks.Get(ctx, "task-id")
if err != nil {
    if kairos.IsNotFoundError(err) {
        fmt.Println("Task not found")
    } else if kairos.IsAuthError(err) {
        fmt.Println("Authentication failed")
    } else if kairos.IsRateLimitError(err) {
        fmt.Println("Rate limit exceeded")
    } else if kairos.IsForbiddenError(err) {
        fmt.Println("Permission denied")
    } else {
        fmt.Printf("Error: %v\n", err)
    }
}
```

## Configuration

### Custom Base URL
```go
client, err := kairos.New(apiKey, kairos.WithBaseURL("https://custom.url/v1"))
```

### Custom Timeout
```go
client, err := kairos.New(apiKey, kairos.WithTimeout(60*time.Second))
```

### Custom HTTP Client
```go
httpClient := &http.Client{
    Timeout: 30*time.Second,
}
client, err := kairos.New(apiKey, kairos.WithHTTPClient(httpClient))
```

### Max Retries
```go
client, err := kairos.New(apiKey, kairos.WithMaxRetries(5))
```

## Context

### With Timeout
```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
task, err := client.Tasks.Get(ctx, "task-id")
```

### With Deadline
```go
ctx, cancel := context.WithDeadline(context.Background(), time.Now().Add(1*time.Minute))
defer cancel()
tasks, _, err := client.Tasks.List(ctx, nil)
```

### With Value
```go
ctx := context.WithValue(context.Background(), "requestID", "abc-123")
task, err := client.Tasks.Get(ctx, "task-id")
```

## Pagination

```go
tasks, pagination, err := client.Tasks.List(ctx, &kairos.ListTasksOptions{
    ListOptions: kairos.ListOptions{
        Limit: 10,
        Offset: 0,
    },
})

if pagination.HasMore {
    // Load more results
    nextOffset := pagination.Limit * pagination.Page
    tasks, _, _ := client.Tasks.List(ctx, &kairos.ListTasksOptions{
        ListOptions: kairos.ListOptions{
            Limit: pagination.Limit,
            Offset: nextOffset,
        },
    })
}
```

## Rate Limiting

The SDK automatically retries on 429 (Too Many Requests) with exponential backoff.

```go
// Configure retries
client, _ := kairos.New(apiKey, kairos.WithMaxRetries(5))

// Check if error is rate limit
if kairos.IsRateLimitError(err) {
    fmt.Println("Rate limited - will retry automatically")
}
```

## Structs Reference

### Task
```go
type Task struct {
    ID          string
    TeamID      string
    GoalID      *string
    Title       string
    Description *string
    Type        string
    Status      string
    Priority    string
    AssignedTo  *string
    DueDate     *string
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

### Goal
```go
type Goal struct {
    ID          string
    TeamID      string
    Title       string
    Description *string
    Status      string
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

### Pagination
```go
type Pagination struct {
    Page    int
    Limit   int
    Total   int
    HasMore bool
}
```

### RateLimit
```go
type RateLimit struct {
    LimitMinute     int
    RemainingMinute int
    LimitHour       int
    RemainingHour   int
    Reset           int64
}
```

## Error Types

```go
type KairosError struct {
    Code       string  // API error code
    Message    string  // Human-readable message
    StatusCode int     // HTTP status code
    RequestID  string  // Request ID for debugging
}

// Helper functions
kairos.IsAuthError(err)          // 401 Unauthorized
kairos.IsForbiddenError(err)     // 403 Forbidden
kairos.IsNotFoundError(err)      // 404 Not Found
kairos.IsRateLimitError(err)     // 429 Too Many Requests
```

## Helper Functions

```go
// Create string pointer
func stringPtr(s string) *string {
    return &s
}

// Usage
title := stringPtr("My Task")
task, _ := client.Tasks.Create(ctx, kairos.CreateTaskInput{
    Title: "New Task",
    Priority: stringPtr("high"),
})
```

## Testing

```go
// Run all tests
go test ./...

// Run with verbose output
go test -v ./...

// Run specific test
go test -run TestTasksCreate

// Run with coverage
go test -cover ./...
```

## Concurrency

The client is thread-safe and can be shared across goroutines:

```go
client, _ := kairos.New("kairos_sk_...")

// Safe to use from multiple goroutines
go func() {
    tasks, _, _ := client.Tasks.List(context.Background(), nil)
}()

go func() {
    goal, _ := client.Goals.Get(context.Background(), "goal-id")
}()
```

## Common Patterns

### Fetch with Retry
```go
var task *kairos.Task
var err error
for i := 0; i < 3; i++ {
    task, err = client.Tasks.Get(ctx, "task-id")
    if err == nil {
        break
    }
    time.Sleep(time.Duration(math.Pow(2, float64(i))) * time.Second)
}
```

### List All Items
```go
var allTasks []kairos.Task
offset := 0
limit := 50

for {
    tasks, pagination, err := client.Tasks.List(ctx, &kairos.ListTasksOptions{
        ListOptions: kairos.ListOptions{
            Limit: limit,
            Offset: offset,
        },
    })

    allTasks = append(allTasks, tasks...)

    if !pagination.HasMore {
        break
    }

    offset += limit
}
```

### Bulk Operations
```go
// Create multiple tasks
inputs := []kairos.CreateTaskInput{
    {Title: "Task 1"},
    {Title: "Task 2"},
    {Title: "Task 3"},
}

for _, input := range inputs {
    task, err := client.Tasks.Create(ctx, input)
    if err != nil {
        log.Printf("Failed to create task: %v", err)
    } else {
        log.Printf("Created task: %s", task.ID)
    }
}
```

## Version Info
- SDK Version: 0.1.0
- Minimum Go Version: 1.21
- Dependencies: None (standard library only)
