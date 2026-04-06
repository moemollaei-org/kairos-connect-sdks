# kairos-go

Official Go SDK for [Kairos](https://thekairos.app).

## Installation

```bash
go get github.com/moemollaei-org/kairos-connect-sdks/go
```

## Quick Start

```go
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/moemollaei-org/kairos-connect-sdks/go"
)

func main() {
	// Create a client with an API key
	client, err := kairos.New("kairos_sk_...")
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}

	ctx := context.Background()

	// Validate API key and get team info
	me, err := client.Me(ctx)
	if err != nil {
		log.Fatalf("Failed to get me: %v", err)
	}
	fmt.Printf("Team ID: %s\n", me.TeamID)
	fmt.Printf("Scopes: %v\n", me.Scopes)

	// List tasks
	tasks, pagination, err := client.Tasks.List(ctx, nil)
	if err != nil {
		log.Fatalf("Failed to list tasks: %v", err)
	}
	fmt.Printf("Found %d tasks (total: %d)\n", len(tasks), pagination.Total)

	// Get a specific task
	task, err := client.Tasks.Get(ctx, "task-id")
	if err != nil {
		log.Fatalf("Failed to get task: %v", err)
	}
	fmt.Printf("Task: %s (%s)\n", task.Title, task.Status)

	// Create a new task
	newTask, err := client.Tasks.Create(ctx, kairos.CreateTaskInput{
		Title:    "New Feature",
		Priority: ptrString("high"),
		Status:   ptrString("open"),
	})
	if err != nil {
		log.Fatalf("Failed to create task: %v", err)
	}
	fmt.Printf("Created task: %s\n", newTask.ID)

	// Update a task
	status := "in_progress"
	updated, err := client.Tasks.Update(ctx, newTask.ID, kairos.UpdateTaskInput{
		Status: &status,
	})
	if err != nil {
		log.Fatalf("Failed to update task: %v", err)
	}
	fmt.Printf("Updated task status to: %s\n", updated.Status)

	// Add a comment to a task
	comment, err := client.Tasks.AddComment(ctx, newTask.ID, "Great work on this!")
	if err != nil {
		log.Fatalf("Failed to add comment: %v", err)
	}
	fmt.Printf("Added comment: %s\n", comment.ID)

	// List goals
	goals, _, err := client.Goals.List(ctx, nil)
	if err != nil {
		log.Fatalf("Failed to list goals: %v", err)
	}
	fmt.Printf("Found %d goals\n", len(goals))

	// Create a goal
	newGoal, err := client.Goals.Create(ctx, kairos.CreateGoalInput{
		Title: "Q1 Objectives",
	})
	if err != nil {
		log.Fatalf("Failed to create goal: %v", err)
	}
	fmt.Printf("Created goal: %s\n", newGoal.ID)

	// Get team info
	team, err := client.Team.Get(ctx)
	if err != nil {
		log.Fatalf("Failed to get team: %v", err)
	}
	fmt.Printf("Team: %s\n", team.Name)

	// List team members
	members, _, err := client.Team.ListMembers(ctx, nil)
	if err != nil {
		log.Fatalf("Failed to list members: %v", err)
	}
	fmt.Printf("Found %d team members\n", len(members))

	// List documents
	docs, _, err := client.Documents.List(ctx, nil)
	if err != nil {
		log.Fatalf("Failed to list documents: %v", err)
	}
	fmt.Printf("Found %d documents\n", len(docs))
}

func ptrString(s string) *string {
	return &s
}
```

## Context Support

All methods accept `context.Context` as the first argument. This allows you to set timeouts, deadlines, and cancellation:

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

task, err := client.Tasks.Get(ctx, "task-id")
```

## Error Handling

The SDK returns `*kairos.KairosError` for API errors. You can use helper functions to check error types:

```go
task, err := client.Tasks.Get(ctx, "task-id")
if err != nil {
	if kairos.IsNotFoundError(err) {
		fmt.Println("Task not found")
	} else if kairos.IsAuthError(err) {
		fmt.Println("Authentication failed")
	} else if kairos.IsForbiddenError(err) {
		fmt.Println("Access denied")
	} else if kairos.IsRateLimitError(err) {
		fmt.Println("Rate limit exceeded")
	} else {
		fmt.Printf("Error: %v\n", err)
	}
}
```

## Configuration

The client can be configured with options:

```go
client, err := kairos.New("kairos_sk_...",
	kairos.WithBaseURL("https://custom.api.url/v1"),
	kairos.WithMaxRetries(5),
	kairos.WithTimeout(60*time.Second),
	kairos.WithHTTPClient(customHTTPClient),
)
```

## API Key Management

The API key can be provided in two ways:

1. **Direct argument**: Pass the API key when creating a client
2. **Environment variable**: Set `KAIROS_API_KEY` and call `kairos.New("")`

```go
// Method 1: Direct argument
client, _ := kairos.New("kairos_sk_...")

// Method 2: Environment variable
client, _ := kairos.New("")  // Reads from KAIROS_API_KEY
```

## Rate Limiting

The SDK automatically retries requests that return 429 (Too Many Requests) with exponential backoff. The default is 3 retries.

## Thread Safety

The `*Client` is safe for concurrent use from multiple goroutines. You can safely share a single client instance across your application.

## Supported Resources

- **Tasks**: CRUD operations, comments
- **Goals**: CRUD operations, task listing
- **Team**: Get team info, list members
- **Documents**: List and get documents
- **Me**: Validate API key and get account info

## Testing

Run the test suite:

```bash
go test ./...
```

## License

This SDK is provided by Kairos. See LICENSE for details.
