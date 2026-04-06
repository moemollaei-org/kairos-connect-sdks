import { HttpClient } from '../http';
import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  Comment,
  CreateCommentInput,
  ListTasksOptions,
  ListOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class TasksResource {
  constructor(private http: HttpClient) {}

  async list(
    options?: ListTasksOptions,
  ): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};

    if (options) {
      if (options.status) params.status = options.status;
      if (options.priority) params.priority = options.priority;
      if (options.assigned_to) params.assigned_to = options.assigned_to;
      if (options.goal_id) params.goal_id = options.goal_id;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }

    const response = await this.http.get<PaginatedResponse<Task>>(
      '/tasks',
      params,
    );
    return response;
  }

  async get(id: string): Promise<Task> {
    const response = await this.http.get<SingleResponse<Task>>(`/tasks/${id}`);
    return response.data;
  }

  async create(input: CreateTaskInput): Promise<Task> {
    const response = await this.http.post<SingleResponse<Task>>(
      '/tasks',
      input,
    );
    return response.data;
  }

  async update(id: string, input: UpdateTaskInput): Promise<Task> {
    const response = await this.http.patch<SingleResponse<Task>>(
      `/tasks/${id}`,
      input,
    );
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/tasks/${id}`);
  }

  async listComments(
    taskId: string,
    options?: ListOptions,
  ): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};

    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }

    const response = await this.http.get<PaginatedResponse<Comment>>(
      `/tasks/${taskId}/comments`,
      params,
    );
    return response;
  }

  async addComment(
    taskId: string,
    input: CreateCommentInput,
  ): Promise<Comment> {
    const response = await this.http.post<SingleResponse<Comment>>(
      `/tasks/${taskId}/comments`,
      input,
    );
    return response.data;
  }
}
