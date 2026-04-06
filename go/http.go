package kairos

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strconv"
	"time"
)

// do executes an HTTP request, handles retries on 429, and decodes the response.
func (c *Client) do(ctx context.Context, method, path string, body interface{}, out interface{}) (*RateLimit, error) {
	var reqBody io.Reader
	if body != nil {
		jsonBody, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("kairos: failed to marshal request body: %w", err)
		}
		reqBody = bytes.NewReader(jsonBody)
	}

	fullURL := c.baseURL + path
	req, err := http.NewRequestWithContext(ctx, method, fullURL, reqBody)
	if err != nil {
		return nil, fmt.Errorf("kairos: failed to create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+c.apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "kairos-sdk-go/"+Version)

	var lastErr error
	for attempt := 0; attempt <= c.maxRetries; attempt++ {
		resp, err := c.httpClient.Do(req)
		if err != nil {
			lastErr = fmt.Errorf("kairos: request failed: %w", err)
			continue
		}

		rateLimit := parseRateLimit(resp)

		// Handle 429 Too Many Requests with retry
		if resp.StatusCode == http.StatusTooManyRequests && attempt < c.maxRetries {
			retryAfter := parseRetryAfter(resp)
			select {
			case <-time.After(retryAfter):
				// Retry
				if reqBody != nil {
					// Reset body for retry
					jsonBody, _ := json.Marshal(body)
					req.Body = io.NopCloser(bytes.NewReader(jsonBody))
				}
				resp.Body.Close()
				continue
			case <-ctx.Done():
				resp.Body.Close()
				return rateLimit, ctx.Err()
			}
		}

		respBody, err := io.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			return rateLimit, fmt.Errorf("kairos: failed to read response body: %w", err)
		}

		// Handle error responses
		if resp.StatusCode < 200 || resp.StatusCode >= 300 {
			var errResp struct {
				Error struct {
					Code      string `json:"code"`
					Message   string `json:"message"`
					RequestID string `json:"request_id"`
				} `json:"error"`
			}
			json.Unmarshal(respBody, &errResp)

			return rateLimit, &KairosError{
				Code:       errResp.Error.Code,
				Message:    errResp.Error.Message,
				StatusCode: resp.StatusCode,
				RequestID:  errResp.Error.RequestID,
			}
		}

		// Decode success response
		if out != nil {
			if err := json.Unmarshal(respBody, out); err != nil {
				return rateLimit, fmt.Errorf("kairos: failed to decode response: %w", err)
			}
		}

		return rateLimit, nil
	}

	return nil, lastErr
}

// get executes a GET request with optional query parameters.
func (c *Client) get(ctx context.Context, path string, query interface{}, out interface{}) (*RateLimit, error) {
	if query != nil {
		queryStr := encodeQueryParams(query)
		if queryStr != "" {
			path = path + "?" + queryStr
		}
	}
	return c.do(ctx, http.MethodGet, path, nil, out)
}

// post executes a POST request.
func (c *Client) post(ctx context.Context, path string, body interface{}, out interface{}) (*RateLimit, error) {
	return c.do(ctx, http.MethodPost, path, body, out)
}

// patch executes a PATCH request.
func (c *Client) patch(ctx context.Context, path string, body interface{}, out interface{}) (*RateLimit, error) {
	return c.do(ctx, http.MethodPatch, path, body, out)
}

// delete executes a DELETE request.
func (c *Client) delete(ctx context.Context, path string, out interface{}) (*RateLimit, error) {
	return c.do(ctx, http.MethodDelete, path, nil, out)
}

// encodeQueryParams converts a struct to URL query parameters.
func encodeQueryParams(v interface{}) string {
	if v == nil {
		return ""
	}

	// Handle ListOptions
	if opts, ok := v.(*ListOptions); ok {
		values := url.Values{}
		if opts.Limit > 0 {
			values.Set("limit", strconv.Itoa(opts.Limit))
		}
		if opts.Offset > 0 {
			values.Set("offset", strconv.Itoa(opts.Offset))
		}
		return values.Encode()
	}

	// Handle ListTasksOptions
	if opts, ok := v.(*ListTasksOptions); ok {
		values := url.Values{}
		if opts.Limit > 0 {
			values.Set("limit", strconv.Itoa(opts.Limit))
		}
		if opts.Offset > 0 {
			values.Set("offset", strconv.Itoa(opts.Offset))
		}
		if opts.Status != "" {
			values.Set("status", opts.Status)
		}
		if opts.Priority != "" {
			values.Set("priority", opts.Priority)
		}
		if opts.AssignedTo != "" {
			values.Set("assigned_to", opts.AssignedTo)
		}
		if opts.GoalID != "" {
			values.Set("goal_id", opts.GoalID)
		}
		if opts.Search != "" {
			values.Set("search", opts.Search)
		}
		return values.Encode()
	}

	return ""
}

// parseRateLimit extracts rate limit info from response headers.
func parseRateLimit(resp *http.Response) *RateLimit {
	rl := &RateLimit{}
	if v := resp.Header.Get("X-RateLimit-Limit-Minute"); v != "" {
		rl.LimitMinute, _ = strconv.Atoi(v)
	}
	if v := resp.Header.Get("X-RateLimit-Remaining-Minute"); v != "" {
		rl.RemainingMinute, _ = strconv.Atoi(v)
	}
	if v := resp.Header.Get("X-RateLimit-Limit-Hour"); v != "" {
		rl.LimitHour, _ = strconv.Atoi(v)
	}
	if v := resp.Header.Get("X-RateLimit-Remaining-Hour"); v != "" {
		rl.RemainingHour, _ = strconv.Atoi(v)
	}
	if v := resp.Header.Get("X-RateLimit-Reset"); v != "" {
		rl.Reset, _ = strconv.ParseInt(v, 10, 64)
	}
	return rl
}

// parseRetryAfter extracts the Retry-After header.
func parseRetryAfter(resp *http.Response) time.Duration {
	if retryAfter := resp.Header.Get("Retry-After"); retryAfter != "" {
		if seconds, err := strconv.Atoi(retryAfter); err == nil {
			return time.Duration(seconds) * time.Second
		}
	}
	return time.Second // Default to 1 second
}
