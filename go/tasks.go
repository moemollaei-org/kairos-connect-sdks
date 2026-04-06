package kairos

import "context"

// TasksService provides task operations.
type TasksService struct {
	client *Client
}

// List returns a paginated list of tasks.
// Workers return: { tasks: [...], count, total, hasMore, limit, offset }
func (s *TasksService) List(ctx context.Context, opts *ListTasksOptions) ([]Task, *Pagination, error) {
	if opts == nil {
		opts = &ListTasksOptions{}
	}

	var resp struct {
		Tasks   []Task `json:"tasks"`
		Count   int    `json:"count"`
		Total   int    `json:"total"`
		HasMore bool   `json:"hasMore"`
		Limit   int    `json:"limit"`
		Offset  int    `json:"offset"`
	}

	_, err := s.client.get(ctx, "/tasks", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Tasks, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// Get returns a single task by ID.
// Workers return: { task: {...}, labels: [...] }
func (s *TasksService) Get(ctx context.Context, id string) (*Task, error) {
	var resp struct {
		Task *Task `json:"task"`
	}

	_, err := s.client.get(ctx, "/tasks/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Task, nil
}

// Create creates a new task.
// Workers return: { task: {...} }
func (s *TasksService) Create(ctx context.Context, input CreateTaskInput) (*Task, error) {
	var resp struct {
		Task *Task `json:"task"`
	}

	_, err := s.client.post(ctx, "/tasks", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Task, nil
}

// Update updates a task. Workers use PUT (not PATCH).
// Workers return: { task: {...} }
func (s *TasksService) Update(ctx context.Context, id string, input UpdateTaskInput) (*Task, error) {
	var resp struct {
		Task *Task `json:"task"`
	}

	_, err := s.client.put(ctx, "/tasks/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Task, nil
}

// Delete deletes a task.
func (s *TasksService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, "/tasks/"+id, nil)
	return err
}

// ─── Labels ──────────────────────────────────────────────────────────────────

// ListLabels returns all labels on a task.
// Workers return: { data: [...] }
func (s *TasksService) ListLabels(ctx context.Context, taskID string) ([]TaskLabel, error) {
	var resp struct {
		Data []TaskLabel `json:"data"`
	}

	_, err := s.client.get(ctx, "/tasks/"+taskID+"/labels", nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// AddLabel adds a label to a task (POST /tasks/:id/labels/:labelId).
func (s *TasksService) AddLabel(ctx context.Context, taskID, labelID string) (*TaskLabel, error) {
	var resp struct {
		Data *TaskLabel `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/labels/"+labelID, struct{}{}, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// RemoveLabel removes a label from a task.
func (s *TasksService) RemoveLabel(ctx context.Context, taskID, labelID string) error {
	_, err := s.client.delete(ctx, "/tasks/"+taskID+"/labels/"+labelID, nil)
	return err
}

// ─── Comments ─────────────────────────────────────────────────────────────────

// ListComments returns comments for a task.
// Workers return: { comments: [...], count, total, has_more }
func (s *TasksService) ListComments(ctx context.Context, taskID string, opts *ListOptions) ([]Comment, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Comments []Comment `json:"comments"`
		Total    interface{} `json:"total"`
		HasMore  bool      `json:"has_more"`
		Limit    int       `json:"limit"`
		Offset   int       `json:"offset"`
	}

	_, err := s.client.get(ctx, "/tasks/"+taskID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	// total may be a string or int
	total := 0
	switch v := resp.Total.(type) {
	case float64:
		total = int(v)
	case string:
		// ignore parse errors
	case nil:
	default:
		_ = v
	}

	return resp.Comments, nativePagination(total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// AddComment adds a comment to a task.
func (s *TasksService) AddComment(ctx context.Context, taskID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// UpdateComment updates a comment. Workers use PUT.
func (s *TasksService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.put(ctx, "/comments/"+commentID, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// DeleteComment deletes a comment.
func (s *TasksService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
