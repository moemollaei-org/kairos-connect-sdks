import { HttpClient } from '../http';
import { normalizeList } from '../normalize';
import type { Team, TeamMember, ListOptions, PaginatedResponse } from '../types';

export class TeamResource {
  constructor(private http: HttpClient) {}

  /**
   * Get the current API key's team.
   * Worker returns { teams: [...] } — we return the first (and typically only) team.
   */
  async get(): Promise<Team> {
    const raw = await this.http.get<Record<string, unknown>>('/teams');
    const teams = normalizeList<Team>(raw, 'teams');
    if (!teams.length) throw new Error('No team found for this API key');
    return teams[0];
  }

  /**
   * List members of a team by ID.
   * Worker: GET /api/v1/teams/:id/members → { members: [...] }
   */
  async listMembers(teamId: string, options?: ListOptions): Promise<PaginatedResponse<TeamMember>> {
    const params: Record<string, unknown> = {};
    const limit = options?.limit ?? 50;
    const offset = options?.offset ?? 0;
    if (options?.limit) params.limit = options.limit;
    if (options?.offset) params.offset = options.offset;

    const raw = await this.http.get<Record<string, unknown>>(`/teams/${teamId}/members`, params);
    const members = normalizeList<TeamMember>(raw, 'members');
    return {
      data: members,
      pagination: { page: 1, limit, total: members.length, has_more: false },
    };
  }
}
