# AGENTS.md

# ForkFlow Agent Guide

This file defines how AI coding agents must work inside the ForkFlow repository.

ForkFlow is a production-like educational microservice project: a social network for developers.
The goal is not only to make features work, but to learn and demonstrate Middle-level backend engineering practices: FastAPI, async Python, PostgreSQL, SQLAlchemy 2, Alembic, Redis, Kafka, RabbitMQ, Celery, gRPC, KrakenD, Prometheus, Grafana, clean architecture, testing, observability, and high-load thinking.

The agent must optimize routine work, but the architecture and final decisions belong to the human developer.

---

## 1. Core working rules

* Do not make large uncontrolled changes.
* Prefer small, reviewable diffs.
* One task should normally produce one focused change.
* Always preserve clean architecture boundaries.
* Do not introduce new production dependencies without explaining why.
* Do not silently change public API contracts.
* Do not silently rename files, services, endpoints, tables, events, or environment variables.
* Do not remove tests to make the build pass.
* Do not weaken validation, authentication, security, or type safety to simplify the task.
* Do not hardcode secrets.
* Do not put real tokens, passwords, private keys, personal data, or production credentials into the repository.
* Do not implement unrelated features while solving the current task.
* If the task is ambiguous, first propose a plan and list assumptions.
* If the task is complex, first inspect the relevant files and produce a short implementation plan before editing code.
* After changing code, summarize what changed, why it changed, and how to verify it.

---

## 2. Project purpose

ForkFlow is a microservice social network for developers.

Main product features:

* user registration and authentication;
* developer profiles;
* posts;
* code snippets;
* tags;
* following/unfollowing users;
* personalized feed;
* comments;
* reactions;
* bookmarks;
* notifications;
* moderation;
* analytics;
* high-load feed experiments.

Main engineering goals:

* demonstrate production-like backend architecture;
* practice PostgreSQL deeply;
* practice async FastAPI and SQLAlchemy 2;
* use Kafka for domain events;
* use RabbitMQ and Celery for background jobs;
* use Redis for cache, rate limiting, idempotency keys, and hot data;
* use gRPC only where it gives a clear benefit;
* use KrakenD as API Gateway;
* add Prometheus metrics, Grafana dashboards, and alerting;
* keep the system understandable and maintainable.

---

## 3. Expected repository layout

Expected high-level structure:

```text
forkflow/
├── services/
│   ├── auth/
│   ├── profile/
│   ├── posts/
│   ├── social_graph/
│   ├── feed/
│   ├── comments/
│   ├── reactions/
│   ├── notifications/
│   ├── analytics/
│   └── moderation/
├── gateway/
│   └── krakend.json
├── proto/
│   ├── auth.proto
│   ├── profile.proto
│   └── social_graph.proto
├── libs/
│   ├── common/
│   ├── observability/
│   └── messaging/
├── infra/
│   ├── docker-compose.yml
│   ├── prometheus/
│   ├── grafana/
│   ├── alertmanager/
│   ├── kafka/
│   ├── rabbitmq/
│   └── postgres/
├── load_tests/
│   ├── k6/
│   └── locust/
├── docs/
│   ├── architecture.md
│   ├── events.md
│   ├── database.md
│   ├── observability.md
│   └── adr/
├── Makefile
├── README.md
└── AGENTS.md
```

Do not create all folders blindly unless the current task requires it. Keep the project incremental.

---

## 4. Service architecture

Each FastAPI service should follow this structure unless the service-specific README says otherwise:

```text
app/
├── main.py
├── config.py
├── domain/
│   ├── entities.py
│   ├── value_objects.py
│   └── exceptions.py
├── application/
│   ├── use_cases/
│   ├── dto.py
│   └── ports.py
├── infrastructure/
│   ├── db/
│   │   ├── models.py
│   │   ├── repositories.py
│   │   └── session.py
│   ├── kafka/
│   ├── redis/
│   ├── grpc/
│   └── celery/
├── presentation/
│   ├── http/
│   │   ├── routes.py
│   │   └── schemas.py
│   └── grpc/
└── tests/
```

Dependency direction:

```text
presentation -> application -> domain
infrastructure -> application/domain through ports/interfaces
domain -> no framework dependencies
```

Rules:

* FastAPI routes must stay thin.
* Business logic belongs in application use cases.
* Domain entities must not depend on FastAPI, SQLAlchemy, Redis, Kafka, or Celery.
* SQLAlchemy models belong to infrastructure.
* Pydantic request/response schemas belong to presentation.
* Repositories belong to infrastructure and implement application ports.
* Do not put database queries directly inside routes.
* Do not put Kafka publishing directly inside route handlers.
* Do not mix HTTP schemas with domain entities.

