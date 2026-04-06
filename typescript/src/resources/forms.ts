import { HttpClient } from '../http';
import type {
  Form,
  CreateFormInput,
  UpdateFormInput,
  FormSubmission,
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  ListFormsOptions,
  ListOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class FormsResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListFormsOptions): Promise<PaginatedResponse<Form>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.is_active !== undefined) params.is_active = options.is_active;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Form>>('/forms', params);
  }

  async get(id: string): Promise<Form> {
    const response = await this.http.get<SingleResponse<Form>>(`/forms/${id}`);
    return response.data;
  }

  async create(input: CreateFormInput): Promise<Form> {
    const response = await this.http.post<SingleResponse<Form>>('/forms', input);
    return response.data;
  }

  async update(id: string, input: UpdateFormInput): Promise<Form> {
    const response = await this.http.patch<SingleResponse<Form>>(`/forms/${id}`, input);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/forms/${id}`);
  }

  // ─── Submissions ──────────────────────────────────────────────────────

  /** List all submissions for a form (requires read:forms scope) */
  async listSubmissions(
    formId: string,
    options?: ListOptions,
  ): Promise<PaginatedResponse<FormSubmission>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<FormSubmission>>(
      `/forms/${formId}/submissions`,
      params,
    );
  }

  /** Submit a response to a form (requires write:forms scope) */
  async submit(
    formId: string,
    data: Record<string, unknown>,
  ): Promise<FormSubmission> {
    const response = await this.http.post<SingleResponse<FormSubmission>>(
      `/forms/${formId}/submissions`,
      { data },
    );
    return response.data;
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a form (requires read:comments scope) */
  async listComments(formId: string, options?: ListOptions): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Comment>>(`/forms/${formId}/comments`, params);
  }

  /** Add a comment to a form (requires write:comments scope) */
  async addComment(formId: string, input: CreateCommentInput): Promise<Comment> {
    const response = await this.http.post<SingleResponse<Comment>>(
      `/forms/${formId}/comments`,
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
