import { HttpClient } from '../http';
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
  SingleResponse,
} from '../types';

export class GoalsResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListGoalsOptions): Promise<PaginatedResponse<Goal>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.status) params.status = options.status;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Goal>>('/goals', params);
  }

  async get(id: string): Promise<Goal> {
    const response = await this.http.get<SingleResponse<Goal>>(`/goals/${id}`);
    return response.data;
  }

  async create(input: CreateGoalInput): Promise<Goal> {
    const response = await this.http.post<SingleResponse<Goal>>('/goals', input);
    return response.data;
  }

  async update(id: string, input: UpdateGoalInput): Promise<Goal> {
    const response = await this.http.patch<SingleResponse<Goal>>(`/goals/${id}`, input);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/goals/${id}`);
  }

  // ─── Tasks under a goal ──────────────────────────────────────────────

  /** List tasks associated with a goal (requires read:tasks scope) */
  async listTasks(goalId: string, options?: ListTasksOptions): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.status) params.status = options.status;
      if (options.priority) params.priority = options.priority;
      if (options.assigned_to) params.assigned_to = options.assigned_to;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }
    return this.http.get<PaginatedResponse<Task>>(`/goals/${goalId}/tasks`, params);
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a goal (requires read:comments scope) */
  async listComments(goalId: string, options?: ListOptions): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Comment>>(`/goals/${goalId}/comments`, params);
  }

  /** Add a comment to a goal (requires write:comments scope) */
  async addComment(goalId: string, input: CreateCommentInput): Promise<Comment> {
    const response = await this.http.post<SingleResponse<Comment>>(
      `/goals/${goalId}/comments`,
      input,
    );
    return response.data;
  }

  /** Update a comment (requires write:comments scope) */
  async updateComment(commentId: string, input: UpdateCommentInput): Promise<Comment> {
    const response = await this.http.patch<SingleResponse<Comment>>(
      `/comments/${commentId}`,
      input,
    );
    return response.data;
  }

  /** Delete a comment (requires write:comments scope) */
  async deleteComment(commentId: string): Promise<void> {
    await this.http.delete(`/comments/${commentId}`);
  }
}
