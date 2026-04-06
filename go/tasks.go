package kairos

import "context"

// TasksService provides task operations.
type TasksService struct {
	client *Client
}

// List returns a paginated list of tasks.
func (s *TasksService) List(ctx context.Context, opts *ListTasksOptions) ([]Task, *Pagination, error) {
	if opts == nil {
		opts = &ListTasksOptions{}
	}

	var resp struct {
		Data       []Task     `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/tasks", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// Get returns a single task by ID.
func (s *TasksService) Get(ctx context.Context, id string) (*Task, error) {
	var resp struct {
		Data *Task `json:"data"`
	}

	_, err := s.client.get(ctx, "/tasks/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Create creates a new task.
func (s *TasksService) Create(ctx context.Context, input CreateTaskInput) (*Task, error) {
	var resp struct {
		Data *Task `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Update updates a task.
func (s *TasksService) Update(ctx context.Context, id string, input UpdateTaskInput) (*Task, error) {
	var resp struct {
		Data *Task `json:"data"`
	}

	_, err := s.client.patch(ctx, "/tasks/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Delete deletes a task.
func (s *TasksService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, "/tasks/"+id, nil)
	return err
}

// ListComments returns comments for a task.
func (s *TasksService) ListComments(ctx context.Context, taskID string, opts *ListOptions) ([]Comment, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Comment  `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/tasks/"+taskID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// AddComment adds a comment to a task.
func (s *TasksService) AddComment(ctx context.Context, taskID string, content string) (*Comment, error) {
	input := CreateCommentInput{Content: content}

	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}
