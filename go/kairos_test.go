package kairos

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
)

func TestNewWithAPIKey(t *testing.T) {
	client, err := New("test-key")

	if err != nil {
		t.Fatalf("New failed: %v", err)
	}

	if client.apiKey != "test-key" {
		t.Errorf("Expected apiKey 'test-key', got '%s'", client.apiKey)
	}

	if client.baseURL != DefaultBaseURL {
		t.Errorf("Expected baseURL '%s', got '%s'", DefaultBaseURL, client.baseURL)
	}
}

func TestNewWithEmptyAPIKeyAndEnvVar(t *testing.T) {
	os.Setenv("KAIROS_API_KEY", "env-key")
	defer os.Unsetenv("KAIROS_API_KEY")

	client, err := New("")

	if err != nil {
		t.Fatalf("New failed: %v", err)
	}

	if client.apiKey != "env-key" {
		t.Errorf("Expected apiKey 'env-key', got '%s'", client.apiKey)
	}
}

func TestNewWithEmptyAPIKeyNoEnvVar(t *testing.T) {
	os.Unsetenv("KAIROS_API_KEY")

	_, err := New("")

	if err == nil {
		t.Fatalf("Expected error when no API key provided")
	}
}

func TestNewWithOptions(t *testing.T) {
	client, err := New("test-key",
		WithBaseURL("https://custom.url"),
		WithMaxRetries(5),
	)

	if err != nil {
		t.Fatalf("New failed: %v", err)
	}

	if client.baseURL != "https://custom.url" {
		t.Errorf("Expected custom baseURL, got '%s'", client.baseURL)
	}

	if client.maxRetries != 5 {
		t.Errorf("Expected maxRetries 5, got %d", client.maxRetries)
	}
}

func TestMe(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Authorization") != "Bearer test-key" {
			w.WriteHeader(http.StatusUnauthorized)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"team_id":               "team-1",
				"scopes":                []string{"read", "write"},
				"rate_limit_per_minute": 60,
				"rate_limit_per_hour":   1000,
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	me, err := client.Me(context.Background())

	if err != nil {
		t.Fatalf("Me failed: %v", err)
	}

	if me.TeamID != "team-1" {
		t.Errorf("Expected TeamID 'team-1', got '%s'", me.TeamID)
	}

	if len(me.Scopes) != 2 {
		t.Errorf("Expected 2 scopes, got %d", len(me.Scopes))
	}

	if me.RateLimitPerMinute != 60 {
		t.Errorf("Expected rate limit 60, got %d", me.RateLimitPerMinute)
	}
}

func TestClientServices(t *testing.T) {
	client, _ := New("test-key")

	if client.Tasks == nil {
		t.Error("Tasks service is nil")
	}

	if client.Goals == nil {
		t.Error("Goals service is nil")
	}

	if client.Team == nil {
		t.Error("Team service is nil")
	}

	if client.Documents == nil {
		t.Error("Documents service is nil")
	}
}
