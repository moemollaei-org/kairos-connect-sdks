import { HttpClient } from '../http';
import { normalizePaginated, normalizeSingle } from '../normalize';
import type {
  Goal,
  CreateGoalInput,
  UpdateGoalInput,
  Task,
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  ListGoalsOptions,
  ListTasksOptions,
  ListOptions,
  PaginatedResponse,
} from '../types';

export class GoalsResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListGoalsOptions): Promise<PaginatedResponse<Goal>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.status) params.status = options.status;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    // Worker returns: { goals: [...], count, total, hasMore, limit, offset }
    const raw = await this.http.get<Record<string, unknown>>('/goals', params);
    return normalizePaginated<Goal>(raw, 'goals', limit, offset);
  }

  async get(id: string): Promise<Goal> {
    // Worker returns: { goal: {...} }
    const raw = await this.http.get<Record<string, unknown>>(`/goals/${id}`);
    return normalizeSingle<Goal>(raw, 'goal');
  }

  async create(input: CreateGoalInput): Promise<Goal> {
    // Worker returns: { goal: {...} }
    const raw = await this.http.post<Record<string, unknown>>('/goals', input);
    return normalizeSingle<Goal>(raw, 'goal');
  }

  async update(id: string, input: UpdateGoalInput): Promise<Goal> {
    // Worker returns: { goal: {...} }
    const raw = await this.http.patch<Record<string, unknown>>(`/goals/${id}`, input);
    return normalizeSingle<Goal>(raw, 'goal');
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/goals/${id}`);
  }

  // ─── Tasks under a goal ──────────────────────────────────────────────

  /** List tasks associated with a goal (requires read:tasks scope) */
  async listTasks(goalId: string, options?: ListTasksOptions): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.status) params.status = options.status;
      if (options.priority) params.priority = options.priority;
      if (options.assigned_to) params.assigned_to = options.assigned_to;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }
    const raw = await this.http.get<Record<string, unknown>>(`/goals/${goalId}/tasks`, params);
    return normalizePaginated<Task>(raw, 'tasks', limit, offset);
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a goal (requires read:comments scope) */
  async listComments(goalId: string, options?: ListOptions): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    const raw = await this.http.get<Record<string, unknown>>(`/goals/${goalId}/comments`, params);
    return normalizePaginated<Comment>(raw, 'comments', limit, offset);
  }

  /** Add a comment to a goal (requires write:comments scope) */
  async addComment(goalId: string, input: CreateCommentInput): Promise<Comment> {
    const raw = await this.http.post<Record<string, unknown>>(
      `/goals/${goalId}/comments`,
      input,
    );
    return normalizeSingle<Comment>(raw, 'comment');
  }

  /** Update a comment (requires write:comments scope) */
  async updateComment(commentId: string, input: UpdateCommentInput): Promise<Comment> {
    const raw = await this.http.patch<Record<string, unknown>>(
      `/comments/${commentId}`,
      input,
    );
    return normalizeSingle<Comment>(raw, 'comment');
  }

  /** Delete a comment (requires write:comments scope) */
  async deleteComment(commentId: string): Promise<void> {
    await this.http.delete(`/comments/${commentId}`);
  }
}
