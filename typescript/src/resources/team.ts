import { HttpClient } from '../http';
import type {
  Team,
  TeamMember,
  ListOptions,
  PaginatedResponse,
  SingleResponse,
} from '../types';

export class TeamResource {
  constructor(private http: HttpClient) {}

  async get(): Promise<Team> {
    const response = await this.http.get<SingleResponse<Team>>('/team');
    return response.data;
  }

  async listMembers(options?: ListOptions): Promise<PaginatedResponse<TeamMember>> {
    const params: Record<string, unknown> = {};

    if (options) {
      if (options.limit) params.limit = options.limit;
      if (options.offset) params.offset = options.offset;
    }

    const response = await this.http.get<PaginatedResponse<TeamMember>>(
      '/team/members',
      params,
    );
    return response;
  }
}
