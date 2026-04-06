/**
 * Response normalization helpers.
 *
 * The Kairos microservice workers return resource-specific response shapes
 * (e.g. { tasks: [...], count, total, hasMore }) rather than the generic
 * { data: [...], pagination: {...} } envelope the SDK exposes to callers.
 *
 * These helpers bridge the gap without coupling every resource method to the
 * specific field names used by each worker.
 */

import type { PaginatedResponse } from './types';

/**
 * Normalise a paginated list response from a worker into the generic
 * PaginatedResponse<T> shape that the SDK surface exposes.
 *
 * @param raw    Raw JSON object returned by the worker.
 * @param key    The resource-specific array key (e.g. "tasks", "goals").
 * @param limit  The requested page size (used to synthesise `page` number).
 * @param offset The requested offset.
 */
export function normalizePaginated<T>(
  raw: Record<string, unknown>,
  key: string,
  limit = 20,
  offset = 0,
): PaginatedResponse<T> {
  // Worker may use a resource-specific key ("tasks") or the generic "data" key.
  const items = ((raw[key] ?? raw['data'] ?? []) as T[]);

  // Workers use "total" or "total_count" for the grand total.
  const total = Number(raw['total'] ?? raw['total_count'] ?? raw['count'] ?? 0);

  // Workers use "hasMore" (camelCase) or "has_more" (snake_case).
  const hasMore = Boolean(raw['hasMore'] ?? raw['has_more'] ?? false);

  // Actual limit returned by the worker (may differ from requested).
  const resolvedLimit = Number(raw['limit'] ?? limit);
  const resolvedOffset = Number(raw['offset'] ?? offset);

  return {
    data: items,
    pagination: {
      page: resolvedLimit > 0 ? Math.floor(resolvedOffset / resolvedLimit) + 1 : 1,
      limit: resolvedLimit,
      total,
      has_more: hasMore,
    },
  };
}

/**
 * Normalise a single-resource response from a worker.
 *
 * @param raw Raw JSON object returned by the worker.
 * @param key The resource-specific key (e.g. "task", "goal", "document").
 */
export function normalizeSingle<T>(raw: Record<string, unknown>, key: string): T {
  return (raw[key] ?? raw['data']) as T;
}

/**
 * Normalise a list sub-resource (e.g. assignees, labels, dependencies)
 * where the worker returns a plain array or wraps it in a keyed object.
 */
export function normalizeList<T>(raw: unknown, key?: string): T[] {
  if (Array.isArray(raw)) return raw as T[];
  if (raw && typeof raw === 'object') {
    const obj = raw as Record<string, unknown>;
    if (key && Array.isArray(obj[key])) return obj[key] as T[];
    if (Array.isArray(obj['data'])) return obj['data'] as T[];
  }
  return [];
}
