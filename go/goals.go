package kairos

import "context"

// GoalsService provides goal operations.
type GoalsService struct {
	client *Client
}

// List returns a paginated list of goals.
func (s *GoalsService) List(ctx context.Context, opts *ListOptions) ([]Goal, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Goal     `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/goals", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// Get returns a single goal by ID.
func (s *GoalsService) Get(ctx context.Context, id string) (*Goal, error) {
	var resp struct {
		Data *Goal `json:"data"`
	}

	_, err := s.client.get(ctx, "/goals/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Create creates a new goal.
func (s *GoalsService) Create(ctx context.Context, input CreateGoalInput) (*Goal, error) {
	var resp struct {
		Data *Goal `json:"data"`
	}

	_, err := s.client.post(ctx, "/goals", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Update updates a goal.
func (s *GoalsService) Update(ctx context.Context, id string, input UpdateGoalInput) (*Goal, error) {
	var resp struct {
		Data *Goal `json:"data"`
	}

	_, err := s.client.patch(ctx, "/goals/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Delete deletes a goal.
func (s *GoalsService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, "/goals/"+id, nil)
	return err
}

// ListTasks returns tasks associated with a goal (requires read:tasks scope).
func (s *GoalsService) ListTasks(ctx context.Context, goalID string, opts *ListTasksOptions) ([]Task, *Pagination, error) {
	if opts == nil {
		opts = &ListTasksOptions{}
	}

	var resp struct {
		Data       []Task     `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/goals/"+goalID+"/tasks", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// ListComments returns comments on a goal (requires read:comments scope).
func (s *GoalsService) ListComments(ctx context.Context, goalID string, opts *ListOptions) ([]Comment, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Comment  `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/goals/"+goalID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// AddComment adds a comment to a goal (requires write:comments scope).
func (s *GoalsService) AddComment(ctx context.Context, goalID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.post(ctx, "/goals/"+goalID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *GoalsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
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
func (s *GoalsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
