# Kairos SDK for TypeScript/JavaScript

Official TypeScript/JavaScript SDK for Kairos project management API. Build applications that integrate seamlessly with Kairos task and goal management.

## Features

- Full TypeScript support with complete type definitions
- Zero external dependencies (uses native `fetch`)
- Automatic retry on rate limits
- Comprehensive error handling with typed errors
- Support for Node.js 18+, Bun, Deno, and browsers
- Full API coverage for tasks, goals, team, and documents

## Installation

### npm

```bash
npm install @kairos/sdk
```

### Bun

```bash
bun add @kairos/sdk
```

### pnpm

```bash
pnpm add @kairos/sdk
```

### yarn

```bash
yarn add @kairos/sdk
```

## Quick Start

### Setting up the client

```typescript
import { Kairos } from '@kairos/sdk';

// Initialize with API key from environment or config
const kairos = new Kairos({
  apiKey: 'kairos_sk_your_api_key_here',
});

// Or use KAIROS_API_KEY environment variable
const kairos = new Kairos();
```

### Creating your first task

```typescript
import { Kairos } from '@kairos/sdk';

const kairos = new Kairos();

// Create a new task
const task = await kairos.tasks.create({
  title: 'Build user authentication',
  description: 'Implement JWT-based auth for the API',
  priority: 'high',
  estimated_hours: 8,
  due_date: '2026-04-15',
});

console.log(`Created task: ${task.id}`);
```

### Managing goals

```typescript
const kairos = new Kairos();

// Create a goal
const goal = await kairos.goals.create({
  title: 'Q2 Product Launch',
  description: 'Launch new features for Q2',
  due_date: '2026-06-30',
});

// Get goal details
const goalDetails = await kairos.goals.get(goal.id);
console.log(`Goal progress: ${goalDetails.progress}%`);

// List all active goals
const goals = await kairos.goals.list({ status: 'active' });
console.log(`Active goals: ${goals.data.length}`);
```

### Working with tasks and comments

```typescript
const kairos = new Kairos();

// List tasks with filters
const tasks = await kairos.tasks.list({
  status: 'in_progress',
  priority: 'high',
  limit: 20,
});

// Get a specific task
const task = await kairos.tasks.get('task_123');

// Update a task
const updated = await kairos.tasks.update('task_123', {
  status: 'in_review',
  actual_hours: 5,
});

// Add a comment
const comment = await kairos.tasks.addComment('task_123', {
  content: 'Implementation complete, ready for review',
});

// List task comments
const comments = await kairos.tasks.listComments('task_123');
```

### Team information

```typescript
const kairos = new Kairos();

// Get team details
const team = await kairos.team.get();
console.log(`Team: ${team.name}`);

// List team members
const members = await kairos.team.listMembers({ limit: 50 });
console.log(`Team size: ${members.pagination.total}`);
```

### Managing documents

```typescript
const kairos = new Kairos();

// List documents
const docs = await kairos.documents.list();

// Get a specific document
const doc = await kairos.documents.get('doc_123');
console.log(`Document: ${doc.title}`);
```

### Validating your API key

```typescript
const kairos = new Kairos();

// Verify API key and get user/team info
const me = await kairos.me();
console.log(`Team ID: ${me.team_id}`);
console.log(`Scopes: ${me.scopes.join(', ')}`);
console.log(`Rate limit: ${me.rate_limit_per_minute}/minute`);
```

## API Reference

### Tasks

#### List tasks

```typescript
const response = await kairos.tasks.list({
  status: 'in_progress',
  priority: 'high',
  assigned_to: 'user_123',
  goal_id: 'goal_123',
  search: 'authentication',
  limit: 20,
  offset: 0,
});

console.log(response.data); // Task[]
console.log(response.pagination); // { page, limit, total, has_more }
```

#### Get task by ID

```typescript
const task = await kairos.tasks.get('task_123');
```

#### Create task

```typescript
const task = await kairos.tasks.create({
  title: 'New feature',
  description: 'Description of the feature',
  type: 'task', // 'task' | 'sub_task' | 'bug' | 'story' | 'epic'
  status: 'to_do', // 'to_do' | 'in_progress' | 'in_review' | 'completed' | 'cancelled'
  priority: 'high', // 'low' | 'medium' | 'high' | 'urgent'
  goal_id: 'goal_123', // Optional
  parent_task_id: 'task_parent', // Optional, for sub-tasks
  assigned_to: 'user_123', // Optional
  estimated_hours: 8, // Optional
  due_date: '2026-04-15', // Optional, ISO 8601
});
```

#### Update task

```typescript
const updated = await kairos.tasks.update('task_123', {
  status: 'in_progress',
  actual_hours: 3,
  priority: 'urgent',
});
```

#### Delete task

```typescript
await kairos.tasks.delete('task_123');
```

#### List task comments

```typescript
const comments = await kairos.tasks.listComments('task_123', {
  limit: 10,
  offset: 0,
});
```

#### Add comment

```typescript
const comment = await kairos.tasks.addComment('task_123', {
  content: 'Task complete!',
});
```

### Goals

#### List goals

```typescript
const response = await kairos.goals.list({
  status: 'active', // 'active' | 'completed' | 'archived'
  limit: 20,
  offset: 0,
});
```

