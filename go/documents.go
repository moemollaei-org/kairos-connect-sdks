package kairos

import "context"

// DocumentsService provides document operations.
type DocumentsService struct {
	client *Client
}

// List returns a paginated list of documents (requires read:documents scope).
// Workers return: { documents: [...], total_count, limit, offset }
// No hasMore field — has_more is computed from total_count vs. returned count.
func (s *DocumentsService) List(ctx context.Context, opts *ListDocumentsOptions) ([]Document, *Pagination, error) {
	if opts == nil {
		opts = &ListDocumentsOptions{}
	}

	var resp struct {
		Documents  []Document `json:"documents"`
		TotalCount int        `json:"total_count"`
		Limit      int        `json:"limit"`
		Offset     int        `json:"offset"`
	}

	_, err := s.client.get(ctx, "/documents", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Documents, computedPagination(resp.TotalCount, resp.Limit, resp.Offset, len(resp.Documents)), nil
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

// Update updates a document (requires write:documents scope). Workers use PUT.
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
