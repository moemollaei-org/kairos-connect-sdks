package kairos

import "fmt"

// KairosError is returned when the API returns an error response.
type KairosError struct {
	Code       string
	Message    string
	StatusCode int
	RequestID  string
}

func (e *KairosError) Error() string {
	return fmt.Sprintf("kairos: %s (status=%d, request_id=%s)", e.Message, e.StatusCode, e.RequestID)
}

// IsAuthError reports whether err is a 401 Unauthorized error.
func IsAuthError(err error) bool {
	if ke, ok := err.(*KairosError); ok {
		return ke.StatusCode == 401
	}
	return false
}

// IsForbiddenError reports whether err is a 403 Forbidden error.
func IsForbiddenError(err error) bool {
	if ke, ok := err.(*KairosError); ok {
		return ke.StatusCode == 403
	}
	return false
}

// IsNotFoundError reports whether err is a 404 Not Found error.
func IsNotFoundError(err error) bool {
	if ke, ok := err.(*KairosError); ok {
		return ke.StatusCode == 404
	}
	return false
}

// IsRateLimitError reports whether err is a 429 Too Many Requests error.
func IsRateLimitError(err error) bool {
	if ke, ok := err.(*KairosError); ok {
		return ke.StatusCode == 429
	}
	return false
}