#### Get goal by ID

```typescript
const goal = await kairos.goals.get('goal_123');
```

#### Create goal

```typescript
const goal = await kairos.goals.create({
  title: 'Q2 Launch',
  description: 'Launch new features',
  due_date: '2026-06-30', // Optional
});
```

#### Update goal

```typescript
const updated = await kairos.goals.update('goal_123', {
  status: 'completed',
  description: 'Updated description',
});
```

#### List tasks in goal

```typescript
const tasks = await kairos.goals.listTasks('goal_123', {
  status: 'completed',
  limit: 20,
});
```

### Team

#### Get team info

```typescript
const team = await kairos.team.get();
// { id, name, slug, description, avatar_url, created_at }
```

#### List team members

```typescript
const members = await kairos.team.listMembers({
  limit: 50,
  offset: 0,
});
// { data: TeamMember[], pagination: Pagination }
```

### Documents

#### List documents

```typescript
const docs = await kairos.documents.list({
  limit: 20,
  offset: 0,
});
```

#### Get document

```typescript
const doc = await kairos.documents.get('doc_123');
```

## Error Handling

The SDK provides typed error classes for different error scenarios:

```typescript
import {
  Kairos,
  AuthError,
  ForbiddenError,
  NotFoundError,
  RateLimitError,
  ValidationError,
  InternalError,
} from '@kairos/sdk';

const kairos = new Kairos();

try {
  const task = await kairos.tasks.create({
    title: 'New task',
  });
} catch (error) {
  if (error instanceof AuthError) {
    console.error('Invalid API key:', error.message);
  } else if (error instanceof ValidationError) {
    console.error('Validation failed:', error.message);
  } else if (error instanceof RateLimitError) {
    console.error(`Rate limited. Retry after ${error.retryAfter} seconds`);
  } else if (error instanceof NotFoundError) {
    console.error('Resource not found:', error.message);
  } else if (error instanceof ForbiddenError) {
    console.error('Access denied:', error.message);
  } else if (error instanceof InternalError) {
    console.error('Server error:', error.message);
  } else {
    console.error('Unknown error:', error);
  }
}
```

### Error properties

All errors have the following properties:

```typescript
error.code; // 'UNAUTHORIZED' | 'FORBIDDEN' | 'NOT_FOUND' | etc.
error.message; // Human-readable error message
error.statusCode; // HTTP status code
error.requestId; // Unique request ID for debugging

// RateLimitError has additional property:
error.retryAfter; // Seconds to wait before retrying
```

## Rate Limiting

The SDK automatically handles rate limit responses (429) by retrying with exponential backoff. You can configure the maximum number of retries:

```typescript
const kairos = new Kairos({
  apiKey: 'kairos_sk_...',
  maxRetries: 3, // Default is 3
  timeout: 30000, // Default is 30 seconds
});
```

To check current rate limit status after a request:

```typescript
const task = await kairos.tasks.get('task_123');

// Access rate limit info through the HTTP client
// (This is internal, but available if needed)
const rateLimit = await kairos.me(); // Includes rate_limit_per_minute and rate_limit_per_hour
```

## Environment Variables

Set your API key via the `KAIROS_API_KEY` environment variable:

```bash
export KAIROS_API_KEY=kairos_sk_your_api_key_here
```

Then initialize without passing the API key:

```typescript
import { Kairos } from '@kairos/sdk';

const kairos = new Kairos(); // Reads from KAIROS_API_KEY
```

## Configuration

```typescript
interface KairosConfig {
  apiKey?: string; // Defaults to KAIROS_API_KEY env var
  baseUrl?: string; // Defaults to https://gateway.thekairos.app/v1
  timeout?: number; // Request timeout in ms, defaults to 30000
  maxRetries?: number; // Max retries for rate limits, defaults to 3
}
```

## Advanced Usage

### Custom base URL (for on-premise deployments)

```typescript
const kairos = new Kairos({
  apiKey: 'kairos_sk_...',
  baseUrl: 'https://kairos.company.com/api/v1',
});
```

### Longer timeout for slow networks

```typescript
const kairos = new Kairos({
  apiKey: 'kairos_sk_...',
  timeout: 60000, // 60 seconds
});
```

### Disable automatic retries

```typescript
const kairos = new Kairos({
  apiKey: 'kairos_sk_...',
  maxRetries: 0,
});
```

## Type Definitions

All types are exported for TypeScript development:

```typescript
import {
  Task,
  Goal,
  Comment,
  Team,
  TeamMember,
  Document,
  CreateTaskInput,
  UpdateTaskInput,
  CreateGoalInput,
  UpdateGoalInput,
  ListTasksOptions,
  ListGoalsOptions,
  PaginatedResponse,
  SingleResponse,
  MeResponse,
} from '@kairos/sdk';
```

## Browser Usage

The SDK works in modern browsers with support for `fetch`:

```html
<script type="module">
  import { Kairos } from 'https://cdn.example.com/@kairos/sdk/dist/index.js';

  const kairos = new Kairos({
    apiKey: 'kairos_sk_...',
  });

  const tasks = await kairos.tasks.list();
  console.log(tasks);
</script>
```

## License

MIT
