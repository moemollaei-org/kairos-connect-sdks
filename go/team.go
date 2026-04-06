package kairos

import "context"

// TeamService provides team operations.
type TeamService struct {
	client *Client
}

// Get returns the current team.
func (s *TeamService) Get(ctx context.Context) (*Team, error) {
	var resp struct {
		Data *Team `json:"data"`
	}

	_, err := s.client.get(ctx, "/team", nil, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Data, nil
}

// ListMembers returns a paginated list of team members.
func (s *TeamService) ListMembers(ctx context.Context, opts *ListOptions) ([]TeamMember, *Pagination, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Data       []TeamMember `json:"data"`
		Pagination Pagination   `json:"pagination"`
	}

	_, err := s.client.get(ctx, "/team/members", opts, &resp)
	if err != nil {
		return nil, nil, err
	}

	return resp.Data, &resp.Pagination, nil
}
