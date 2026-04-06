package kairos

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestTeamGet(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"id":         "team-1",
				"name":       "Acme Corp",
				"created_at": time.Now().UTC().Format(time.RFC3339),
				"updated_at": time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	team, err := client.Team.Get(context.Background())

	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}

	if team.ID != "team-1" {
		t.Errorf("Expected ID 'team-1', got '%s'", team.ID)
	}

	if team.Name != "Acme Corp" {
		t.Errorf("Expected name 'Acme Corp', got '%s'", team.Name)
	}
}

func TestTeamListMembers(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": []map[string]interface{}{
				{
					"id":         "member-1",
					"team_id":    "team-1",
					"email":      "alice@example.com",
					"name":       "Alice",
					"role":       "admin",
					"created_at": time.Now().UTC().Format(time.RFC3339),
					"updated_at": time.Now().UTC().Format(time.RFC3339),
				},
				{
					"id":         "member-2",
					"team_id":    "team-1",
					"email":      "bob@example.com",
					"name":       "Bob",
					"role":       "member",
					"created_at": time.Now().UTC().Format(time.RFC3339),
					"updated_at": time.Now().UTC().Format(time.RFC3339),
				},
			},
			"pagination": map[string]interface{}{
				"page":     1,
				"limit":    10,
				"total":    2,
				"has_more": false,
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	members, pagination, err := client.Team.ListMembers(context.Background(), nil)

	if err != nil {
		t.Fatalf("ListMembers failed: %v", err)
	}

	if len(members) != 2 {
		t.Errorf("Expected 2 members, got %d", len(members))
	}

	if members[0].Email != "alice@example.com" {
		t.Errorf("Expected email 'alice@example.com', got '%s'", members[0].Email)
	}

	if members[1].Role != "member" {
		t.Errorf("Expected role 'member', got '%s'", members[1].Role)
	}

	if pagination.Total != 2 {
		t.Errorf("Expected total 2, got %d", pagination.Total)
	}
}