---

## 5. Technology roles

Use technologies according to their intended role.

### Kafka

Kafka is for domain events and event streaming.

Examples:

```text
UserRegistered
ProfileUpdated
PostCreated
PostUpdated
PostDeleted
UserFollowed
UserUnfollowed
CommentCreated
ReactionAdded
PostViewed
```

Rules:

* Use Kafka when multiple services may react independently to the same domain event.
* Do not use Kafka for simple request/response communication.
* Do not publish events before the database transaction is safely persisted.
* Prefer outbox pattern for important domain events.
* Consumers must be idempotent where possible.

### RabbitMQ and Celery

RabbitMQ and Celery are for background jobs.

Examples:

```text
send_email_notification
send_telegram_notification
generate_user_export
moderate_post
recalculate_user_score
```

Rules:

* Use Celery tasks for work that can happen outside the request lifecycle.
* Configure retries explicitly for unreliable external operations.
* Do not use Celery as a replacement for domain event streaming.
* Do not put critical domain state only inside a Celery task.

### Redis

Redis is for fast temporary data.

Use cases:

```text
feed cache
profile cache
rate limit counters
idempotency keys
hot posts cache
hot tags cache
short-lived token/session state
```

Rules:

* Redis cache must be treated as disposable.
* PostgreSQL remains the source of truth.
* Always define TTL for temporary cache keys unless there is a clear reason not to.
* Use explicit key naming conventions.

### gRPC

gRPC is for internal service-to-service calls where batch or typed contracts help.

Good candidates:

```text
ProfileService.GetProfilesBatch
SocialGraphService.GetFollowees
SocialGraphService.IsFollowing
AuthService.IntrospectToken
```

Rules:

* Do not call gRPC per feed item in a loop.
* Prefer batch methods.
* Avoid building a distributed monolith.
* Prefer domain events for async propagation of state changes.

### KrakenD

KrakenD is the API Gateway.

Responsibilities:

* external HTTP entrypoint;
* routing to internal services;
* basic aggregation when useful;
* rate limiting;
* hiding internal service topology;
* gateway-level auth checks where appropriate.

Rules:

* Do not put business logic into KrakenD.
* Do not make Gateway responsible for domain decisions.

---

## 6. Main services and responsibilities

### Auth Service

Responsibilities:

* registration;
* login;
* password hashing;
* JWT access/refresh tokens;
* sessions;
* logout;
* roles;
* publishing `UserRegistered`.

Database examples:

```text
users
refresh_sessions
roles
user_roles
```

Important rules:

* Never store plaintext passwords.
* Use strong password hashing.
* Email must be unique.
* Token/session invalidation must be explicit.
* Registration must be covered by tests.

---

### Profile Service

Responsibilities:

* developer profile;
* bio;
* skills;
* links;
* avatar URL;
* public profile card;
* gRPC batch profile lookup.

Database examples:

```text
profiles
skills
profile_skills
profile_links
```

Important rules:

* Profile is separate from Auth user credentials.
* Cache public profile data carefully.
* Use batch profile fetching for feed-related scenarios.

---

### Post Service

Responsibilities:

* posts;
* code snippets;
* tags;
* drafts;
* post visibility;
* outbox events.

Database examples:

```text
posts
post_tags
tags
post_code_snippets
post_outbox
```

Important rules:

* Creating a post and writing the outbox event must be one transaction.
* Do not publish Kafka events inside the main transaction.
* Use cursor pagination for post lists.
* Use meaningful PostgreSQL indexes.
* Add tests for post creation and event creation.

---

### Social Graph Service

Responsibilities:

* follow;
* unfollow;
* followers;
* followees;
* blocks;
* gRPC methods for feed service.

Database examples:

```text
follows
blocks
```

Important rules:

* Use unique constraint for `(follower_id, followee_id)`.
* Follow/unfollow should be idempotent where reasonable.
* Avoid race conditions on repeated follow attempts.
* Publish `UserFollowed` and `UserUnfollowed`.

---

### Feed Service

Responsibilities:

* personalized feed;
* cached feed;
* cursor pagination;
* fanout-on-write for normal users;
* fanout-on-read strategy for high-follower users;
* feed item denormalization.

Database examples:

```text
feed_items
user_feed_state
hot_posts
```

Important rules:

