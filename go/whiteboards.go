package kairos

import "context"

// WhiteboardsService provides whiteboard operations.
type WhiteboardsService struct {
	client *Client
}

// List returns a paginated list of whiteboards (requires read:whiteboards scope).
func (s *WhiteboardsService) List(ctx context.Context, opts *ListOptions) ([]Whiteboard, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Whiteboard `json:"data"`
		Pagination Pagination   `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/whiteboards", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// Get returns a single whiteboard by ID (requires read:whiteboards scope).
func (s *WhiteboardsService) Get(ctx context.Context, id string) (*Whiteboard, error) {
	var resp struct {
		Data *Whiteboard `json:"data"`
	}

	_, err := s.client.get(ctx, "/whiteboards/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Create creates a new whiteboard (requires write:whiteboards scope).
func (s *WhiteboardsService) Create(ctx context.Context, input CreateWhiteboardInput) (*Whiteboard, error) {
	var resp struct {
		Data *Whiteboard `json:"data"`
	}

	_, err := s.client.post(ctx, "/whiteboards", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Update updates a whiteboard (requires write:whiteboards scope).
func (s *WhiteboardsService) Update(ctx context.Context, id string, input UpdateWhiteboardInput) (*Whiteboard, error) {
	var resp struct {
		Data *Whiteboard `json:"data"`
	}

	_, err := s.client.patch(ctx, "/whiteboards/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
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
		Data       []Comment  `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/whiteboards/"+whiteboardID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// AddComment adds a comment to a whiteboard (requires write:comments scope).
func (s *WhiteboardsService) AddComment(ctx context.Context, whiteboardID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.post(ctx, "/whiteboards/"+whiteboardID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *WhiteboardsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.patch(ctx, "/comments/"+commentID, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// DeleteComment deletes a comment (requires write:comments scope).
func (s *WhiteboardsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
