import { HttpClient } from '../http';
import type {
  Whiteboard,
  CreateWhiteboardInput,
  UpdateWhiteboardInput,
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  ListWhiteboardsOptions,
  ListOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class WhiteboardsResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListWhiteboardsOptions): Promise<PaginatedResponse<Whiteboard>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }
    return this.http.get<PaginatedResponse<Whiteboard>>('/whiteboards', params);
  }

  async get(id: string): Promise<Whiteboard> {
    const response = await this.http.get<SingleResponse<Whiteboard>>(`/whiteboards/${id}`);
    return response.data;
  }

  async create(input: CreateWhiteboardInput): Promise<Whiteboard> {
    const response = await this.http.post<SingleResponse<Whiteboard>>('/whiteboards', input);
    return response.data;
  }

  async update(id: string, input: UpdateWhiteboardInput): Promise<Whiteboard> {
    const response = await this.http.patch<SingleResponse<Whiteboard>>(
      `/whiteboards/${id}`,
      input,
    );
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/whiteboards/${id}`);
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a whiteboard (requires read:comments scope) */
  async listComments(
    whiteboardId: string,
    options?: ListOptions,
  ): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    return this.http.get<PaginatedResponse<Comment>>(
      `/whiteboards/${whiteboardId}/comments`,
      params,
    );
  }

  /** Add a comment to a whiteboard (requires write:comments scope) */
  async addComment(whiteboardId: string, input: CreateCommentInput): Promise<Comment> {
    const response = await this.http.post<SingleResponse<Comment>>(
      `/whiteboards/${whiteboardId}/comments`,
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
