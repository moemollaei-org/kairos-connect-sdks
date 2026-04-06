package kairos

import "context"

// FormsService provides form instance operations.
// The underlying Kairos worker exposes forms as "instances" at
// /api/v1/forms/instances. The gateway routes /v1/forms/instances/*
// to the FORMS worker, so this service uses /forms/instances as its base path.
type FormsService struct {
	client *Client
}

const formsBase = "/forms/instances"

// List returns a paginated list of form instances (requires read:forms scope).
// Workers return: { instances: [...], count, total, has_more }
// team_id is injected automatically by the gateway proxy from the API key.
func (s *FormsService) List(ctx context.Context, opts *ListOptions) ([]Form, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Instances []Form `json:"instances"`
		Total     int    `json:"total"`
		Count     int    `json:"count"`
		HasMore   bool   `json:"has_more"`
		Limit     int    `json:"limit"`
		Offset    int    `json:"offset"`
	}

	_, err := s.client.get(ctx, formsBase, opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	total := resp.Total
	if total == 0 {
		total = resp.Count
	}
	return resp.Instances, nativePagination(total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// Get returns a single form instance by ID (requires read:forms scope).
// Workers return: { instance: {...} }
func (s *FormsService) Get(ctx context.Context, id string) (*Form, error) {
	var resp struct {
		Instance *Form `json:"instance"`
	}

	_, err := s.client.get(ctx, formsBase+"/"+id, nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Instance, nil
}

// Create creates a new form instance (requires write:forms scope).
// Workers return: { instance: {...} }
func (s *FormsService) Create(ctx context.Context, input CreateFormInput) (*Form, error) {
	var resp struct {
		Instance *Form `json:"instance"`
	}

	_, err := s.client.post(ctx, formsBase, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Instance, nil
}

// Update updates a form instance (requires write:forms scope).
// Workers return: { instance: {...} }
func (s *FormsService) Update(ctx context.Context, id string, input UpdateFormInput) (*Form, error) {
	var resp struct {
		Instance *Form `json:"instance"`
	}

	_, err := s.client.patch(ctx, formsBase+"/"+id, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Instance, nil
}

// Delete deletes a form instance (requires write:forms scope).
func (s *FormsService) Delete(ctx context.Context, id string) error {
	_, err := s.client.delete(ctx, formsBase+"/"+id, nil)
	return err
}

// ListSubmissions returns records (submissions) for a form instance (requires read:forms scope).
func (s *FormsService) ListSubmissions(ctx context.Context, formID string, opts *ListOptions) ([]FormSubmission, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Records []FormSubmission `json:"records"`
		Total   int              `json:"total"`
		HasMore bool             `json:"has_more"`
		Limit   int              `json:"limit"`
		Offset  int              `json:"offset"`
	}

	_, err := s.client.get(ctx, formsBase+"/"+formID+"/records", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Records, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// Submit submits a record for a form instance (requires write:forms scope).
func (s *FormsService) Submit(ctx context.Context, formID string, data map[string]interface{}) (*FormSubmission, error) {
	input := struct {
		Data map[string]interface{} `json:"data"`
	}{Data: data}

	var resp struct {
		Record *FormSubmission `json:"record"`
	}

	_, err := s.client.post(ctx, formsBase+"/"+formID+"/records", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Record, nil
}

// ListComments returns comments on a form (requires read:comments scope).
func (s *FormsService) ListComments(ctx context.Context, formID string, opts *ListOptions) ([]Comment, *Pagination, error) {
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

	_, err := s.client.get(ctx, "/forms/"+formID+"/comments", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Comments, nativePagination(resp.Total, resp.Limit, resp.Offset, resp.HasMore), nil
}

// AddComment adds a comment to a form (requires write:comments scope).
func (s *FormsService) AddComment(ctx context.Context, formID string, input CreateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.post(ctx, "/forms/"+formID+"/comments", input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// UpdateComment updates a comment (requires write:comments scope).
func (s *FormsService) UpdateComment(ctx context.Context, commentID string, input UpdateCommentInput) (*Comment, error) {
	var resp struct {
		Comment *Comment `json:"comment"`
	}

	_, err := s.client.patch(ctx, "/comments/"+commentID, input, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Comment, nil
}

// DeleteComment deletes a comment (requires write:comments scope).
func (s *FormsService) DeleteComment(ctx context.Context, commentID string) error {
	_, err := s.client.delete(ctx, "/comments/"+commentID, nil)
	return err
}
