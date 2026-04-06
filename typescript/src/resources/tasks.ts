import { HttpClient } from '../http';
import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  TaskAssignee,
  AddTaskAssigneeInput,
  TaskLabel,
  AddTaskLabelInput,
  TaskDependency,
  AddTaskDependencyInput,
  ListTasksOptions,
  ListOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class TasksResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListTasksOptions): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};
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
    return this.http.get<PaginatedResponse<Task>>('/tasks', params);
  }

  async get(id: string): Promise<Task> {
    const response = await this.http.get<SingleResponse<Task>>(`/tasks/${id}`);
    return response.data;
  }

  async create(input: CreateTaskInput): Promise<Task> {
    const response = await this.http.post<SingleResponse<Task>>('/tasks', input);
    return response.data;
  }

  async update(id: string, input: UpdateTaskInput): Promise<Task> {
    const response = await this.http.patch<SingleResponse<Task>>(`/tasks/${id}`, input);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/tasks/${id}`);
  }

  // ─── Assignees ───────────────────────────────────────────────────────

  /** List all assignees for a task */
  async listAssignees(taskId: string): Promise<TaskAssignee[]> {
    const response = await this.http.get<SingleResponse<TaskAssignee[]>>(
      `/tasks/${taskId}/assignees`,
    );
    return response.data;
  }

  /** Add a user as an assignee to a task */
  async addAssignee(taskId: string, input: AddTaskAssigneeInput): Promise<TaskAssignee> {
    const response = await this.http.post<SingleResponse<TaskAssignee>>(
      `/tasks/${taskId}/assignees`,
      input,
    );
    return response.data;
  }

  /** Remove a user from a task's assignees */
  async removeAssignee(taskId: string, userId: string): Promise<void> {
    await this.http.delete(`/tasks/${taskId}/assignees/${userId}`);
  }

  // ─── Labels ──────────────────────────────────────────────────────────

  /** List all labels on a task */
  async listLabels(taskId: string): Promise<TaskLabel[]> {
    const response = await this.http.get<SingleResponse<TaskLabel[]>>(
      `/tasks/${taskId}/labels`,
    );
    return response.data;
  }

  /** Add a label to a task */
  async addLabel(taskId: string, input: AddTaskLabelInput): Promise<TaskLabel> {
    const response = await this.http.post<SingleResponse<TaskLabel>>(
      `/tasks/${taskId}/labels`,
      input,
    );
    return response.data;
  }

  /** Remove a label from a task */
  async removeLabel(taskId: string, labelId: string): Promise<void> {
    await this.http.delete(`/tasks/${taskId}/labels/${labelId}`);
  }

  // ─── Subtasks ─────────────────────────────────────────────────────────

  /** List immediate subtasks of a task */
  async listSubtasks(taskId: string, options?: ListOptions): Promise<PaginatedResponse<Task>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Task>>(`/tasks/${taskId}/subtasks`, params);
  }

  /** Create a subtask under a parent task */
  async createSubtask(taskId: string, input: CreateTaskInput): Promise<Task> {
    const response = await this.http.post<SingleResponse<Task>>(
      `/tasks/${taskId}/subtasks`,
      input,
    );
    return response.data;
  }

  // ─── Dependencies ─────────────────────────────────────────────────────

  /** List dependencies for a task */
  async listDependencies(taskId: string): Promise<TaskDependency[]> {
    const response = await this.http.get<SingleResponse<TaskDependency[]>>(
      `/tasks/${taskId}/dependencies`,
    );
    return response.data;
  }

  /** Add a dependency to a task */
  async addDependency(taskId: string, input: AddTaskDependencyInput): Promise<TaskDependency> {
    const response = await this.http.post<SingleResponse<TaskDependency>>(
      `/tasks/${taskId}/dependencies`,
      input,
    );
    return response.data;
  }

  /** Remove a dependency from a task */
  async removeDependency(taskId: string, dependencyId: string): Promise<void> {
    await this.http.delete(`/tasks/${taskId}/dependencies/${dependencyId}`);
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a task */
  async listComments(taskId: string, options?: ListOptions): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Comment>>(`/tasks/${taskId}/comments`, params);
  }

  /** Add a comment to a task */
  async addComment(taskId: string, input: CreateCommentInput): Promise<Comment> {
    const response = await this.http.post<SingleResponse<Comment>>(
      `/tasks/${taskId}/comments`,
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
