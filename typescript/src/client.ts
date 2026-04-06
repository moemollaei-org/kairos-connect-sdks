import { HttpClient } from './http';
import { TasksResource } from './resources/tasks';
import { GoalsResource } from './resources/goals';
import { TeamResource } from './resources/team';
import { DocumentsResource } from './resources/documents';
import type { KairosConfig, MeResponse, SingleResponse } from './types';

export class Kairos {
  public readonly tasks: TasksResource;
  public readonly goals: GoalsResource;
  public readonly team: TeamResource;
  public readonly documents: DocumentsResource;

  private http: HttpClient;

  constructor(config?: KairosConfig) {
    const apiKey = config?.apiKey || process.env.KAIROS_API_KEY;
    const baseUrl = config?.baseUrl || 'https://gateway.thekairos.app/v1';
    const timeout = config?.timeout ?? 30000;
    const maxRetries = config?.maxRetries ?? 3;

    if (!apiKey) {
      throw new Error(
        'API key is required. Provide it via config.apiKey or KAIROS_API_KEY environment variable.',
      );
    }

    this.http = new HttpClient({
      apiKey,
      baseUrl,
      timeout,
      maxRetries,
    });

    this.tasks = new TasksResource(this.http);
    this.goals = new GoalsResource(this.http);
    this.team = new TeamResource(this.http);
    this.documents = new DocumentsResource(this.http);
  }

  async me(): Promise<MeResponse> {
    const response = await this.http.get<SingleResponse<MeResponse>>('/me');
    return response.data;
  }
}
