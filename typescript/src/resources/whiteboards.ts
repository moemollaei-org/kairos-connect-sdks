import { HttpClient } from '../http';
import { normalizePaginated, normalizeSingle } from '../normalize';
import type {
  Whiteboard,
  CreateWhiteboardInput,
  UpdateWhiteboardInput,
  ListWhiteboardsOptions,
  PaginatedResponse,
} from '../types';

export class WhiteboardsResource {
  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListWhiteboardsOptions): Promise<PaginatedResponse<Whiteboard>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 50;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
      if (options.search) params.search = options.search;
    }
    // Worker returns: { whiteboards: [...], total_count, limit, offset }
    // team_id is injected automatically by the gateway proxy.
    const raw = await this.http.get<Record<string, unknown>>('/whiteboards', params);
    return normalizePaginated<Whiteboard>(raw, 'whiteboards', limit, offset);
  }

  async get(id: string): Promise<Whiteboard> {
    // Worker returns: { whiteboard: {...} }
    const raw = await this.http.get<Record<string, unknown>>(`/whiteboards/${id}`);
    return normalizeSingle<Whiteboard>(raw, 'whiteboard');
  }

  async create(input: CreateWhiteboardInput): Promise<Whiteboard> {
    // Worker returns: { whiteboard: {...} }
    const raw = await this.http.post<Record<string, unknown>>('/whiteboards', input);
    return normalizeSingle<Whiteboard>(raw, 'whiteboard');
  }

  async update(id: string, input: UpdateWhiteboardInput): Promise<Whiteboard> {
    // Worker returns: { whiteboard: {...} }
    const raw = await this.http.put<Record<string, unknown>>(`/whiteboards/${id}`, input);
    return normalizeSingle<Whiteboard>(raw, 'whiteboard');
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/whiteboards/${id}`);
  }
}
