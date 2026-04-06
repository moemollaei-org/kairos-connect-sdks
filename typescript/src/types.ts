// ─── Task types ──────────────────────────────────────────────────────────────

export interface Task {
  id: string;
  team_id: string;
  goal_id: string | null;
  parent_task_id: string | null;
  title: string;
  description: string | null;
  type: 'task' | 'sub_task' | 'bug' | 'story' | 'epic';
  status: 'to_do' | 'in_progress' | 'in_review' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  /** Primary assignee (deprecated in favour of task_assignees; kept for compatibility) */
  assigned_to: string | null;
  estimated_hours: number | null;
  actual_hours: number | null;
  due_date: string | null;
  completed_at: string | null;
  start_date: string | null;
  order_index: number;
  is_recurring: boolean;
  recurrence_rule: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  type?: Task['type'];
  status?: Task['status'];
  priority?: Task['priority'];
  goal_id?: string;
  parent_task_id?: string;
  assigned_to?: string;
  estimated_hours?: number;
  due_date?: string;
  start_date?: string;
}

export type UpdateTaskInput = Partial<CreateTaskInput>;

/** Record from task_assignees table — multiple assignees per task */
export interface TaskAssignee {
  task_id: string;
  user_id: string;
  assigned_by: string;
  assigned_at: string;
}

export interface AddTaskAssigneeInput {
  user_id: string;
}

/** Record from task_labels table */
export interface TaskLabel {
  task_id: string;
  label_id: string;
  added_by: string;
  added_at: string;
}

export interface AddTaskLabelInput {
  label_id: string;
}

/** Record from task_dependencies table */
export interface TaskDependency {
  id: string;
  task_id: string;
  depends_on_task_id: string;
  dependency_type: 'blocks' | 'blocked_by' | 'relates_to' | 'duplicates';
  created_by: string;
  created_at: string;
}

export interface AddTaskDependencyInput {
  depends_on_task_id: string;
  dependency_type: TaskDependency['dependency_type'];
}

// ─── Goal types ───────────────────────────────────────────────────────────────

export interface Goal {
  id: string;
  team_id: string;
  title: string;
  description: string | null;
  status: 'active' | 'completed' | 'archived';
  progress: number;
  due_date: string | null;
  start_date: string | null;
  owner_id: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalInput {
  title: string;
  description?: string;
  due_date?: string;
  start_date?: string;
  owner_id?: string;
}

export interface UpdateGoalInput extends Partial<CreateGoalInput> {
  status?: Goal['status'];
  progress?: number;
}

// ─── Comment types ────────────────────────────────────────────────────────────

/**
 * A comment on any entity (task, goal, document, whiteboard, or form).
 * The entity is identified by entity_type + entity_id when the API
 * returns standalone comment resources. task_id / goal_id are kept for
 * backward compatibility when listing comments via nested routes.
 */
export interface Comment {
  id: string;
  team_id: string;
  /** The entity this comment belongs to (when using standalone /comments routes) */
  entity_type: 'task' | 'goal' | 'document' | 'whiteboard' | 'form' | null;
  entity_id: string | null;
  /** Convenience field — set when entity_type = 'task' */
  task_id: string | null;
  /** Convenience field — set when entity_type = 'goal' */
  goal_id: string | null;
  /** Parent comment for threaded replies */
  parent_comment_id: string | null;
  content: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateCommentInput {
  content: string;
  parent_comment_id?: string;
}

export interface UpdateCommentInput {
  content: string;
}

// ─── Document types ───────────────────────────────────────────────────────────

export interface Document {
  id: string;
  team_id: string;
  teamspace_id: string | null;
  parent_id: string | null;
  title: string;
  /** Prosemirror JSON content */
  content: Record<string, unknown> | null;
  type: 'document' | 'database' | 'page';
  icon: string | null;
  cover_image: string | null;
  is_public: boolean;
  word_count: number;
  created_by: string;
  last_edited_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateDocumentInput {
  title: string;
  content?: Record<string, unknown>;
  teamspace_id?: string;
  parent_id?: string;
  type?: Document['type'];
  icon?: string;
}

export type UpdateDocumentInput = Partial<CreateDocumentInput>;

// ─── Whiteboard types ─────────────────────────────────────────────────────────

export interface Whiteboard {
  id: string;
  team_id: string;
  title: string;
  description: string | null;
  thumbnail_url: string | null;
  content: Record<string, unknown> | null;
  is_public: boolean;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateWhiteboardInput {
  title: string;
  description?: string;
  content?: Record<string, unknown>;
  is_public?: boolean;
}

export type UpdateWhiteboardInput = Partial<CreateWhiteboardInput>;

// ─── Form types (CRM form configs + submissions) ──────────────────────────────

export interface Form {
  id: string;
  team_id: string;
  name: string;
  description: string | null;
  /** JSON schema of form fields */
  fields: FormField[];
  settings: Record<string, unknown>;
  is_active: boolean;
  submission_count: number;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface FormField {
  id: string;
  type: 'text' | 'email' | 'phone' | 'number' | 'select' | 'multiselect' | 'checkbox' | 'date' | 'textarea';
  label: string;
  placeholder?: string;
  required: boolean;
  options?: string[];
}

export interface CreateFormInput {
  name: string;
  description?: string;
  fields?: FormField[];
  settings?: Record<string, unknown>;
  is_active?: boolean;
}

export type UpdateFormInput = Partial<CreateFormInput>;

export interface FormSubmission {
  id: string;
  form_id: string;
  team_id: string;
  /** Field values keyed by field id */
  data: Record<string, unknown>;
  submitter_email: string | null;
  submitter_name: string | null;
  ip_address: string | null;
  submitted_at: string;
}

// ─── Team types ───────────────────────────────────────────────────────────────

export interface Team {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  avatar_url: string | null;
  created_at: string;
}

export interface TeamMember {
  user_id: string;
  email: string;
  name: string;
  avatar_url: string | null;
  role: string;
  joined_at: string;
}

// ─── Shared / pagination types ────────────────────────────────────────────────

export interface Pagination {
  page: number;
  limit: number;
  total: number;
  has_more: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

export interface SingleResponse<T> {
  data: T;
}

// ─── List / filter options ────────────────────────────────────────────────────

export interface ListTasksOptions {
  status?: Task['status'];
  priority?: Task['priority'];
  assigned_to?: string;
  goal_id?: string;
  parent_task_id?: string;
  type?: Task['type'];
  limit?: number;
  offset?: number;
  search?: string;
}

export interface ListGoalsOptions {
  status?: Goal['status'];
  limit?: number;
  offset?: number;
}

export interface ListDocumentsOptions {
  teamspace_id?: string;
  parent_id?: string;
  type?: Document['type'];
  limit?: number;
  offset?: number;
  search?: string;
}

export interface ListWhiteboardsOptions {
  limit?: number;
  offset?: number;
  search?: string;
}

export interface ListFormsOptions {
  is_active?: boolean;
  limit?: number;
  offset?: number;
}

export interface ListOptions {
  limit?: number;
  offset?: number;
}

// ─── Me / config / rate limit ─────────────────────────────────────────────────

export interface MeResponse {
  team_id: string;
  scopes: string[];
  rate_limit_per_minute: number;
  rate_limit_per_hour: number;
}

export interface KairosConfig {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
  maxRetries?: number;
}

export interface RateLimitInfo {
  limitPerMinute: number;
  remainingPerMinute: number;
  limitPerHour: number;
  remainingPerHour: number;
  resetAt: number;
}
