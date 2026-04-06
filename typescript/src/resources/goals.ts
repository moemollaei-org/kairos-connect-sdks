import { HttpClient } from '../http';
import type {
  Goal,
  CreateGoalInput,
  UpdateGoalInput,
  Task,
  ListGoalsOptions,
  ListTasksOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class GoalsResource {
  constructor(private http: HttpClient) {}

  async list(
    options?: ListGoalsOptions,
  ): Promise<PaginatedResponse<Goal>> {
    const params: Record<string, unknown> = {};

    if (options) {
      if (options.status) params.status = options.status;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }

    const response = await this.http.get<PaginatedResponse<Goal>>(
      '/goals',
      params,
    );
    return response;
  }

  async get(id: string): Promise<Goal> {
    const response = await this.http.get<SingleResponse<Goal>>(`/goals/${id}`);
    return response.data;
  }

  async create(input: CreateGoalInput): Promise<Goal> {
    const response = await this.http.post<SingleResponse<Goal>>(
      '/goals',
      input,
    );
    return response.data;
  }

  async update(id: string, input: UpdateGoalInput): Promise<Goal> {
    const response = await this.http.patch<SingleResponse<Goal>>(
      `/goals/${id}`,
      input,
    );
    return response.data;
  }

  async listTasks(
    goalId: string,
    options?: ListTasksOptions,
  ): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};

    if (options) {
      if (options.status) params.status = options.status;
      if (options.priority) params.priority = options.priority;
      if (options.assigned_to) params.assigned_to = options.assigned_to;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }

    const response = await this.http.get<PaginatedResponse<Task>>(
      `/goals/${goalId}/tasks`,
      params,
    );
    return response;
  }
}
