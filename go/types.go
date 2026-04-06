package kairos

import "time"

// ─── Task types ──────────────────────────────────────────────────────────────

// Task represents a Kairos task.
type Task struct {
	ID             string     `json:"id"`
	TeamID         string     `json:"team_id"`
	GoalID         *string    `json:"goal_id"`
	ParentTaskID   *string    `json:"parent_task_id"`
	Title          string     `json:"title"`
	Description    *string    `json:"description"`
	Type           string     `json:"type"`
	Status         string     `json:"status"`
	Priority       string     `json:"priority"`
	AssignedTo     *string    `json:"assigned_to"`
	EstimatedHours *float64   `json:"estimated_hours"`
	ActualHours    *float64   `json:"actual_hours"`
	DueDate        *string    `json:"due_date"`
	StartDate      *string    `json:"start_date"`
	CompletedAt    *time.Time `json:"completed_at"`
	OrderIndex     int        `json:"order_index"`
	IsRecurring    bool       `json:"is_recurring"`
	RecurrenceRule *string    `json:"recurrence_rule"`
	CreatedBy      string     `json:"created_by"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      time.Time  `json:"updated_at"`
}

// CreateTaskInput is input for creating a task.
type CreateTaskInput struct {
	Title          string   `json:"title"`
	Description    *string  `json:"description,omitempty"`
	Type           *string  `json:"type,omitempty"`
	Status         *string  `json:"status,omitempty"`
	Priority       *string  `json:"priority,omitempty"`
	GoalID         *string  `json:"goal_id,omitempty"`
	ParentTaskID   *string  `json:"parent_task_id,omitempty"`
	AssignedTo     *string  `json:"assigned_to,omitempty"`
	EstimatedHours *float64 `json:"estimated_hours,omitempty"`
	DueDate        *string  `json:"due_date,omitempty"`
	StartDate      *string  `json:"start_date,omitempty"`
}

// UpdateTaskInput is input for updating a task (all fields optional).
type UpdateTaskInput struct {
	Title          *string  `json:"title,omitempty"`
	Description    *string  `json:"description,omitempty"`
	Type           *string  `json:"type,omitempty"`
	Status         *string  `json:"status,omitempty"`
	Priority       *string  `json:"priority,omitempty"`
	AssignedTo     *string  `json:"assigned_to,omitempty"`
	EstimatedHours *float64 `json:"estimated_hours,omitempty"`
	DueDate        *string  `json:"due_date,omitempty"`
	StartDate      *string  `json:"start_date,omitempty"`
}

// TaskAssignee represents a user assigned to a task (from task_assignees table).
type TaskAssignee struct {
	TaskID     string    `json:"task_id"`
	UserID     string    `json:"user_id"`
	AssignedBy string    `json:"assigned_by"`
	AssignedAt time.Time `json:"assigned_at"`
}

// TaskLabel represents a label applied to a task (from task_labels table).
type TaskLabel struct {
	TaskID  string    `json:"task_id"`
	LabelID string    `json:"label_id"`
	AddedBy string    `json:"added_by"`
	AddedAt time.Time `json:"added_at"`
}

// TaskDependency represents a dependency between tasks.
type TaskDependency struct {
	ID               string    `json:"id"`
	TaskID           string    `json:"task_id"`
	DependsOnTaskID  string    `json:"depends_on_task_id"`
	DependencyType   string    `json:"dependency_type"` // blocks, blocked_by, relates_to, duplicates
	CreatedBy        string    `json:"created_by"`
	CreatedAt        time.Time `json:"created_at"`
}

// ─── Goal types ───────────────────────────────────────────────────────────────

// Goal represents a Kairos goal.
type Goal struct {
	ID          string    `json:"id"`
	TeamID      string    `json:"team_id"`
	Title       string    `json:"title"`
	Description *string   `json:"description"`
	Status      string    `json:"status"`
	Progress    float64   `json:"progress"`
	DueDate     *string   `json:"due_date"`
	StartDate   *string   `json:"start_date"`
	OwnerID     *string   `json:"owner_id"`
	CreatedBy   string    `json:"created_by"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// CreateGoalInput is input for creating a goal.
type CreateGoalInput struct {
	Title       string  `json:"title"`
	Description *string `json:"description,omitempty"`
	DueDate     *string `json:"due_date,omitempty"`
	StartDate   *string `json:"start_date,omitempty"`
	OwnerID     *string `json:"owner_id,omitempty"`
}

// UpdateGoalInput is input for updating a goal.
type UpdateGoalInput struct {
	Title       *string  `json:"title,omitempty"`
	Description *string  `json:"description,omitempty"`
	Status      *string  `json:"status,omitempty"`
	Progress    *float64 `json:"progress,omitempty"`
	DueDate     *string  `json:"due_date,omitempty"`
	StartDate   *string  `json:"start_date,omitempty"`
	OwnerID     *string  `json:"owner_id,omitempty"`
}

// ─── Comment types ────────────────────────────────────────────────────────────

// Comment represents a comment on any entity (task, goal, document, whiteboard, or form).
type Comment struct {
	ID              string     `json:"id"`
	TeamID          string     `json:"team_id"`
	EntityType      *string    `json:"entity_type"`
	EntityID        *string    `json:"entity_id"`
	TaskID          *string    `json:"task_id"`
	GoalID          *string    `json:"goal_id"`
	ParentCommentID *string    `json:"parent_comment_id"`
	Content         string     `json:"content"`
	CreatedBy       string     `json:"created_by"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

// CreateCommentInput is input for creating a comment.
type CreateCommentInput struct {
	Content         string  `json:"content"`
	ParentCommentID *string `json:"parent_comment_id,omitempty"`
}

// UpdateCommentInput is input for updating a comment.
type UpdateCommentInput struct {
	Content string `json:"content"`
}

// ─── Document types ───────────────────────────────────────────────────────────

// Document represents a Kairos document (Notion-like rich text page or database).
type Document struct {
	ID           string                 `json:"id"`
	TeamID       string                 `json:"team_id"`
	TeamspaceID  *string                `json:"teamspace_id"`
	ParentID     *string                `json:"parent_id"`
	Title        string                 `json:"title"`
	Content      map[string]interface{} `json:"content"`
	Type         string                 `json:"type"`
	Icon         *string                `json:"icon"`
	CoverImage   *string                `json:"cover_image"`
	IsPublic     bool                   `json:"is_public"`
	WordCount    int                    `json:"word_count"`
	CreatedBy    string                 `json:"created_by"`
	LastEditedBy *string                `json:"last_edited_by"`
	CreatedAt    time.Time              `json:"created_at"`
	UpdatedAt    time.Time              `json:"updated_at"`
}

// CreateDocumentInput is input for creating a document.
type CreateDocumentInput struct {
	Title       string                 `json:"title"`
	Content     map[string]interface{} `json:"content,omitempty"`
	TeamspaceID *string                `json:"teamspace_id,omitempty"`
	ParentID    *string                `json:"parent_id,omitempty"`
	Type        *string                `json:"type,omitempty"`
	Icon        *string                `json:"icon,omitempty"`
}

// UpdateDocumentInput is input for updating a document.
type UpdateDocumentInput struct {
	Title    *string                `json:"title,omitempty"`
	Content  map[string]interface{} `json:"content,omitempty"`
	Icon     *string                `json:"icon,omitempty"`
	ParentID *string                `json:"parent_id,omitempty"`
}

// ─── Whiteboard types ─────────────────────────────────────────────────────────

// Whiteboard represents a Kairos whiteboard.
type Whiteboard struct {
	ID           string                 `json:"id"`
	TeamID       string                 `json:"team_id"`
	Title        string                 `json:"title"`
	Description  *string                `json:"description"`
	ThumbnailURL *string                `json:"thumbnail_url"`
	Content      map[string]interface{} `json:"content"`
	IsPublic     bool                   `json:"is_public"`
	CreatedBy    string                 `json:"created_by"`
	CreatedAt    time.Time              `json:"created_at"`
	UpdatedAt    time.Time              `json:"updated_at"`
}

// CreateWhiteboardInput is input for creating a whiteboard.
type CreateWhiteboardInput struct {
	Title       string                 `json:"title"`
	Description *string                `json:"description,omitempty"`
	Content     map[string]interface{} `json:"content,omitempty"`
	IsPublic    *bool                  `json:"is_public,omitempty"`
}

// UpdateWhiteboardInput is input for updating a whiteboard.
type UpdateWhiteboardInput struct {
	Title       *string                `json:"title,omitempty"`
	Description *string                `json:"description,omitempty"`
	Content     map[string]interface{} `json:"content,omitempty"`
	IsPublic    *bool                  `json:"is_public,omitempty"`
}

// ─── Form types ───────────────────────────────────────────────────────────────

// FormField defines a single field in a form.
type FormField struct {
	ID          string   `json:"id"`
	Type        string   `json:"type"` // text, email, phone, number, select, multiselect, checkbox, date, textarea
	Label       string   `json:"label"`
	Placeholder *string  `json:"placeholder,omitempty"`
	Required    bool     `json:"required"`
	Options     []string `json:"options,omitempty"`
}

// Form represents a Kairos form (crm_form_configs table).
type Form struct {
	ID              string                 `json:"id"`
	TeamID          string                 `json:"team_id"`
	Name            string                 `json:"name"`
	Description     *string                `json:"description"`
	Fields          []FormField            `json:"fields"`
	Settings        map[string]interface{} `json:"settings"`
	IsActive        bool                   `json:"is_active"`
	SubmissionCount int                    `json:"submission_count"`
	CreatedBy       string                 `json:"created_by"`
	CreatedAt       time.Time              `json:"created_at"`
	UpdatedAt       time.Time              `json:"updated_at"`
}

// CreateFormInput is input for creating a form.
type CreateFormInput struct {
	Name        string                 `json:"name"`
	Description *string                `json:"description,omitempty"`
	Fields      []FormField            `json:"fields,omitempty"`
	Settings    map[string]interface{} `json:"settings,omitempty"`
	IsActive    *bool                  `json:"is_active,omitempty"`
}

// UpdateFormInput is input for updating a form.
type UpdateFormInput struct {
	Name        *string                `json:"name,omitempty"`
	Description *string                `json:"description,omitempty"`
	Fields      []FormField            `json:"fields,omitempty"`
	Settings    map[string]interface{} `json:"settings,omitempty"`
	IsActive    *bool                  `json:"is_active,omitempty"`
}

// FormSubmission represents a submitted form response (crm_form_submissions table).
type FormSubmission struct {
	ID             string                 `json:"id"`
	FormID         string                 `json:"form_id"`
	TeamID         string                 `json:"team_id"`
	Data           map[string]interface{} `json:"data"`
	SubmitterEmail *string                `json:"submitter_email"`
	SubmitterName  *string                `json:"submitter_name"`
	IPAddress      *string                `json:"ip_address"`
	SubmittedAt    time.Time              `json:"submitted_at"`
}

// ─── Team types ───────────────────────────────────────────────────────────────

// Team represents a Kairos team.
type Team struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Slug        string    `json:"slug"`
	Description *string   `json:"description"`
	AvatarURL   *string   `json:"avatar_url"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// TeamMember represents a member of a team.
type TeamMember struct {
	UserID    string    `json:"user_id"`
	Email     string    `json:"email"`
	Name      *string   `json:"name"`
	AvatarURL *string   `json:"avatar_url"`
	Role      string    `json:"role"`
	JoinedAt  time.Time `json:"joined_at"`
}

// ─── Pagination / options ─────────────────────────────────────────────────────

// Pagination is returned for list responses.
type Pagination struct {
	Page    int  `json:"page"`
	Limit   int  `json:"limit"`
	Total   int  `json:"total"`
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
	Status       string `url:"status,omitempty"`
	Priority     string `url:"priority,omitempty"`
	AssignedTo   string `url:"assigned_to,omitempty"`
	GoalID       string `url:"goal_id,omitempty"`
	ParentTaskID string `url:"parent_task_id,omitempty"`
	Type         string `url:"type,omitempty"`
	Search       string `url:"search,omitempty"`
}

// ListDocumentsOptions has document-specific filters.
type ListDocumentsOptions struct {
	ListOptions
	TeamspaceID string `url:"teamspace_id,omitempty"`
	ParentID    string `url:"parent_id,omitempty"`
	Type        string `url:"type,omitempty"`
	Search      string `url:"search,omitempty"`
}

// ─── Auth / config ────────────────────────────────────────────────────────────

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
