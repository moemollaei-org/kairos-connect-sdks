package kairos

import "context"

// DocumentsService provides document operations.
type DocumentsService struct {
	client *Client
}

// List returns a paginated list of documents (requires read:documents scope).
// Workers return: { documents: [...], total_count, limit, offset }
// team_id is injected automatically by the gateway proxy from the API key.
func (s *DocumentsService) List(ctx context.Context, opts *ListDocumentsOptions) ([]Document, *Pagination, error) {
	if opts == nil {
		opts = &ListDocumentsOptions{}
	}

	var resp struct {
		Documents  []Document `json:"documents"`
		TotalCount int        `json:"total_count"`
		Total      int        `json:"total"` // fallback alias
		HasMore    bool       `json:"hasMore"`
		Limit      int        `json:"limit"`
		Offset     int        `json:"offset"`
	}

	_, err := s.client.get(ctx, "/documents", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	total := resp.TotalCount
	if total == 0 {
		total = resp.Total
	}
	return resp.Documents, nativePagination(total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// Get returns a single document by ID (requires read:documents scope).
// Workers return: { document: {...} }
func (s *DocumentsService) Get(ctx context.Context, id string) (*Document, error) {
	var resp struct {
		Document *Document `json:"document"`
	}

	_, err := s.client.get(ctx, "/documents/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Document, nil
}

// Create creates a new document (requires write:documents scope).
// Workers return: { document: {...} }
func (s *DocumentsService) Create(ctx context.Context, input CreateDocumentInput) (*Document, error) {
	var resp struct {
		Document *Document `json:"document"`
	}

	_, err := s.client.post(ctx, "/documents", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Document, nil
}

// Update updates a document (requires write:documents scope).
// Workers return: { document: {...} }
func (s *DocumentsService) Update(ctx context.Context, id string, input UpdateDocumentInput) (*Document, error) {
	var resp struct {
		Document *Document `json:"document"`
	}

	_, err := s.client.put(ctx, "/documents/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Document, nil
}

// Delete deletes a document (requires write:documents scope).
func (s *DocumentsService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, "/documents/"+id, nil)
	return err
}

// ListComments returns comments on a document (requires read:comments scope).
func (s *DocumentsService) ListComments(ctx context.Context, documentID string, opts *ListOptions) ([]Comment, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Comments []Comment `json:"comments"`
		Total    int       `json:"total"`
		HasMore  bool      `json:"hasMore"`
		Limit    int       `json:"limit"`
		Offset   int       `json:"offset"`
	}

	_, err := s.client.get(ctx, "/documents/"+documentID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Comments, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// AddComment adds a comment to a document (requires write:comments scope).
func (s *DocumentsService) AddComment(ctx context.Context, documentID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.post(ctx, "/documents/"+documentID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *DocumentsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.put(ctx, "/comments/"+commentID, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// DeleteComment deletes a comment (requires write:comments scope).
func (s *DocumentsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
