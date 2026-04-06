export class KairosError extends Error {
  constructor(
    public readonly code: string,
    public readonly message: string,
    public readonly statusCode: number,
    public readonly requestId?: string,
  ) {
    super(message);
    this.name = 'KairosError';
    Object.setPrototypeOf(this, KairosError.prototype);
  }
}

export class AuthError extends KairosError {
  constructor(message: string, requestId?: string) {
    super('UNAUTHORIZED', message, 401, requestId);
    this.name = 'AuthError';
    Object.setPrototypeOf(this, AuthError.prototype);
  }
}

export class ForbiddenError extends KairosError {
  constructor(message: string, requestId?: string) {
    super('FORBIDDEN', message, 403, requestId);
    this.name = 'ForbiddenError';
    Object.setPrototypeOf(this, ForbiddenError.prototype);
  }
}

export class NotFoundError extends KairosError {
  constructor(message: string, requestId?: string) {
    super('NOT_FOUND', message, 404, requestId);
    this.name = 'NotFoundError';
    Object.setPrototypeOf(this, NotFoundError.prototype);
  }
}

export class RateLimitError extends KairosError {
  constructor(
    message: string,
    public readonly retryAfter: number,
    requestId?: string,
  ) {
    super('RATE_LIMIT_EXCEEDED', message, 429, requestId);
    this.name = 'RateLimitError';
    Object.setPrototypeOf(this, RateLimitError.prototype);
  }
}

export class ValidationError extends KairosError {
  constructor(message: string, requestId?: string) {
    super('VALIDATION_ERROR', message, 400, requestId);
    this.name = 'ValidationError';
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}

export class InternalError extends KairosError {
  constructor(message: string, requestId?: string) {
    super('INTERNAL_ERROR', message, 500, requestId);
    this.name = 'InternalError';
    Object.setPrototypeOf(this, InternalError.prototype);
  }
}
