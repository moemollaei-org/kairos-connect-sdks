// Client
export { Kairos, Kairos as default } from './client';

// Resources
export { TasksResource } from './resources/tasks';
export { GoalsResource } from './resources/goals';
export { TeamResource } from './resources/team';
export { DocumentsResource } from './resources/documents';
export { WhiteboardsResource } from './resources/whiteboards';
export { FormsResource } from './resources/forms';

// Types
export type {
  // Tasks
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  TaskAssignee,
  AddTaskAssigneeInput,
  TaskLabel,
  AddTaskLabelInput,
  TaskDependency,
  AddTaskDependencyInput,
  // Goals
  Goal,
  CreateGoalInput,
  UpdateGoalInput,
  // Comments
  Comment,
  CreateCommentInput,
  UpdateCommentInput,
  // Documents
  Document,
  CreateDocumentInput,
  UpdateDocumentInput,
  // Whiteboards
  Whiteboard,
  CreateWhiteboardInput,
  UpdateWhiteboardInput,
  // Forms
  Form,
  FormField,
  CreateFormInput,
  UpdateFormInput,
  FormSubmission,
  // Team
  Team,
  TeamMember,
  // Shared
  Pagination,
  PaginatedResponse,
  SingleResponse,
  // List options
  ListTasksOptions,
  ListGoalsOptions,
  ListDocumentsOptions,
  ListWhiteboardsOptions,
  ListFormsOptions,
  ListOptions,
  // Config
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
