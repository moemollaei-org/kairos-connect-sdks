package kairos

import "context"

// DocumentsService provides document operations.
type DocumentsService struct {
	client *Client
}

// List returns a paginated list of documents.
func (s *DocumentsService) List(ctx context.Context, opts *ListOptions) ([]Document, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Document `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/documents", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// Get returns a single document by ID.
func (s *DocumentsService) Get(ctx context.Context, id string) (*Document, error) {
	var resp struct {
		Data *Document `json:"data"`
	}

	_, err := s.client.get(ctx, "/documents/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}
