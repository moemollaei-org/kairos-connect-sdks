# Changelog

All notable changes to the Kairos SDK will be documented in this file.

## [0.1.0] - 2026-04-05

### Added
- Initial release of the official Kairos TypeScript/JavaScript SDK
- Full API coverage for all Kairos endpoints
  - Tasks: list, get, create, update, delete
  - Comments: list comments, add comment to task
  - Goals: list, get, create, update, list tasks
  - Team: get team info, list members
  - Documents: list, get
- Complete TypeScript type definitions
- Comprehensive error handling with typed error classes
  - KairosError (base)
  - AuthError (401)
  - ValidationError (400)
  - ForbiddenError (403)
  - NotFoundError (404)
  - RateLimitError (429) with automatic retry
  - InternalError (500+)
- Automatic rate limit handling with configurable retries
- Zero external dependencies (uses native fetch)
- Support for Node.js 18+, Bun, Deno, and browsers
- Dual module support (ESM + CommonJS)
- API key management via environment variable or config
- Comprehensive documentation with examples
- Full test suite with 25+ test cases
- TypeScript strict mode enabled
- Source maps for debugging

### Features
- **Type Safety**: Full TypeScript support with strict mode
- **Zero Dependencies**: Uses native fetch API
- **Automatic Retries**: Handles 429 rate limits automatically
- **Error Handling**: Typed error classes for all API responses
- **Configuration**: Flexible configuration for different environments
- **Documentation**: Complete README with examples and API reference
- **Testing**: Comprehensive test suite with Vitest
- **Build**: Optimized ESM and CommonJS builds with tsup

### Documentation
- README.md with installation, quick start, and full API reference
- IMPLEMENTATION.md with technical details and architecture
- Inline code comments and JSDoc-style documentation
- Example usage in README for all major features
