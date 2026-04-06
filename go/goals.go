package kairos

import "context"

// GoalsService provides goal operations.
type GoalsService struct {
	client *Client
}

// List returns a paginated list of goals.
// Workers return: { goals: [...], count, total, hasMore, limit, offset }
func (s *GoalsService) List(ctx context.Context, opts *ListOptions) ([]Goal, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Goals   []Goal `json:"goals"`
		Total   int    `json:"total"`
		HasMore bool   `json:"hasMore"`
		Limit   int    `json:"limit"`
		Offset  int    `json:"offset"`
	}

	_, err := s.client.get(ctx, "/goals", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Goals, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// Get returns a single goal by ID.
// Workers return: { goal: {...} }
func (s *GoalsService) Get(ctx context.Context, id string) (*Goal, error) {
	var resp struct {
		Goal *Goal `json:"goal"`
	}

	_, err := s.client.get(ctx, "/goals/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Goal, nil
}

// Create creates a new goal.
// Workers return: { goal: {...} }
func (s *GoalsService) Create(ctx context.Context, input CreateGoalInput) (*Goal, error) {
	var resp struct {
		Goal *Goal `json:"goal"`
	}

	_, err := s.client.post(ctx, "/goals", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Goal, nil
}

// Update updates a goal.
// Workers return: { goal: {...} }
func (s *GoalsService) Update(ctx context.Context, id string, input UpdateGoalInput) (*Goal, error) {
	var resp struct {
		Goal *Goal `json:"goal"`
	}

	_, err := s.client.put(ctx, "/goals/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Goal, nil
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
		Tasks   []Task `json:"tasks"`
		Total   int    `json:"total"`
		HasMore bool   `json:"hasMore"`
		Limit   int    `json:"limit"`
		Offset  int    `json:"offset"`
	}

	// Goals worker has no /:id/tasks sub-route — filter tasks by GoalID instead.
	opts.GoalID = goalID
	_, err := s.client.get(ctx, "/tasks", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Tasks, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// ListComments returns comments on a goal (requires read:comments scope).
func (s *GoalsService) ListComments(ctx context.Context, goalID string, opts *ListOptions) ([]Comment, *Pagination, error) {
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

	_, err := s.client.get(ctx, "/goals/"+goalID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Comments, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// AddComment adds a comment to a goal (requires write:comments scope).
func (s *GoalsService) AddComment(ctx context.Context, goalID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.post(ctx, "/goals/"+goalID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *GoalsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
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
func (s *GoalsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
