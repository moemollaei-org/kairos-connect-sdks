import { HttpClient } from '../http';
import { normalizePaginated, normalizeSingle } from '../normalize';
import type {
  Document,
  CreateDocumentInput,
  UpdateDocumentInput,
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  ListDocumentsOptions,
  ListOptions,
  PaginatedResponse,
} from '../types';

export class DocumentsResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListDocumentsOptions): Promise<PaginatedResponse<Document>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 50;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.teamspace_id) params.teamspace_id = options.teamspace_id;
      if (options.parent_id) params.parent_id = options.parent_id;
      if (options.type) params.type = options.type;
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }
    // Worker returns: { documents: [...], total_count, limit, offset }
    // team_id is injected automatically by the gateway proxy.
    const raw = await this.http.get<Record<string, unknown>>('/documents', params);
    return normalizePaginated<Document>(raw, 'documents', limit, offset);
  }

  async get(id: string): Promise<Document> {
    // Worker returns: { document: {...} }
    const raw = await this.http.get<Record<string, unknown>>(`/documents/${id}`);
    return normalizeSingle<Document>(raw, 'document');
  }

  async create(input: CreateDocumentInput): Promise<Document> {
    // Worker returns: { document: {...} }
    const raw = await this.http.post<Record<string, unknown>>('/documents', input);
    return normalizeSingle<Document>(raw, 'document');
  }

  async update(id: string, input: UpdateDocumentInput): Promise<Document> {
    // Worker returns: { document: {...} }
    const raw = await this.http.patch<Record<string, unknown>>(`/documents/${id}`, input);
    return normalizeSingle<Document>(raw, 'document');
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/documents/${id}`);
  }

  // ─── Comments ─────────────────────────────────────────────────────────

  /** List all comments on a document (requires read:comments scope) */
  async listComments(
    documentId: string,
    options?: ListOptions,
  ): Promise<PaginatedResponse<Comment>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    const raw = await this.http.get<Record<string, unknown>>(
      `/documents/${documentId}/comments`,
      params,
    );
    return normalizePaginated<Comment>(raw, 'comments', limit, offset);
  }

  /** Add a comment to a document (requires write:comments scope) */
  async addComment(documentId: string, input: CreateCommentInput): Promise<Comment> {
    const raw = await this.http.post<Record<string, unknown>>(
      `/documents/${documentId}/comments`,
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
