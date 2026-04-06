package kairos

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"time"
)

const DefaultBaseURL = "https://gateway.thekairos.app/v1"
const Version = "0.3.0"

// Client is the Kairos API client.
type Client struct {
	apiKey     string
	baseURL    string
	httpClient *http.Client
	maxRetries int
	Tasks       *TasksService
	Goals       *GoalsService
	Team        *TeamService
	Documents   *DocumentsService
	Whiteboards *WhiteboardsService
	Forms       *FormsService
}

// ClientOption is a function that configures the client.
type ClientOption func(*Client)

// WithBaseURL sets a custom base URL for the API.
func WithBaseURL(url string) ClientOption {
	return func(c *Client) {
		c.baseURL = url
	}
}

// WithHTTPClient sets a custom HTTP client.
func WithHTTPClient(client *http.Client) ClientOption {
	return func(c *Client) {
		c.httpClient = client
	}
}

// WithMaxRetries sets the maximum number of retries for failed requests.
func WithMaxRetries(n int) ClientOption {
	return func(c *Client) {
		c.maxRetries = n
	}
}

// WithTimeout sets the timeout for HTTP requests.
func WithTimeout(d time.Duration) ClientOption {
	return func(c *Client) {
		c.httpClient.Timeout = d
	}
}

// New creates a new Kairos client.
// If apiKey is empty, reads from KAIROS_API_KEY environment variable.
func New(apiKey string, opts ...ClientOption) (*Client, error) {
	if apiKey == "" {
		apiKey = os.Getenv("KAIROS_API_KEY")
	}
	if apiKey == "" {
		return nil, fmt.Errorf("kairos: api key required; set KAIROS_API_KEY or pass apiKey")
	}

	c := &Client{
		apiKey:     apiKey,
		baseURL:    DefaultBaseURL,
		httpClient: &http.Client{Timeout: 30 * time.Second},
		maxRetries: 3,
	}

	for _, opt := range opts {
		opt(c)
	}

	c.Tasks = &TasksService{client: c}
	c.Goals = &GoalsService{client: c}
	c.Team = &TeamService{client: c}
	c.Documents = &DocumentsService{client: c}
	c.Whiteboards = &WhiteboardsService{client: c}
	c.Forms = &FormsService{client: c}

	return c, nil
}

// Me validates the API key and returns team info + scopes.
func (c *Client) Me(ctx context.Context) (*MeResponse, error) {
	var resp struct {
		Data *MeResponse `json:"data"`
	}
	_, err := c.get(ctx, "/me", nil, &resp)
	if err != nil {
		return nil, err
	}
	return resp.Data, nil
}
