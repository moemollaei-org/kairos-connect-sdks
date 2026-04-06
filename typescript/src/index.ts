// Client
export { Kairos, Kairos as default } from './client';

// Resources
export { TasksResource } from './resources/tasks';
export { GoalsResource } from './resources/goals';
export { TeamResource } from './resources/team';
export { DocumentsResource } from './resources/documents';

// Types
export type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  Goal,
  CreateGoalInput,
  UpdateGoalInput,
  Comment,
  CreateCommentInput,
  Team,
  TeamMember,
  Document,
  Pagination,
  PaginatedResponse,
  SingleResponse,
  ListTasksOptions,
  ListGoalsOptions,
  ListOptions,
  MeResponse,
  KairosConfig,
  RateLimitInfo,
} from './types';

// Errors
export {
  KairosError,
  AuthError,
  ForbiddenError,
  NotFoundError,
  RateLimitError,
  ValidationError,
  InternalError,
} from './errors';
