package kairos

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestDocumentsList(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": []map[string]interface{}{
				{
					"id":         "doc-1",
					"team_id":    "team-1",
					"title":      "Q1 Plan",
					"content":    "Some content",
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
	documents, pagination, err := client.Documents.List(context.Background(), nil)

	if err != nil {
		t.Fatalf("List failed: %v", err)
	}

	if len(documents) != 1 {
		t.Errorf("Expected 1 document, got %d", len(documents))
	}

	if documents[0].Title != "Q1 Plan" {
		t.Errorf("Expected title 'Q1 Plan', got '%s'", documents[0].Title)
	}

	if pagination.Total != 1 {
		t.Errorf("Expected total 1, got %d", pagination.Total)
	}
}

func TestDocumentsGet(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		response := map[string]interface{}{
			"data": map[string]interface{}{
				"id":         "doc-1",
				"team_id":    "team-1",
				"title":      "Q1 Plan",
				"content":    "Some content",
				"created_by": "user-1",
				"created_at": time.Now().UTC().Format(time.RFC3339),
				"updated_at": time.Now().UTC().Format(time.RFC3339),
			},
		}
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	client, _ := New("test-key", WithBaseURL(server.URL))
	doc, err := client.Documents.Get(context.Background(), "doc-1")

	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}

	if doc.ID != "doc-1" {
		t.Errorf("Expected ID 'doc-1', got '%s'", doc.ID)
	}

	if doc.Title != "Q1 Plan" {
		t.Errorf("Expected title 'Q1 Plan', got '%s'", doc.Title)
	}
}
