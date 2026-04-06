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

// ListTasks returns tasks for a goal.
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
