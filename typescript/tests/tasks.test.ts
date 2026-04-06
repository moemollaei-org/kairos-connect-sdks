import { describe, it, expect, beforeEach, vi } from 'vitest';
import { Kairos } from '../src/client';
import { AuthError, ValidationError, RateLimitError } from '../src/errors';
import type { Task, CreateTaskInput } from '../src/types';

describe('TasksResource', () => {
  let client: Kairos;

  beforeEach(() => {
    process.env.KAIROS_API_KEY = 'kairos_sk_test_key_12345';
  });

  describe('list()', () => {
    it('should fetch tasks with pagination', async () => {
      const mockTasks: Task[] = [
        {
          id: 'task_1',
          team_id: 'team_1',
          goal_id: null,
          parent_task_id: null,
          title: 'Test Task 1',
          description: 'Description 1',
          type: 'task',
          status: 'to_do',
          priority: 'high',
          assigned_to: 'user_1',
          estimated_hours: 5,
          actual_hours: null,
          due_date: '2026-04-10',
          completed_at: null,
          created_by: 'user_1',
          created_at: '2026-04-05T00:00:00Z',
          updated_at: '2026-04-05T00:00:00Z',
        },
      ];

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              data: mockTasks,
              pagination: {
                page: 1,
                limit: 10,
                total: 1,
                has_more: false,
              },
            }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      const result = await client.tasks.list();

      expect(result.data).toEqual(mockTasks);
      expect(result.pagination.total).toBe(1);
      expect(result.pagination.has_more).toBe(false);
    });

    it('should pass filter options to the API', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              data: [],
              pagination: {
                page: 1,
                limit: 10,
                total: 0,
                has_more: false,
              },
            }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      await client.tasks.list({
        status: 'in_progress',
        priority: 'high',
        limit: 20,
      });

      expect(global.fetch).toHaveBeenCalled();
      const callUrl = (global.fetch as any).mock.calls[0][0];
      expect(callUrl).toContain('status=in_progress');
      expect(callUrl).toContain('priority=high');
      expect(callUrl).toContain('limit=20');
    });
  });

  describe('get()', () => {
    it('should fetch a single task by ID', async () => {
      const mockTask: Task = {
        id: 'task_1',
        team_id: 'team_1',
        goal_id: null,
        parent_task_id: null,
        title: 'Test Task',
        description: 'Description',
        type: 'task',
        status: 'to_do',
        priority: 'medium',
        assigned_to: null,
        estimated_hours: null,
        actual_hours: null,
        due_date: null,
        completed_at: null,
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T00:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ data: mockTask }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      const result = await client.tasks.get('task_1');

      expect(result).toEqual(mockTask);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tasks/task_1'),
        expect.any(Object),
      );
    });
  });

  describe('create()', () => {
    it('should create a new task', async () => {
      const input: CreateTaskInput = {
        title: 'New Task',
        description: 'Task description',
        priority: 'high',
        estimated_hours: 8,
      };

      const createdTask: Task = {
        id: 'task_new',
        team_id: 'team_1',
        goal_id: null,
        parent_task_id: null,
        ...input,
        type: 'task',
        status: 'to_do',
        assigned_to: null,
        actual_hours: null,
        due_date: null,
        completed_at: null,
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T00:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ data: createdTask }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      const result = await client.tasks.create(input);

      expect(result).toEqual(createdTask);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tasks'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(input),
        }),
      );
    });
  });

  describe('update()', () => {
    it('should update an existing task', async () => {
      const updateInput = {
        status: 'in_progress' as const,
        actual_hours: 3,
      };

      const updatedTask: Task = {
        id: 'task_1',
        team_id: 'team_1',
        goal_id: null,
        parent_task_id: null,
        title: 'Test Task',
        description: null,
        type: 'task',
        status: 'in_progress',
        priority: 'medium',
        assigned_to: null,
        estimated_hours: 5,
        actual_hours: 3,
        due_date: null,
        completed_at: null,
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T01:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ data: updatedTask }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      const result = await client.tasks.update('task_1', updateInput);

      expect(result.status).toBe('in_progress');
      expect(result.actual_hours).toBe(3);
    });
  });

  describe('delete()', () => {
    it('should delete a task', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(null, {
            status: 204,
            headers: {
              'X-RateLimit-Limit-Minute': '100',
              'X-RateLimit-Remaining-Minute': '99',
              'X-RateLimit-Limit-Hour': '1000',
              'X-RateLimit-Remaining-Hour': '999',
              'X-RateLimit-Reset': '1712304000',
            },
          }),
        ),
      );

      client = new Kairos();
      await expect(client.tasks.delete('task_1')).rejects.toThrow();
    });
  });

  describe('error handling', () => {
    it('should throw AuthError on 401 response', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              error: {
                code: 'UNAUTHORIZED',
                message: 'Invalid API key',
              },
            }),
            {
              status: 401,
              headers: {
                'content-type': 'application/json',
                'X-Request-Id': 'req_123',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      await expect(client.tasks.list()).rejects.toThrow(AuthError);
    });

    it('should throw ValidationError on 400 response', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              error: {
                code: 'VALIDATION_ERROR',
                message: 'Missing required field: title',
              },
            }),
            {
              status: 400,
              headers: {
                'content-type': 'application/json',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      await expect(
        client.tasks.create({ title: '' }),
      ).rejects.toThrow(ValidationError);
    });

    it('should throw RateLimitError on 429 response with retryAfter', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              error: {
                code: 'RATE_LIMIT_EXCEEDED',
                message: 'Rate limit exceeded',
              },
            }),
            {
              status: 429,
              headers: {
                'content-type': 'application/json',
                'Retry-After': '60',
              },
            },
          ),
        ),
      );

      client = new Kairos({ maxRetries: 0 });
      try {
        await client.tasks.list();
        expect.fail('Should have thrown RateLimitError');
      } catch (error) {
        expect(error).toBeInstanceOf(RateLimitError);
        expect((error as RateLimitError).retryAfter).toBe(60);
      }
    });
  });

  describe('listComments()', () => {
    it('should fetch comments for a task', async () => {
      const mockComments = [
        {
          id: 'comment_1',
          task_id: 'task_1',
          team_id: 'team_1',
          content: 'This is a comment',
          created_by: 'user_1',
          created_at: '2026-04-05T00:00:00Z',
          updated_at: '2026-04-05T00:00:00Z',
        },
      ];

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              data: mockComments,
              pagination: {
                page: 1,
                limit: 10,
                total: 1,
                has_more: false,
              },
            }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      const result = await client.tasks.listComments('task_1');

      expect(result.data).toEqual(mockComments);
    });
  });

  describe('addComment()', () => {
    it('should add a comment to a task', async () => {
      const newComment = {
        id: 'comment_new',
        task_id: 'task_1',
        team_id: 'team_1',
        content: 'New comment',
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T00:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ data: newComment }),
            {
              status: 200,
              headers: {
                'content-type': 'application/json',
                'X-RateLimit-Limit-Minute': '100',
                'X-RateLimit-Remaining-Minute': '99',
                'X-RateLimit-Limit-Hour': '1000',
                'X-RateLimit-Remaining-Hour': '999',
                'X-RateLimit-Reset': '1712304000',
              },
            },
          ),
        ),
      );

      client = new Kairos();
      const result = await client.tasks.addComment('task_1', {
        content: 'New comment',
      });

      expect(result.content).toBe('New comment');
    });
  });
});
