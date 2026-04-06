package kairos

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestGoalsList(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"goals": []map[string]interface{}{
				{
					"id":          "goal-1",
					"team_id":     "team-1",
					"title":       "Q1 Objectives",
					"description": "Goals for Q1",
					"status":      "active",
					"created_by":  "user-1",
					"created_at":  time.Now().UTC().Format(time.RFC3339),
					"updated_at":  time.Now().UTC().Format(time.RFC3339),
				},
			},
			"total":     1,
			"hasMore":   false,
			"limit":     10,
			"count":     1,
			"offset":    0,
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	goals, pagination, err := client.Goals.List(context.Background(), nil)

	if err != nil {
		t.Fatalf("List failed: %v", err)
	}

	if len(goals) != 1 {
		t.Errorf("Expected 1 goal, got %d", len(goals))
	}

	if goals[0].Title != "Q1 Objectives" {
		t.Errorf("Expected title 'Q1 Objectives', got '%s'", goals[0].Title)
	}

	if pagination.Total != 1 {
		t.Errorf("Expected total 1, got %d", pagination.Total)
	}
}

func TestGoalsGet(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"goal": map[string]interface{}{
				"id":          "goal-1",
				"team_id":     "team-1",
				"title":       "Q1 Objectives",
				"description": "Goals for Q1",
				"status":      "active",
				"created_by":  "user-1",
				"created_at":  time.Now().UTC().Format(time.RFC3339),
				"updated_at":  time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	goal, err := client.Goals.Get(context.Background(), "goal-1")

	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}

	if goal.ID != "goal-1" {
		t.Errorf("Expected ID 'goal-1', got '%s'", goal.ID)
	}

	if goal.Title != "Q1 Objectives" {
		t.Errorf("Expected title 'Q1 Objectives', got '%s'", goal.Title)
	}
}

func TestGoalsCreate(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"goal": map[string]interface{}{
				"id":         "goal-2",
				"team_id":    "team-1",
				"title":      "New Goal",
				"status":     "active",
				"created_by": "user-1",
				"created_at": time.Now().UTC().Format(time.RFC3339),
				"updated_at": time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	input := CreateGoalInput{Title: "New Goal"}
	goal, err := client.Goals.Create(context.Background(), input)

	if err != nil {
		t.Fatalf("Create failed: %v", err)
	}

	if goal.Title != "New Goal" {
		t.Errorf("Expected title 'New Goal', got '%s'", goal.Title)
	}
}

func TestGoalsUpdate(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPatch {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"goal": map[string]interface{}{
				"id":     "goal-1",
				"title":  "Updated Goal",
				"status": "completed",
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	status := "completed"
	input := UpdateGoalInput{Status: &status}
	goal, err := client.Goals.Update(context.Background(), "goal-1", input)

	if err != nil {
		t.Fatalf("Update failed: %v", err)
	}

	if goal.Status != "completed" {
		t.Errorf("Expected status 'completed', got '%s'", goal.Status)
	}
}

func TestGoalsListTasks(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"tasks": []map[string]interface{}{
				{
					"id":         "task-1",
					"team_id":    "team-1",
					"goal_id":    "goal-1",
					"title":      "Task 1",
					"status":     "open",
					"created_by": "user-1",
					"created_at": time.Now().UTC().Format(time.RFC3339),
					"updated_at": time.Now().UTC().Format(time.RFC3339),
				},
			},
			"total":     1,
			"hasMore":   false,
			"limit":     10,
			"count":     1,
			"offset":    0,
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	tasks, pagination, err := client.Goals.ListTasks(context.Background(), "goal-1", nil)

	if err != nil {
		t.Fatalf("ListTasks failed: %v", err)
	}

	if len(tasks) != 1 {
		t.Errorf("Expected 1 task, got %d", len(tasks))
	}

	if pagination.Total != 1 {
		t.Errorf("Expected total 1, got %d", pagination.Total)
	}
}
