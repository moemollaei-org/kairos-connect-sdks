package kairos

import (
	"context"
	"fmt"
)

// demoClientNew demonstrates creating a new Kairos client.
func demoClientNew() {
	client, _ := New("kairos_sk_test")
	fmt.Printf("Client created with base URL: %s\n", client.baseURL)
	// Output: Client created with base URL: https://gateway.thekairos.app/v1
}

// demoClientNewWithOptions demonstrates creating a client with options.
func demoClientNewWithOptions() {
	client, _ := New("kairos_sk_test",
		WithBaseURL("https://custom.api.com/v1"),
		WithMaxRetries(5),
	)
	fmt.Printf("Client with custom config: %s, retries: %d\n", client.baseURL, client.maxRetries)
	// Output: Client with custom config: https://custom.api.com/v1, retries: 5
}

// demoTasksServiceCreate demonstrates creating a task.
func demoTasksServiceCreate() {
	// In a real scenario, you would use a valid API key and server
	client, _ := New("kairos_sk_test")
	_ = client

	input := CreateTaskInput{
		Title:    "Implement authentication",
		Priority: stringPtr("high"),
		Status:   stringPtr("open"),
	}
	_ = input
	// task, err := client.Tasks.Create(context.Background(), input)
}

// demoTasksServiceUpdate demonstrates updating a task.
func demoTasksServiceUpdate() {
	client, _ := New("kairos_sk_test")
	_ = client

	status := "in_progress"
	input := UpdateTaskInput{
		Status: &status,
	}
	_ = input
	// task, err := client.Tasks.Update(context.Background(), "task-id", input)
}

// demoGoalsServiceCreate demonstrates creating a goal.
func demoGoalsServiceCreate() {
	client, _ := New("kairos_sk_test")
	_ = client

	input := CreateGoalInput{
		Title:       "Q1 2024 Objectives",
		Description: stringPtr("Key objectives for Q1"),
	}
	_ = input
	// goal, err := client.Goals.Create(context.Background(), input)
}

// demoTasksServiceList demonstrates listing tasks with filters.
func demoTasksServiceList() {
	client, _ := New("kairos_sk_test")
	_ = client

	opts := &ListTasksOptions{
		Status:   "open",
		Priority: "high",
		ListOptions: ListOptions{
			Limit:  20,
			Offset: 0,
		},
	}
	_ = opts
	// tasks, pagination, err := client.Tasks.List(context.Background(), opts)
}

// demoKairosErrorIsNotFoundError demonstrates error handling.
func demoKairosErrorIsNotFoundError() {
	client, _ := New("kairos_sk_test")
	_ = client

	// In a real scenario with an actual error response:
	// task, err := client.Tasks.Get(context.Background(), "nonexistent")
	// if IsNotFoundError(err) {
	//     fmt.Println("Task not found")
	// }
}

// demoClientServices demonstrates accessing different service clients.
func demoClientServices() {
	client, _ := New("kairos_sk_test")

	// Access different service clients
	_ = client.Tasks      // TasksService
	_ = client.Goals      // GoalsService
	_ = client.Team       // TeamService
	_ = client.Documents  // DocumentsService
}

// demoContextTimeout demonstrates using context with timeouts.
func demoContextTimeout() {
	client, _ := New("kairos_sk_test")
	_ = client

	ctx, cancel := context.WithTimeout(context.Background(), 0)
	defer cancel()

	// This will fail fast due to timeout
	_ = ctx
	// tasks, _, err := client.Tasks.List(ctx, nil)
}

func stringPtr(s string) *string {
	return &s
}