* `GET /feed` is a high-load endpoint.
* Prefer cursor pagination.
* Use Redis cache for hot feed pages.
* Avoid N+1 service calls.
* Use denormalized author/post snapshots where useful.
* Measure improvements with load tests and metrics.

---

### Comments Service

Responsibilities:

* comments;
* replies;
* soft delete;
* comment counters;
* publishing comment events.

Database examples:

```text
comments
comment_reactions
```

Important rules:

* Keep tree logic understandable.
* Prefer soft delete for comments.
* Add anti-spam/rate-limit points later.
* Test nested comments carefully.

---

### Reactions Service

Responsibilities:

* likes;
* reactions;
* bookmarks;
* reaction counters.

Database examples:

```text
post_reactions
post_reaction_counters
bookmarks
```

Important rules:

* Reaction operations should be idempotent.
* Use unique constraints to avoid duplicate reactions.
* Denormalized counters are allowed but must be updated safely.
* Publish `ReactionAdded` and `ReactionRemoved`.

---

### Notifications Service

Responsibilities:

* in-app notifications;
* unread counters;
* notification settings;
* consuming Kafka events;
* creating Celery tasks for external delivery.

Database examples:

```text
notifications
notification_settings
```

Important rules:

* Kafka event means “something happened”.
* Celery task means “perform this delivery job”.
* Notification creation should be idempotent.
* External delivery must be retry-safe.

---

### Analytics Service

Responsibilities:

* event consumption;
* post views;
* daily activity;
* popular tags;
* aggregated stats.

Database examples:

```text
post_views
daily_user_activity
daily_tag_stats
```

Important rules:

* Analytics should not block core product flows.
* Prefer batch inserts where useful.
* Use indexes and possibly partitioning for time-based data.
* Keep analytics eventually consistent.

---

### Moderation Service

Responsibilities:

* rule-based content checks;
* stop words;
* suspicious content score;
* moderation cases;
* publishing moderation results.

Database examples:

```text
moderation_cases
blocked_terms
```

Important rules:

* Do not add ML in the first version.
* Start with deterministic rules.
* Keep moderation explainable.

---

## 7. PostgreSQL rules

PostgreSQL is a core learning area in this project.

Always consider:

* schema design;
* constraints;
* indexes;
* transactions;
* query plans;
* migrations;
* data volume;
* locking;
* idempotency;
* pagination.

Preferred patterns:

* UUID primary keys;
* `created_at`;
* `updated_at`;
* soft delete where useful;
* explicit unique constraints;
* composite indexes for common query patterns;
* partial indexes where appropriate;
* GIN indexes where appropriate;
* cursor pagination for high-volume lists;
* outbox table for domain events.

Before adding an index, explain:

* which query it helps;
* expected selectivity;
* expected query plan;
* write overhead;
* whether it duplicates an existing index.

For performance-related changes, prefer evidence:

```text
EXPLAIN
EXPLAIN ANALYZE
load test result
Prometheus metric
```

---

## 8. API rules

General HTTP rules:

* Use `/api/v1/...` externally through the gateway.
* Internal service routes may be simpler but must be documented.
* Use proper HTTP status codes.
* Return consistent error responses.
* Validate request data with Pydantic schemas.
* Do not expose internal database models directly.
* Use pagination for list endpoints.
* Use idempotency keys for operations where duplicate requests are dangerous.

Example error response shape:

```json
{
  "error": {
    "code": "duplicate_email",
    "message": "User with this email already exists",
    "details": {}
  }
}
```

---

## 9. Testing rules

Tests are required for meaningful changes.

Preferred test levels:

* unit tests for domain/application logic;
* integration tests for repositories and database behavior;
* API tests for FastAPI endpoints;
* contract-like tests for important event payloads;
* smoke tests for service health endpoints.

Rules:

* Do not remove tests without explicit reason.
* Do not make tests weaker to pass.
* Mock external systems in unit tests.
* Do not require real Kafka/RabbitMQ in unit tests.
* Use test containers or docker compose only for integration tests where appropriate.
* Every new use case should have at least success and failure tests.
* Every bug fix should include a regression test when practical.

---

## 10. Observability rules

Every service should eventually expose:

```text
/health
/metrics
```

Important metrics:

```text
http_requests_total
http_request_duration_seconds
db_query_duration_seconds
redis_cache_hits_total
redis_cache_misses_total
kafka_messages_consumed_total
kafka_messages_produced_total
celery_tasks_total
outbox_pending_events_total
```

Logging rules:

