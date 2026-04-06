# Quick Start Guide

Get started with the Kairos SDK in 5 minutes.

## Installation

```bash
npm install @kairos/sdk
```

## Basic Usage

### Initialize the client

```typescript
import { Kairos } from '@kairos/sdk';

// Using environment variable
const kairos = new Kairos();

// Or provide API key directly
const kairos = new Kairos({
  apiKey: 'kairos_sk_your_key_here',
});
```

## Common Operations

### Create a Task

```typescript
const task = await kairos.tasks.create({
  title: 'Build login feature',
  priority: 'high',
  estimated_hours: 8,
});

console.log(`Created task: ${task.id}`);
```

### List Tasks

```typescript
const result = await kairos.tasks.list({
  status: 'in_progress',
  priority: 'high',
});

console.log(`Found ${result.data.length} tasks`);
console.log(`Total: ${result.pagination.total}`);
```

### Update a Task

```typescript
const updated = await kairos.tasks.update('task_id', {
  status: 'completed',
  actual_hours: 7.5,
});
```

### Create a Goal

```typescript
const goal = await kairos.goals.create({
  title: 'Q2 Product Release',
  due_date: '2026-06-30',
});
```

### Get Team Information

```typescript
const team = await kairos.team.get();
console.log(`Team: ${team.name}`);

const members = await kairos.team.listMembers();
console.log(`Members: ${members.pagination.total}`);
```

## Error Handling

```typescript
import { Kairos, AuthError, RateLimitError } from '@kairos/sdk';

const kairos = new Kairos();

try {
  const task = await kairos.tasks.get('task_id');
} catch (error) {
  if (error instanceof AuthError) {
    console.error('Invalid API key');
  } else if (error instanceof RateLimitError) {
    console.error(`Rate limited. Wait ${error.retryAfter} seconds`);
  } else {
    console.error('Unknown error:', error.message);
  }
}
```

## Environment Setup

Create a `.env` file:

```env
KAIROS_API_KEY=kairos_sk_your_api_key_here
```

Then in your code:

```typescript
const kairos = new Kairos(); // Automatically reads from .env
```

## TypeScript Support

Full TypeScript definitions are included:

```typescript
import { Kairos, Task, Goal } from '@kairos/sdk';

const kairos = new Kairos();

// Types are automatically inferred
const task: Task = await kairos.tasks.get('task_id');
const goals: Goal[] = (await kairos.goals.list()).data;
```

## Advanced Configuration

```typescript
const kairos = new Kairos({
  apiKey: 'kairos_sk_...',
  baseUrl: 'https://custom.kairos.app/v1', // For on-premise
  timeout: 60000, // 60 second timeout
  maxRetries: 5, // Maximum retries for rate limits
});
```

## More Examples

For more examples and complete API reference, see [README.md](./README.md)
