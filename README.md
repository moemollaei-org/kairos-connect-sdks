# Kairos SDKs

Official SDKs for the [Kairos](https://thekairos.app) API. All SDKs target `gateway.thekairos.app/v1`.

| SDK | Package | Docs |
|-----|---------|------|
| [TypeScript / JavaScript](./typescript) | [`@kairos/sdk`](https://www.npmjs.com/package/@kairos/sdk) | [Docs](https://thekairos.app/docs/sdks/javascript) |
| [Python](./python) | [`kairos-sdk`](https://pypi.org/project/kairos-sdk/) | [Docs](https://thekairos.app/docs/sdks/python) |
| [Go](./go) | [`github.com/moemollaei-org/kairos-connect-sdks/go`](https://pkg.go.dev/github.com/moemollaei-org/kairos-connect-sdks/go) | [Docs](https://thekairos.app/docs/sdks/go) |

## Quick start

### TypeScript / JavaScript

```bash
npm install @kairos/sdk
# or
bun add @kairos/sdk
```

```ts
import { Kairos } from '@kairos/sdk';

const kairos = new Kairos({ apiKey: 'kairos_sk_...' });
const tasks = await kairos.tasks.list();
```

### Python

```bash
pip install kairos-sdk
# or
uv add kairos-sdk
```

```python
from kairos import Kairos

kairos = Kairos(api_key="kairos_sk_...")
tasks = await kairos.tasks.list()
```

### Go

```bash
go get github.com/moemollaei-org/kairos-connect-sdks/go
```

```go
import kairos "github.com/moemollaei-org/kairos-connect-sdks/go"

client := kairos.New("kairos_sk_...")
tasks, err := client.Tasks.List(ctx, nil)
```

## Releasing

Each SDK is versioned independently using prefixed git tags:

| SDK | Tag format | Example |
|-----|-----------|---------|
| TypeScript | `typescript/vX.Y.Z` | `typescript/v1.0.0` |
| Python | `python/vX.Y.Z` | `python/v1.0.0` |
| Go | `go/vX.Y.Z` | `go/v1.0.0` |

Pushing a tag triggers the corresponding publish workflow automatically.

```bash
# Release TypeScript SDK
git tag typescript/v0.1.0 && git push --tags

# Release Python SDK
git tag python/v0.1.0 && git push --tags

# Release Go SDK
git tag go/v0.1.0 && git push --tags
```

## Repository structure

```
kairos-sdks/
├── typescript/   # @kairos/sdk — zero-dep, ESM + CJS, Vitest
├── python/       # kairos-sdk — httpx + Pydantic v2, async + sync
└── go/           # stdlib only, context-aware, options pattern
```

## Contributing

All SDKs live in this repo. CI runs automatically on every push and PR,
testing all three SDKs in parallel.
