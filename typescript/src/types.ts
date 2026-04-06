// Task types
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
  assigned_to: string | null;
  estimated_hours: number | null;
  actual_hours: number | null;
  due_date: string | null;
  completed_at: string | null;
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
}

export type UpdateTaskInput = Partial<CreateTaskInput>;

// Goal types
export interface Goal {
  id: string;
  team_id: string;
  title: string;
  description: string | null;
  status: 'active' | 'completed' | 'archived';
  progress: number;
  due_date: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalInput {
  title: string;
  description?: string;
  due_date?: string;
}

export interface UpdateGoalInput extends Partial<CreateGoalInput> {
  status?: Goal['status'];
}

// Comment types
export interface Comment {
  id: string;
  task_id: string;
  team_id: string;
  content: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface CreateCommentInput {
  content: string;
}

// Team types
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

// Document types
export interface Document {
  id: string;
  team_id: string;
  title: string;
  content: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

// Pagination types
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

// List options
export interface ListTasksOptions {
  status?: Task['status'];
  priority?: Task['priority'];
  assigned_to?: string;
  goal_id?: string;
  limit?: number;
  offset?: number;
  search?: string;
}

export interface ListGoalsOptions {
  status?: Goal['status'];
  limit?: number;
  offset?: number;
}

export interface ListOptions {
  limit?: number;
  offset?: number;
}

// Me response
export interface MeResponse {
  team_id: string;
  scopes: string[];
  rate_limit_per_minute: number;
  rate_limit_per_hour: number;
}

// Configuration
export interface KairosConfig {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
  maxRetries?: number;
}

// Rate limit info
export interface RateLimitInfo {
  limitPerMinute: number;
  remainingPerMinute: number;
  limitPerHour: number;
  remainingPerHour: number;
  resetAt: number;
}
