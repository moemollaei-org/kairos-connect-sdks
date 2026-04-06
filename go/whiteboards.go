package kairos

import "context"

// WhiteboardsService provides whiteboard operations.
type WhiteboardsService struct {
	client *Client
}

// List returns a paginated list of whiteboards (requires read:whiteboards scope).
// Workers return: { whiteboards: [...], total_count, limit, offset }
// team_id is injected automatically by the gateway proxy from the API key.
func (s *WhiteboardsService) List(ctx context.Context, opts *ListOptions) ([]Whiteboard, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Whiteboards []Whiteboard `json:"whiteboards"`
		TotalCount  int          `json:"total_count"`
		Total       int          `json:"total"` // fallback alias
		HasMore     bool         `json:"hasMore"`
		Limit       int          `json:"limit"`
		Offset      int          `json:"offset"`
	}

	_, err := s.client.get(ctx, "/whiteboards", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	total := resp.TotalCount
	if total == 0 {
		total = resp.Total
	}
	return resp.Whiteboards, nativePagination(total, resp.Limit, resp.Offset, resp.HasMore), nil
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

// Update updates a whiteboard (requires write:whiteboards scope).
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

// ListComments returns comments on a whiteboard (requires read:comments scope).
func (s *WhiteboardsService) ListComments(ctx context.Context, whiteboardID string, opts *ListOptions) ([]Comment, *Pagination, error) {
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

	_, err := s.client.get(ctx, "/whiteboards/"+whiteboardID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Comments, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// AddComment adds a comment to a whiteboard (requires write:comments scope).
func (s *WhiteboardsService) AddComment(ctx context.Context, whiteboardID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.post(ctx, "/whiteboards/"+whiteboardID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *WhiteboardsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
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
func (s *WhiteboardsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
