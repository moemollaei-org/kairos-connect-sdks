package kairos

import "time"

// Task represents a Kairos task.
type Task struct {
	ID           string     `json:"id"`
	TeamID       string     `json:"team_id"`
	GoalID       *string    `json:"goal_id"`
	ParentTaskID *string    `json:"parent_task_id"`
	Title        string     `json:"title"`
	Description  *string    `json:"description"`
	Type         string     `json:"type"`
	Status       string     `json:"status"`
	Priority     string     `json:"priority"`
	AssignedTo   *string    `json:"assigned_to"`
	DueDate      *string    `json:"due_date"`
	CompletedAt  *time.Time `json:"completed_at"`
	CreatedBy    string     `json:"created_by"`
	CreatedAt    time.Time  `json:"created_at"`
	UpdatedAt    time.Time  `json:"updated_at"`
}

// CreateTaskInput is input for creating a task.
type CreateTaskInput struct {
	Title       string  `json:"title"`
	Description *string `json:"description,omitempty"`
	Type        *string `json:"type,omitempty"`
	Status      *string `json:"status,omitempty"`
	Priority    *string `json:"priority,omitempty"`
	GoalID      *string `json:"goal_id,omitempty"`
	AssignedTo  *string `json:"assigned_to,omitempty"`
	DueDate     *string `json:"due_date,omitempty"`
}

// UpdateTaskInput is input for updating a task (all fields optional).
type UpdateTaskInput struct {
	Title       *string `json:"title,omitempty"`
	Description *string `json:"description,omitempty"`
	Status      *string `json:"status,omitempty"`
	Priority    *string `json:"priority,omitempty"`
	AssignedTo  *string `json:"assigned_to,omitempty"`
	DueDate     *string `json:"due_date,omitempty"`
}

// Goal represents a Kairos goal.
type Goal struct {
	ID          string    `json:"id"`
	TeamID      string    `json:"team_id"`
	Title       string    `json:"title"`
	Description *string   `json:"description"`
	Status      string    `json:"status"`
	CreatedBy   string    `json:"created_by"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// CreateGoalInput is input for creating a goal.
type CreateGoalInput struct {
	Title       string  `json:"title"`
	Description *string `json:"description,omitempty"`
	Status      *string `json:"status,omitempty"`
}

// UpdateGoalInput is input for updating a goal.
type UpdateGoalInput struct {
	Title       *string `json:"title,omitempty"`
	Description *string `json:"description,omitempty"`
	Status      *string `json:"status,omitempty"`
}

// Comment represents a task comment.
type Comment struct {
	ID        string    `json:"id"`
	TaskID    string    `json:"task_id"`
	Content   string    `json:"content"`
	CreatedBy string    `json:"created_by"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// CreateCommentInput is input for creating a comment.
type CreateCommentInput struct {
	Content string `json:"content"`
}

// Team represents a Kairos team.
type Team struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// TeamMember represents a member of a team.
type TeamMember struct {
	ID        string    `json:"id"`
	TeamID    string    `json:"team_id"`
	Email     string    `json:"email"`
	Name      *string   `json:"name"`
	Role      string    `json:"role"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// Document represents a Kairos document.
type Document struct {
	ID        string    `json:"id"`
	TeamID    string    `json:"team_id"`
	Title     string    `json:"title"`
	Content   *string   `json:"content"`
	CreatedBy string    `json:"created_by"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// Pagination is returned for list responses.
type Pagination struct {
	Page    int `json:"page"`
	Limit   int `json:"limit"`
	Total   int `json:"total"`
	HasMore bool `json:"has_more"`
}

// ListOptions are common list options.
type ListOptions struct {
	Limit  int `url:"limit,omitempty"`
	Offset int `url:"offset,omitempty"`
}

// ListTasksOptions has task-specific filters.
type ListTasksOptions struct {
	ListOptions
	Status     string `url:"status,omitempty"`
	Priority   string `url:"priority,omitempty"`
	AssignedTo string `url:"assigned_to,omitempty"`
	GoalID     string `url:"goal_id,omitempty"`
	Search     string `url:"search,omitempty"`
}

// MeResponse is returned by Me().
type MeResponse struct {
	TeamID             string   `json:"team_id"`
	Scopes             []string `json:"scopes"`
	RateLimitPerMinute int      `json:"rate_limit_per_minute"`
	RateLimitPerHour   int      `json:"rate_limit_per_hour"`
}

// RateLimit contains rate limit info from response headers.
type RateLimit struct {
	LimitMinute     int
	RemainingMinute int
	LimitHour       int
	RemainingHour   int
	Reset           int64
}
