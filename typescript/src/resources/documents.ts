import { HttpClient } from '../http';
import type {
  Document,
  ListOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class DocumentsResource {
  constructor(private http: HttpClient) {}

  async list(options?: ListOptions): Promise<PaginatedResponse<Document>> {
    const params: Record<string, unknown> = {};

    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }

    const response = await this.http.get<PaginatedResponse<Document>>(
      '/documents',
      params,
    );
    return response;
  }

  async get(id: string): Promise<Document> {
    const response = await this.http.get<SingleResponse<Document>>(
      `/documents/${id}`,
    );
    return response.data;
  }
}