* Use structured logs where possible.
* Include request ID or correlation ID.
* Do not log secrets.
* Do not log full tokens.
* Do not log plaintext passwords.
* Do not log sensitive user data.

Alerting candidates:

```text
HighErrorRate
P95LatencyTooHigh
PostgresConnectionsHigh
KafkaConsumerLagHigh
CeleryQueueTooLong
OutboxEventsStuck
RedisDown
Gateway5xxSpike
```

---

## 11. Security rules

* Never store plaintext passwords.
* Never commit real secrets.
* Use `.env.example` for documentation.
* Validate all external input.
* Keep authentication and authorization explicit.
* Do not trust user-provided IDs without authorization checks.
* Do not expose stack traces to clients.
* Do not bypass security checks for convenience.
* Be careful with SSRF-like external URL fetching if such features appear later.
* Use rate limiting on sensitive endpoints such as login, registration, password reset, and post creation.

---

## 12. Development workflow

Before implementation:

1. Inspect relevant files.
2. Identify current architecture.
3. Propose a short plan if the task touches more than one layer.
4. Ask for clarification only when necessary.
5. Keep the change scoped.

During implementation:

1. Make the smallest useful change.
2. Preserve naming conventions.
3. Add or update tests.
4. Add or update documentation when behavior changes.
5. Avoid unrelated refactoring.

After implementation:

1. Run relevant tests if possible.
2. Run linter/formatter if configured.
3. Summarize changed files.
4. Explain how to verify manually.
5. Mention any skipped checks honestly.

---

## 13. Common commands

Use these commands when available. If they do not exist yet, suggest adding them instead of inventing one-off workflows.

```bash
make setup
make install
make lint
make format
make test
make up
make down
make logs
```

Service-specific examples:

```bash
make test-auth
make test-posts
make test-feed
make migrate-auth
make migrate-posts
```

Python examples:

```bash
pytest
ruff check .
ruff format .
alembic upgrade head
```

Docker examples:

```bash
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml logs -f
docker compose -f infra/docker-compose.yml down
```

Do not assume these commands exist. Check first.

---

## 14. Definition of Done

A task is done when:

* the requested behavior is implemented;
* clean architecture boundaries are preserved;
* relevant tests are added or updated;
* relevant tests pass, or skipped checks are clearly reported;
* lint/format issues are not introduced;
* public contracts are documented if changed;
* migrations are included when database schema changes;
* new environment variables are added to `.env.example`;
* security implications are considered;
* the final response includes verification steps.

---

## 15. What not to build yet

Do not add these unless explicitly requested:

* Kubernetes;
* service mesh;
* OpenTelemetry tracing;
* Elasticsearch;
* ClickHouse;
* MinIO/S3;
* GraphQL;
* complex frontend;
* real email/SMS providers;
* ML recommendations;
* GitHub OAuth;
* payment systems.

The first goal is a strong backend MVP, not maximum technology count.

---

## 16. MVP priority order

Build in this order unless the human developer changes the roadmap:

1. Repository skeleton.
2. Tooling: Makefile, ruff, pytest, docker compose.
3. Auth Service skeleton.
4. Auth registration.
5. Auth login/JWT.
6. Profile Service.
7. Post Service.
8. Outbox pattern for PostCreated.
9. Kafka integration.
10. Social Graph Service.
11. Feed Service.
12. Redis feed cache.
13. Reactions and Comments.
14. Notifications with RabbitMQ/Celery.
15. Prometheus/Grafana.
16. Load tests.
17. PostgreSQL optimization reports.
18. Documentation and portfolio README.

---

## 17. Human learning rule

This project is also for learning.

When implementing non-trivial code, include a short explanation of:

* why this approach was chosen;
* what alternatives exist;
* what trade-offs were made;
* what could fail in production;
* how the tests prove the behavior;
* what the human developer should understand before moving on.

Do not hide complexity behind generated code.

The human developer should be able to explain every important architectural decision in an interview.

## 18. Git workflow

- For feature PR work, do not commit immediately after implementation.
- After making changes, run relevant checks and show a diff/status summary.
- Wait for explicit human approval before staging or committing.
- Treat commands like "коммить", "закоммить", or "можно коммитить" as explicit approval.

The agent must never run `git add` or `git commit` unless the human explicitly asks to commit the current changes.

## Other
ForkFlow is the current project name.
roadmap.pdf may contain the old DevPulse name and is used only as an architectural reference.
ForkFlow should be used exclusively in all new files, Docker names, directories, documentation, variables, and READMEs.

## Docstrings & comments
Style - Google
Lang - Russian

Project Lang - Russian