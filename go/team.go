package kairos

import (
	"context"
	"fmt"
)

// TeamService provides team operations.
type TeamService struct {
	client *Client
}

// Get returns the current API key's team.
// Workers return { teams: [...] } — returns the first team.
func (s *TeamService) Get(ctx context.Context) (*Team, error) {
	var resp struct {
		Teams []Team `json:"teams"`
	}

	_, err := s.client.get(ctx, "/teams", nil, &resp)
	if err != nil {
		return nil, err
	}

	if len(resp.Teams) == 0 {
		return nil, fmt.Errorf("kairos: no team found for this API key")
	}

	return &resp.Teams[0], nil
}

// ListMembers returns the members of a team by ID.
// Workers return { members: [...] }
func (s *TeamService) ListMembers(ctx context.Context, teamID string, opts *ListOptions) ([]TeamMember, error) {
	if opts == nil {
		opts = &ListOptions{}
	}

	var resp struct {
		Members []TeamMember `json:"members"`
	}

	_, err := s.client.get(ctx, "/teams/"+teamID+"/members", opts, &resp)
	if err != nil {
		return nil, err
	}

	return resp.Members, nil
}
