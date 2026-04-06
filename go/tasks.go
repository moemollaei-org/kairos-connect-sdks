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

// ─── Assignees ───────────────────────────────────────────────────────────────

// ListAssignees returns all assignees for a task.
func (s *TasksService) ListAssignees(ctx context.Context, taskID string) ([]TaskAssignee, error) {
	var resp struct {
		Data []TaskAssignee `json:"data"`
	}

	_, err := s.client.get(ctx, "/tasks/"+taskID+"/assignees", nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// AddAssignee adds a user as an assignee to a task.
func (s *TasksService) AddAssignee(ctx context.Context, taskID, userID string) (*TaskAssignee, error) {
	input := struct {
		UserID string `json:"user_id"`
	}{UserID: userID}

	var resp struct {
		Data *TaskAssignee `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/assignees", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// RemoveAssignee removes a user from a task's assignees.
func (s *TasksService) RemoveAssignee(ctx context.Context, taskID, userID string) error {
	_, err := s.client.delete(ctx, "/tasks/"+taskID+"/assignees/"+userID, nil)
	return err
}

// ─── Labels ──────────────────────────────────────────────────────────────────

// ListLabels returns all labels on a task.
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

// AddLabel adds a label to a task.
func (s *TasksService) AddLabel(ctx context.Context, taskID, labelID string) (*TaskLabel, error) {
	input := struct {
		LabelID string `json:"label_id"`
	}{LabelID: labelID}

	var resp struct {
		Data *TaskLabel `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/labels", input, &resp)
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

// ─── Subtasks ─────────────────────────────────────────────────────────────────

// ListSubtasks returns immediate subtasks of a task.
func (s *TasksService) ListSubtasks(ctx context.Context, taskID string, opts *ListOptions) ([]Task, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Task     `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/tasks/"+taskID+"/subtasks", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// CreateSubtask creates a subtask under a parent task.
func (s *TasksService) CreateSubtask(ctx context.Context, taskID string, input CreateTaskInput) (*Task, error) {
	var resp struct {
		Data *Task `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/subtasks", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// ─── Dependencies ─────────────────────────────────────────────────────────────

// ListDependencies returns all dependencies for a task.
func (s *TasksService) ListDependencies(ctx context.Context, taskID string) ([]TaskDependency, error) {
	var resp struct {
		Data []TaskDependency `json:"data"`
	}

	_, err := s.client.get(ctx, "/tasks/"+taskID+"/dependencies", nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// AddDependency adds a dependency to a task.
func (s *TasksService) AddDependency(ctx context.Context, taskID, dependsOnTaskID, dependencyType string) (*TaskDependency, error) {
	input := struct {
		DependsOnTaskID string `json:"depends_on_task_id"`
		DependencyType  string `json:"dependency_type"`
	}{
		DependsOnTaskID: dependsOnTaskID,
		DependencyType:  dependencyType,
	}

	var resp struct {
		Data *TaskDependency `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/dependencies", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// RemoveDependency removes a dependency from a task.
func (s *TasksService) RemoveDependency(ctx context.Context, taskID, dependencyID string) error {
	_, err := s.client.delete(ctx, "/tasks/"+taskID+"/dependencies/"+dependencyID, nil)
	return err
}

// ─── Comments ─────────────────────────────────────────────────────────────────

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
func (s *TasksService) AddComment(ctx context.Context, taskID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.post(ctx, "/tasks/"+taskID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// UpdateComment updates a comment.
func (s *TasksService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.patch(ctx, "/comments/"+commentID, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// DeleteComment deletes a comment.
func (s *TasksService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
