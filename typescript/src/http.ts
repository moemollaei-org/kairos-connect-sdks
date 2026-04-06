import {
  KairosError,
  AuthError,
  ForbiddenError,
  NotFoundError,
  RateLimitError,
  ValidationError,
  InternalError,
} from './errors';
import type { RateLimitInfo } from './types';

interface HttpClientConfig {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  maxRetries: number;
}

export class HttpClient {
  private apiKey: string;
  private baseUrl: string;
  private timeout: number;
  private maxRetries: number;
  public rateLimit: RateLimitInfo | null = null;

  constructor(config: HttpClientConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl;
    this.timeout = config.timeout;
    this.maxRetries = config.maxRetries;
  }

  private updateRateLimitInfo(headers: Headers): void {
    const limitPerMinute = headers.get('X-RateLimit-Limit-Minute');
    const remainingPerMinute = headers.get('X-RateLimit-Remaining-Minute');
    const limitPerHour = headers.get('X-RateLimit-Limit-Hour');
    const remainingPerHour = headers.get('X-RateLimit-Remaining-Hour');
    const resetAt = headers.get('X-RateLimit-Reset');

    if (
      limitPerMinute &&
      remainingPerMinute &&
      limitPerHour &&
      remainingPerHour &&
      resetAt
    ) {
      this.rateLimit = {
        limitPerMinute: parseInt(limitPerMinute, 10),
        remainingPerMinute: parseInt(remainingPerMinute, 10),
        limitPerHour: parseInt(limitPerHour, 10),
        remainingPerHour: parseInt(remainingPerHour, 10),
        resetAt: parseInt(resetAt, 10),
      };
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    this.updateRateLimitInfo(response.headers);

    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');
    const requestId = response.headers.get('X-Request-Id');

    if (!response.ok) {
      let errorData: {
        error?: { code: string; message: string };
      } | null = null;

      if (isJson) {
        try {
          errorData = (await response.json()) as {
            error?: { code: string; message: string };
          } | null;
        } catch {
          // Ignore JSON parse errors
        }
      }

      const errorMessage = errorData?.error?.message || response.statusText;
      const errorCode = errorData?.error?.code || 'UNKNOWN_ERROR';

      switch (response.status) {
        case 400:
          throw new ValidationError(errorMessage, requestId ?? undefined);
        case 401:
          throw new AuthError(errorMessage, requestId ?? undefined);
        case 403:
          throw new ForbiddenError(errorMessage, requestId ?? undefined);
        case 404:
          throw new NotFoundError(errorMessage, requestId ?? undefined);
        case 429: {
          const retryAfter = response.headers.get('Retry-After');
          const retryAfterSeconds = retryAfter ? parseInt(retryAfter, 10) : 60;
          throw new RateLimitError(
            errorMessage,
            retryAfterSeconds,
            requestId ?? undefined,
          );
        }
        case 500:
        case 502:
        case 503:
        case 504:
          throw new InternalError(errorMessage, requestId ?? undefined);
        default:
          throw new KairosError(
            errorCode,
            errorMessage,
            response.status,
            requestId ?? undefined,
          );
      }
    }

    if (isJson) {
      return (await response.json()) as T;
    }

    throw new KairosError(
      'INVALID_RESPONSE',
      'Response is not JSON',
      response.status,
      requestId ?? undefined,
    );
  }

  private async makeRequest<T>(
    method: string,
    path: string,
    body?: unknown,
    retryCount = 0,
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const headers: Record<string, string> = {
        'Authorization': `Bearer ${this.apiKey}`,
        'User-Agent': 'kairos-sdk-js/0.1.0',
      };
      // Only set Content-Type when there is a body — sending it on GET/DELETE
      // causes some Cloudflare Workers to return 404 due to request routing.
      if (body !== undefined) {
        headers['Content-Type'] = 'application/json';
      }

      const response = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      return await this.handleResponse<T>(response);
    } catch (error) {
      if (error instanceof RateLimitError && retryCount < this.maxRetries) {
        const delayMs = error.retryAfter * 1000;
        await new Promise((resolve) => setTimeout(resolve, delayMs));
        return this.makeRequest<T>(method, path, body, retryCount + 1);
      }

      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  async get<T>(path: string, params?: Record<string, unknown>): Promise<T> {
    let fullPath = path;

    if (params && Object.keys(params).length > 0) {
      const searchParams = new URLSearchParams();
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== null) {
          searchParams.append(key, String(value));
        }
      }
      fullPath = `${path}?${searchParams.toString()}`;
    }

    return this.makeRequest<T>('GET', fullPath);
  }

  async post<T>(path: string, body?: unknown): Promise<T> {
    return this.makeRequest<T>('POST', path, body);
  }

  async put<T>(path: string, body?: unknown): Promise<T> {
    return this.makeRequest<T>('PUT', path, body);
  }

  async patch<T>(path: string, body?: unknown): Promise<T> {
    return this.makeRequest<T>('PATCH', path, body);
  }

  async delete<T>(path: string): Promise<T> {
    return this.makeRequest<T>('DELETE', path);
  }
}
