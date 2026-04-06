package kairos

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestTasksList(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Authorization") != "Bearer test-key" {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": []map[string]interface{}{
				{
					"id":            "task-1",
					"team_id":       "team-1",
					"goal_id":       nil,
					"parent_task_id": nil,
					"title":         "Test Task",
					"description":   "A test task",
					"type":          "feature",
					"status":        "open",
					"priority":      "high",
					"assigned_to":   nil,
					"due_date":      nil,
					"completed_at":  nil,
					"created_by":    "user-1",
					"created_at":    time.Now().UTC().Format(time.RFC3339),
					"updated_at":    time.Now().UTC().Format(time.RFC3339),
				},
			},
			"pagination": map[string]interface{}{
				"page":     1,
				"limit":    10,
				"total":    1,
				"has_more": false,
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	tasks, pagination, err := client.Tasks.List(context.Background(), nil)

	if err != nil {
		t.Fatalf("List failed: %v", err)
	}

	if len(tasks) != 1 {
		t.Errorf("Expected 1 task, got %d", len(tasks))
	}

	if tasks[0].Title != "Test Task" {
		t.Errorf("Expected title 'Test Task', got '%s'", tasks[0].Title)
	}

	if pagination.Total != 1 {
		t.Errorf("Expected total 1, got %d", pagination.Total)
	}
}

func TestTasksGet(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"id":            "task-1",
				"team_id":       "team-1",
				"title":         "Test Task",
				"description":   "A test task",
				"type":          "feature",
				"status":        "open",
				"priority":      "high",
				"created_by":    "user-1",
				"created_at":    time.Now().UTC().Format(time.RFC3339),
				"updated_at":    time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	task, err := client.Tasks.Get(context.Background(), "task-1")

	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}

	if task.ID != "task-1" {
		t.Errorf("Expected ID 'task-1', got '%s'", task.ID)
	}

	if task.Title != "Test Task" {
		t.Errorf("Expected title 'Test Task', got '%s'", task.Title)
	}
}

func TestTasksGetNotFound(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusNotFound)

		response := map[string]interface{}{
			"error": map[string]interface{}{
				"code":       "not_found",
				"message":    "Task not found",
				"request_id": "req-123",
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	_, err := client.Tasks.Get(context.Background(), "nonexistent")

	if err == nil {
		t.Fatalf("Expected error, got nil")
	}

	if !IsNotFoundError(err) {
		t.Errorf("Expected NotFoundError, got %T", err)
	}

	if ke, ok := err.(*KairosError); ok {
		if ke.StatusCode != 404 {
			t.Errorf("Expected status code 404, got %d", ke.StatusCode)
		}
	}
}

func TestTasksCreate(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"id":         "task-2",
				"team_id":    "team-1",
				"title":      "New Task",
				"status":     "open",
				"created_by": "user-1",
				"created_at": time.Now().UTC().Format(time.RFC3339),
				"updated_at": time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	input := CreateTaskInput{Title: "New Task"}
	task, err := client.Tasks.Create(context.Background(), input)

	if err != nil {
		t.Fatalf("Create failed: %v", err)
	}

	if task.Title != "New Task" {
		t.Errorf("Expected title 'New Task', got '%s'", task.Title)
	}
}

func TestTasksUpdate(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPatch {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"id":     "task-1",
				"title":  "Updated Task",
				"status": "in_progress",
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	status := "in_progress"
	input := UpdateTaskInput{Status: &status}
	task, err := client.Tasks.Update(context.Background(), "task-1", input)

	if err != nil {
		t.Fatalf("Update failed: %v", err)
	}

	if task.Status != "in_progress" {
		t.Errorf("Expected status 'in_progress', got '%s'", task.Status)
	}
}

func TestTasksDelete(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodDelete {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		w.WriteHeader(http.StatusNoContent)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	err := client.Tasks.Delete(context.Background(), "task-1")

	if err != nil {
		t.Fatalf("Delete failed: %v", err)
	}
}

func TestAuthError(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusUnauthorized)

		response := map[string]interface{}{
			"error": map[string]interface{}{
				"code":       "unauthorized",
				"message":    "Invalid API key",
				"request_id": "req-456",
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("invalid-key", WithBaseURL(server.URL))
	_, err := client.Tasks.Get(context.Background(), "task-1")

	if err == nil {
		t.Fatalf("Expected error, got nil")
	}

	if !IsAuthError(err) {
		t.Errorf("Expected AuthError, got %T", err)
	}

	if ke, ok := err.(*KairosError); ok {
		if ke.StatusCode != 401 {
			t.Errorf("Expected status code 401, got %d", ke.StatusCode)
		}
	}
}

func TestRateLimitError(t *testing.T) {
	attempt := 0
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		attempt++
		if attempt < 3 {
			w.Header().Set("Content-Type", "application/json")
			w.Header().Set("Retry-After", "1")
			w.WriteHeader(http.StatusTooManyRequests)

			response := map[string]interface{}{
				"error": map[string]interface{}{
					"code":       "rate_limit_exceeded",
					"message":    "Too many requests",
					"request_id": "req-789",
				},
			}
			json.NewEncoder(w).Encode(response)
		} else {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusOK)

			response := map[string]interface{}{
				"data": map[string]interface{}{
					"id":    "task-1",
					"title": "Test Task",
				},
			}
			json.NewEncoder(w).Encode(response)
		}
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL), WithMaxRetries(2))
	task, err := client.Tasks.Get(context.Background(), "task-1")

	if err != nil {
		t.Fatalf("Get failed after retries: %v", err)
	}

	if task.ID != "task-1" {
		t.Errorf("Expected task after retry, got %v", task)
	}
}

func TestTasksAddComment(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"id":         "comment-1",
				"task_id":    "task-1",
				"content":    "Great work!",
				"created_by": "user-1",
				"created_at": time.Now().UTC().Format(time.RFC3339),
				"updated_at": time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	comment, err := client.Tasks.AddComment(context.Background(), "task-1", "Great work!")

	if err != nil {
		t.Fatalf("AddComment failed: %v", err)
	}

	if comment.Content != "Great work!" {
		t.Errorf("Expected content 'Great work!', got '%s'", comment.Content)
	}
}

func TestTasksListComments(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": []map[string]interface{}{
				{
					"id":         "comment-1",
					"task_id":    "task-1",
					"content":    "Great work!",
					"created_by": "user-1",
					"created_at": time.Now().UTC().Format(time.RFC3339),
					"updated_at": time.Now().UTC().Format(time.RFC3339),
				},
			},
			"pagination": map[string]interface{}{
				"page":     1,
				"limit":    10,
				"total":    1,
				"has_more": false,
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	comments, pagination, err := client.Tasks.ListComments(context.Background(), "task-1", nil)

	if err != nil {
		t.Fatalf("ListComments failed: %v", err)
	}

	if len(comments) != 1 {
		t.Errorf("Expected 1 comment, got %d", len(comments))
	}

	if pagination.Total != 1 {
		t.Errorf("Expected total 1, got %d", pagination.Total)
	}
}
