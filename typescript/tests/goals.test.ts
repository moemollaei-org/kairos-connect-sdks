import { describe, it, expect, beforeEach, vi } from 'vitest';
import { Kairos } from '../src/client';
import type { Goal, CreateGoalInput } from '../src/types';

describe('GoalsResource', () => {
  let client: Kairos;

  beforeEach(() => {
    process.env.KAIROS_API_KEY = 'kairos_sk_test_key_12345';
  });

  describe('list()', () => {
    it('should fetch goals with pagination', async () => {
      const mockGoals: Goal[] = [
        {
          id: 'goal_1',
          team_id: 'team_1',
          title: 'Q2 Objectives',
          description: 'Quarterly objectives for Q2',
          status: 'active',
          progress: 45,
          due_date: '2026-06-30',
          created_by: 'user_1',
          created_at: '2026-04-05T00:00:00Z',
          updated_at: '2026-04-05T00:00:00Z',
        },
      ];

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              goals: mockGoals,
              count: 1,
              total: 1,
              hasMore: false,
              limit: 10,
              offset: 0,
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
      const result = await client.goals.list();

      expect(result.data).toEqual(mockGoals);
      expect(result.pagination.total).toBe(1);
    });

    it('should filter goals by status', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              goals: [],
              count: 0,
              total: 0,
              hasMore: false,
              limit: 10,
              offset: 0,
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
      await client.goals.list({ status: 'active' });

      const callUrl = (global.fetch as any).mock.calls[0][0];
      expect(callUrl).toContain('status=active');
    });
  });

  describe('get()', () => {
    it('should fetch a single goal by ID', async () => {
      const mockGoal: Goal = {
        id: 'goal_1',
        team_id: 'team_1',
        title: 'Q2 Objectives',
        description: 'Quarterly objectives',
        status: 'active',
        progress: 45,
        due_date: '2026-06-30',
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T00:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ goal: mockGoal }),
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
      const result = await client.goals.get('goal_1');

      expect(result).toEqual(mockGoal);
    });
  });

  describe('create()', () => {
    it('should create a new goal', async () => {
      const input: CreateGoalInput = {
        title: 'New Goal',
        description: 'Goal description',
        due_date: '2026-06-30',
      };

      const createdGoal: Goal = {
        id: 'goal_new',
        team_id: 'team_1',
        ...input,
        status: 'active',
        progress: 0,
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T00:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ goal: createdGoal }),
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
      const result = await client.goals.create(input);

      expect(result).toEqual(createdGoal);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/goals'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(input),
        }),
      );
    });
  });

  describe('update()', () => {
    it('should update an existing goal', async () => {
      const updateInput = {
        status: 'completed' as const,
      };

      const updatedGoal: Goal = {
        id: 'goal_1',
        team_id: 'team_1',
        title: 'Q2 Objectives',
        description: 'Quarterly objectives',
        status: 'completed',
        progress: 100,
        due_date: '2026-06-30',
        created_by: 'user_1',
        created_at: '2026-04-05T00:00:00Z',
        updated_at: '2026-04-05T01:00:00Z',
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ goal: updatedGoal }),
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
      const result = await client.goals.update('goal_1', updateInput);

      expect(result.status).toBe('completed');
      expect(result.progress).toBe(100);
    });
  });

  describe('listTasks()', () => {
    it('should fetch tasks under a goal', async () => {
      const mockTasks = [
        {
          id: 'task_1',
          team_id: 'team_1',
          goal_id: 'goal_1',
          parent_task_id: null,
          title: 'Task 1',
          description: null,
          type: 'task' as const,
          status: 'to_do' as const,
          priority: 'high' as const,
          assigned_to: null,
          estimated_hours: null,
          actual_hours: null,
          due_date: null,
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
              tasks: mockTasks,
              count: 1,
              total: 1,
              hasMore: false,
              limit: 10,
              offset: 0,
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
      const result = await client.goals.listTasks('goal_1');

      expect(result.data).toEqual(mockTasks);
    });
  });
});
