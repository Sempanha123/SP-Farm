# SP-Farm V2 — Architecture & Dependency Rules

This document defines the formal architecture layers, dependency boundaries, CQRS patterns, and communication rules for SP-Farm V2.

---

## 1. High-Level Layered Model

SP-Farm V2 is structured into five distinct, strictly bounded layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  (PySide6 UI, Views, Tables, Dialogs, Cute Light Theme)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Dispatches Commands / Queries
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
│  (CQRS Buses, Workflows, Handlers, Orchestrators, Events)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ Operates on Domain Entities
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       Domain Layer                          │
│  (Pure Entities, Value Objects, Domain Rules, Interfaces)   │
└──────────────────────────────▲──────────────────────────────┘
                               │ Implements Interfaces
┌──────────────────────────────┴──────────────────────────────┐
│                    Infrastructure Layer                     │
│  (SQLAlchemy 2, SQLite WAL, Secrets Vault, ADB, Appium)     │
└─────────────────────────────────────────────────────────────┘
                               ▲
                               │ Supervised concurrency
┌──────────────────────────────┴──────────────────────────────┐
│                       Workers Layer                         │
│  (Supervisor, Multi-Device Pool, Async Background Jobs)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Layer Definitions & Responsibilities

### Domain Layer (`src/spfarm/domain/`)
- **Responsibility**: Houses business entities, aggregates, domain rules, and abstract interfaces (such as `IUnitOfWork` and repository protocols).
- **Dependency Rule**: **Zero external framework dependencies**. Domain MUST NOT import `PySide6`, `sqlalchemy`, `requests`, `urllib`, `appium`, or `subprocess`.
- **Pure Python**: Testable in isolation without mocking UI or database drivers.

### Application Layer (`src/spfarm/application/`)
- **Responsibility**: Coordinates use-case execution, enforces transactional boundaries, dispatches CQRS commands/queries, and publishes domain events.
- **Dependency Rule**: Coordinates domain models and infrastructure interfaces. Must not depend on `PySide6` or concrete UI widgets.

### Infrastructure Layer (`src/spfarm/infrastructure/`)
- **Responsibility**: Implements external concerns, database repositories (`SQLAlchemy 2`), secure vaulting (`keyring`, `cryptography`), device control (`ADB`, `Appium`), and external Meta/HTTP APIs.
- **Dependency Rule**: Implements domain interfaces. Never leaks raw SQL or ADB handles to the presentation layer.

### Presentation Layer (`src/spfarm/presentation/`)
- **Responsibility**: Handles user interaction, rendering views, tables (`QTableView`), inspectors, and styling with the Cute Light Design System.
- **Dependency Rule**: **No business logic in views**. Presentation communicates exclusively through Application `CommandBus` and `QueryBus`. Presentation NEVER directly calls SQL, subprocess, ADB, or Appium.

### Workers Layer (`src/spfarm/workers/`)
- **Responsibility**: Manages background asynchronous execution, device pool concurrency, persistent job execution, and worker life cycles.
- **Dependency Rule**: Reports status back to the presentation layer via Qt signals and the application `EventBus`.

---

## 3. Communication Patterns

### CQRS (Command Query Responsibility Segregation)
- **Commands** (`Command`): State-mutating operations. Handled by `CommandHandler[C, R]`, returning `Result[R, AppError]`.
- **Queries** (`Query`): Side-effect-free data retrieval operations. Handled by `QueryHandler[Q, R]`, returning `Result[R, AppError]`.

### Decoupled Messaging via EventBus
- Asynchronous and domain state changes emit typed `Event` objects.
- Components subscribe to specific event types via `EventBus.subscribe(EventType, handler)`.
- Prevents direct coupling between worker threads, database triggers, and UI refresh cycles.

### Explicit Error Handling: `Result[T, E]`
- Exceptions are not leaked across layer boundaries for routine business failures.
- Methods return `Success(value)` or `Failure(error)` using `spfarm.shared.result.Result`.
- Errors inherit from `spfarm.shared.errors.AppError` with standardized error codes and correlation IDs.

---

## 4. Automated Architectural Enforcement

The architectural boundaries defined above are continuously validated via automated AST tests (`tests/unit/test_architecture_rules.py`).
Any commit introducing forbidden imports (e.g. importing `sqlalchemy` in `domain/` or `PySide6` in `application/`) will fail CI checks immediately.
