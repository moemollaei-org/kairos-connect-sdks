package kairos

import "context"

// WhiteboardsService provides whiteboard operations.
type WhiteboardsService struct {
	client *Client
}

// List returns a paginated list of whiteboards (requires read:whiteboards scope).
// Workers return: { whiteboards: [...], total_count, limit, offset }
// No hasMore field — has_more is computed from total_count vs. returned count.
func (s *WhiteboardsService) List(ctx context.Context, opts *ListOptions) ([]Whiteboard, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Whiteboards []Whiteboard `json:"whiteboards"`
		TotalCount  int          `json:"total_count"`
		Limit       int          `json:"limit"`
		Offset      int          `json:"offset"`
	}

	_, err := s.client.get(ctx, "/whiteboards", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Whiteboards, computedPagination(resp.TotalCount, resp.Limit, resp.Offset, len(resp.Whiteboards)), nil
}

// Get returns a single whiteboard by ID (requires read:whiteboards scope).
// Workers return: { whiteboard: {...} }
func (s *WhiteboardsService) Get(ctx context.Context, id string) (*Whiteboard, error) {
	var resp struct {
		Whiteboard *Whiteboard `json:"whiteboard"`
	}

	_, err := s.client.get(ctx, "/whiteboards/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Whiteboard, nil
}

// Create creates a new whiteboard (requires write:whiteboards scope).
// Workers return: { whiteboard: {...} }
func (s *WhiteboardsService) Create(ctx context.Context, input CreateWhiteboardInput) (*Whiteboard, error) {
	var resp struct {
		Whiteboard *Whiteboard `json:"whiteboard"`
	}

	_, err := s.client.post(ctx, "/whiteboards", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Whiteboard, nil
}

// Update updates a whiteboard (requires write:whiteboards scope). Workers use PUT.
// Workers return: { whiteboard: {...} }
func (s *WhiteboardsService) Update(ctx context.Context, id string, input UpdateWhiteboardInput) (*Whiteboard, error) {
	var resp struct {
		Whiteboard *Whiteboard `json:"whiteboard"`
	}

	_, err := s.client.put(ctx, "/whiteboards/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Whiteboard, nil
}

// Delete deletes a whiteboard (requires write:whiteboards scope).
func (s *WhiteboardsService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, "/whiteboards/"+id, nil)
	return err
}
