import { describe, it, expect, beforeEach, vi } from 'vitest';
import { Kairos } from '../src/client';
import type { MeResponse } from '../src/types';

describe('Kairos Client', () => {
  beforeEach(() => {
    delete process.env.KAIROS_API_KEY;
  });

  describe('constructor', () => {
    it('should read API key from environment variable', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key_12345';
      const client = new Kairos();
      expect(client).toBeDefined();
      expect(client.tasks).toBeDefined();
      expect(client.goals).toBeDefined();
      expect(client.team).toBeDefined();
      expect(client.documents).toBeDefined();
    });

    it('should use config API key over environment variable', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_env_key';
      const client = new Kairos({
        apiKey: 'kairos_sk_config_key',
      });
      expect(client).toBeDefined();
    });

    it('should throw error if no API key is provided', () => {
      expect(() => {
        new Kairos();
      }).toThrow('API key is required');
    });

    it('should use custom base URL', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos({
        baseUrl: 'https://custom.api.com/v1',
      });
      expect(client).toBeDefined();
    });

    it('should use default config values', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();
      expect(client).toBeDefined();
    });
  });

  describe('me()', () => {
    it('should fetch current user and team information', async () => {
      const mockResponse: MeResponse = {
        team_id: 'team_1',
        scopes: ['tasks:read', 'tasks:write', 'goals:read'],
        rate_limit_per_minute: 100,
        rate_limit_per_hour: 1000,
      };

      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({ data: mockResponse }),
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

      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();
      const result = await client.me();

      expect(result).toEqual(mockResponse);
      expect(result.team_id).toBe('team_1');
      expect(result.scopes).toContain('tasks:read');
    });

    it('should include authorization header with API key', async () => {
      global.fetch = vi.fn(() =>
        Promise.resolve(
          new Response(
            JSON.stringify({
              data: {
                team_id: 'team_1',
                scopes: [],
                rate_limit_per_minute: 100,
                rate_limit_per_hour: 1000,
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

      process.env.KAIROS_API_KEY = 'kairos_sk_test_key_12345';
      const client = new Kairos();
      await client.me();

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/me'),
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer kairos_sk_test_key_12345',
          }),
        }),
      );
    });
  });

  describe('resource initialization', () => {
    it('should initialize all resource classes', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();

      expect(client.tasks).toBeDefined();
      expect(client.goals).toBeDefined();
      expect(client.team).toBeDefined();
      expect(client.documents).toBeDefined();
    });

    it('should have tasks resource with all methods', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();

      expect(typeof client.tasks.list).toBe('function');
      expect(typeof client.tasks.get).toBe('function');
      expect(typeof client.tasks.create).toBe('function');
      expect(typeof client.tasks.update).toBe('function');
      expect(typeof client.tasks.delete).toBe('function');
      expect(typeof client.tasks.listComments).toBe('function');
      expect(typeof client.tasks.addComment).toBe('function');
    });

    it('should have goals resource with all methods', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();

      expect(typeof client.goals.list).toBe('function');
      expect(typeof client.goals.get).toBe('function');
      expect(typeof client.goals.create).toBe('function');
      expect(typeof client.goals.update).toBe('function');
      expect(typeof client.goals.listTasks).toBe('function');
    });

    it('should have team resource with all methods', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();

      expect(typeof client.team.get).toBe('function');
      expect(typeof client.team.listMembers).toBe('function');
    });

    it('should have documents resource with all methods', () => {
      process.env.KAIROS_API_KEY = 'kairos_sk_test_key';
      const client = new Kairos();

      expect(typeof client.documents.list).toBe('function');
      expect(typeof client.documents.get).toBe('function');
    });
  });
});
