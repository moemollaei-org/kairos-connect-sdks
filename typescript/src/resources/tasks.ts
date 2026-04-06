import { HttpClient } from '../http';
import { normalizePaginated, normalizeSingle, normalizeList } from '../normalize';
import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  TaskLabel,
  AddTaskLabelInput,
  ListTasksOptions,
  ListOptions,
  PaginatedResponse,
} from '../types';

export class TasksResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListTasksOptions): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.status) params.status = options.status;
      if (options.priority) params.priority = options.priority;
      if (options.assigned_to) params.assigned_to = options.assigned_to;
      if (options.goal_id) params.goal_id = options.goal_id;
      if (options.parent_task_id) params.parent_task_id = options.parent_task_id;
      if (options.type) params.type = options.type;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }
    // Worker returns: { tasks: [...], count, total, hasMore, limit, offset }
    const raw = await this.http.get<Record<string, unknown>>('/tasks', params);
    return normalizePaginated<Task>(raw, 'tasks', limit, offset);
  }

  async get(id: string): Promise<Task> {
    // Worker returns: { task: {...}, labels: [...] }
    const raw = await this.http.get<Record<string, unknown>>(`/tasks/${id}`);
    return normalizeSingle<Task>(raw, 'task');
  }

  async create(input: CreateTaskInput): Promise<Task> {
    // Worker returns: { task: {...} }
    const raw = await this.http.post<Record<string, unknown>>('/tasks', input);
    return normalizeSingle<Task>(raw, 'task');
  }

  async update(id: string, input: UpdateTaskInput): Promise<Task> {
    // Worker uses PUT (full replacement), not PATCH
    const raw = await this.http.put<Record<string, unknown>>(`/tasks/${id}`, input);
    return normalizeSingle<Task>(raw, 'task');
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/tasks/${id}`);
  }

  // ─── Labels ──────────────────────────────────────────────────────────

  /** List all labels on a task */
  async listLabels(taskId: string): Promise<TaskLabel[]> {
    // Worker returns: { data: [...] }
    const raw = await this.http.get<unknown>(`/tasks/${taskId}/labels`);
    return normalizeList<TaskLabel>(raw, 'labels');
  }

  /** Add a label to a task (POST /tasks/:id/labels/:labelId) */
  async addLabel(taskId: string, input: AddTaskLabelInput): Promise<TaskLabel> {
    const raw = await this.http.post<Record<string, unknown>>(
      `/tasks/${taskId}/labels/${input.label_id}`,
      {},
    );
    return normalizeSingle<TaskLabel>(raw, 'label');
  }

  /** Remove a label from a task */
  async removeLabel(taskId: string, labelId: string): Promise<void> {
    await this.http.delete(`/tasks/${taskId}/labels/${labelId}`);
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a task */
  async listComments(taskId: string, options?: ListOptions): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    // Worker returns: { comments: [...], count, total, has_more }
    const raw = await this.http.get<Record<string, unknown>>(`/tasks/${taskId}/comments`, params);
    return normalizePaginated<Comment>(raw, 'comments', limit, offset);
  }

  /** Add a comment to a task */
  async addComment(taskId: string, input: CreateCommentInput): Promise<Comment> {
    const raw = await this.http.post<Record<string, unknown>>(
      `/tasks/${taskId}/comments`,
      input,
    );
    return normalizeSingle<Comment>(raw, 'comment');
  }

  /** Update a comment (requires write:comments scope) */
  async updateComment(commentId: string, input: UpdateCommentInput): Promise<Comment> {
    const raw = await this.http.put<Record<string, unknown>>(
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
