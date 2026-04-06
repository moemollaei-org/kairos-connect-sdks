import { HttpClient } from '../http';
import { normalizePaginated, normalizeSingle } from '../normalize';
import type {
  Form,
  CreateFormInput,
  UpdateFormInput,
  FormSubmission,
  ListFormsOptions,
  ListOptions,
  PaginatedResponse,
} from '../types';

/**
 * Forms resource.
 *
 * The underlying Kairos worker exposes forms as "instances" at
 * /api/v1/forms/instances.  The gateway routes /v1/forms/instances/* to
 * the FORMS worker, so the SDK uses /forms/instances as its base path.
 * Submissions are "records" in the worker's data model.
 */
export class FormsResource {
  private readonly BASE = '/forms/instances';

  constructor(private http: HttpClient) {}

  // ─── Core CRUD ───────────────────────────────────────────────────────

  async list(options?: ListFormsOptions): Promise<PaginatedResponse<Form>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 50;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    // Worker returns: { instances: [...], count, total, has_more }
    // team_id is injected automatically by the gateway proxy.
    const raw = await this.http.get<Record<string, unknown>>(this.BASE, params);
    return normalizePaginated<Form>(raw, 'instances', limit, offset);
  }

  async get(id: string): Promise<Form> {
    // Worker returns: { instance: {...} }
    const raw = await this.http.get<Record<string, unknown>>(`${this.BASE}/${id}`);
    return normalizeSingle<Form>(raw, 'instance');
  }

  async create(input: CreateFormInput): Promise<Form> {
    // Worker returns: { instance: {...} }
    const raw = await this.http.post<Record<string, unknown>>(this.BASE, input);
    return normalizeSingle<Form>(raw, 'instance');
  }

  async update(id: string, input: UpdateFormInput): Promise<Form> {
    // Worker returns: { instance: {...} }
    const raw = await this.http.put<Record<string, unknown>>(`${this.BASE}/${id}`, input);
    return normalizeSingle<Form>(raw, 'instance');
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`${this.BASE}/${id}`);
  }

  // ─── Submissions (records) ────────────────────────────────────────────

  /** List all records (submissions) for a form instance (requires read:forms scope) */
  async listSubmissions(
    formId: string,
    options?: ListOptions,
  ): Promise<PaginatedResponse<FormSubmission>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 50;
    const offset = options?.offset ?? 0;
    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }
    const raw = await this.http.get<Record<string, unknown>>(
      `${this.BASE}/${formId}/records`,
      params,
    );
    return normalizePaginated<FormSubmission>(raw, 'records', limit, offset);
  }

  /** Submit a record for a form instance (requires write:forms scope) */
  async submit(
    formId: string,
    data: Record<string, unknown>,
  ): Promise<FormSubmission> {
    const raw = await this.http.post<Record<string, unknown>>(
      `${this.BASE}/${formId}/records`,
      { data },
    );
    return normalizeSingle<FormSubmission>(raw, 'record');
  }
}
