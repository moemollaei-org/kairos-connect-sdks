package kairos

import "context"

// FormsService provides form operations.
type FormsService struct {
	client *Client
}

// List returns a paginated list of forms (requires read:forms scope).
func (s *FormsService) List(ctx context.Context, opts *ListOptions) ([]Form, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Form     `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/forms", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// Get returns a single form by ID (requires read:forms scope).
func (s *FormsService) Get(ctx context.Context, id string) (*Form, error) {
	var resp struct {
		Data *Form `json:"data"`
	}

	_, err := s.client.get(ctx, "/forms/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Create creates a new form (requires write:forms scope).
func (s *FormsService) Create(ctx context.Context, input CreateFormInput) (*Form, error) {
	var resp struct {
		Data *Form `json:"data"`
	}

	_, err := s.client.post(ctx, "/forms", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Update updates a form (requires write:forms scope).
func (s *FormsService) Update(ctx context.Context, id string, input UpdateFormInput) (*Form, error) {
	var resp struct {
		Data *Form `json:"data"`
	}

	_, err := s.client.patch(ctx, "/forms/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// Delete deletes a form (requires write:forms scope).
func (s *FormsService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, "/forms/"+id, nil)
	return err
}

// ListSubmissions returns submissions for a form (requires read:forms scope).
func (s *FormsService) ListSubmissions(ctx context.Context, formID string, opts *ListOptions) ([]FormSubmission, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []FormSubmission `json:"data"`
		Pagination Pagination       `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/forms/"+formID+"/submissions", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// Submit submits a response to a form (requires write:forms scope).
func (s *FormsService) Submit(ctx context.Context, formID string, data map[string]interface{}) (*FormSubmission, error) {
	input := struct {
		Data map[string]interface{} `json:"data"`
	}{Data: data}

	var resp struct {
		Data *FormSubmission `json:"data"`
	}

	_, err := s.client.post(ctx, "/forms/"+formID+"/submissions", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// ListComments returns comments on a form (requires read:comments scope).
func (s *FormsService) ListComments(ctx context.Context, formID string, opts *ListOptions) ([]Comment, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []Comment  `json:"data"`
		Pagination Pagination `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/forms/"+formID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}

// AddComment adds a comment to a form (requires write:comments scope).
func (s *FormsService) AddComment(ctx context.Context, formID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Data *Comment `json:"data"`
	}

	_, err := s.client.post(ctx, "/forms/"+formID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *FormsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
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
func (s *FormsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
