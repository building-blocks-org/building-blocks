# Domain Layer 🧠

The **domain layer** is the heart of your business logic.
It is completely independent of frameworks, databases, and other technical concerns.
This layer models your problem space using core DDD patterns: **Entities, Value Objects, Domain Events, Aggregates, Repositories, and Domain Services**.

---

## 📁 Directory Structure

```
domain/
├── aggregate_root.py            # Base class for aggregate roots
├── domain_error.py              # Base class for domain-specific exceptions
├── entity.py                    # Base class for entities with identity
├── value_object.py              # Base class for value objects (immutables)
├── messages/
│   ├── message.py               # Base class for messages (commands/events)
│   ├── command.py               # Base class for domain commands
│   └── event.py                 # Base class for domain events
├── ports/
│   ├── inbound/                 # Interfaces for domain services (rare)
│   └── outbound/
│       ├── aggregate_repository.py    # Aggregate repository abstraction
│       ├── read_only_repository.py    # Read-only repository interface
│       ├── repository.py              # Generic repository interface
│       └── write_only_repository.py   # Write-only repository interface
├── services/                    # Domain service implementations (optional)
└── README.md                    # This documentation
```

---

## ✨ Core Concepts

### 1. **Entities**
- Objects defined by their unique identity and encapsulated logic.
- Inherit from `Entity`.

### 2. **Value Objects**
- Immutable, equality-by-value.
- Inherit from `ValueObject`.

### 3. **Aggregate Roots**
- Entities that control a cluster of domain objects and enforce invariants.
- Inherit from `AggregateRoot`.

### 4. **Domain Events & Commands**
- **Events:** Things that have happened (immutable, recordable).
- **Commands:** Requests for actions (intent, not result).
- All inherit from `Message` (specialized as `Command` or `Event`).

### 5. **Repositories (Outbound Ports)**
- Abstract persistence contracts defined by the domain.
- Found in `ports/outbound/`.
- Types:
  - `Repository`: Generic CRUD (create, read, update, delete)
  - `ReadOnlyRepository`: Only read operations
  - `WriteOnlyRepository`: Only write operations
  - `AggregateRepository`: For aggregate roots

### 6. **Domain Exceptions**
- Custom error types unique to domain logic.
- Inherit from `DomainException`.

### 7. **Domain Services**
- Stateless operations that don’t fit naturally inside an entity or value object.
- Place interfaces (if any) in `ports/inbound/`, implementations in `services/`.

---

## 🧩 How to Use

1. **Define Entities and Value Objects**
   Extend `Entity` and `ValueObject` to model your business concepts.

   ```python
   from building_blocks.domain.entity import Entity

   class User(Entity):
       def __init__(self, user_id: str, email: str):
           super().__init__(user_id)
           self.email = email
   ```

2. **Model Aggregates**
   Use `AggregateRoot` for your aggregate boundaries.

3. **Raise Domain Events**
   Create subclasses of `Event` and use them to communicate important business changes.

4. **Define Outbound Ports (Repositories)**
   Specify repository interfaces in `ports/outbound/`.

   ```python
   from building_blocks.application.ports.outbound.repository import Repository

   class UserRepository(Repository[User, str]):
         def find_by_email(self, email: str) -> User | None:
              """Find a user by email."""
              pass

         def save(self, user: User) -> None:
              """Save a user."""
              pass

        def delete(self, user: User) -> None:
            """Delete a user."""
            pass
   ```

5. **Handle Domain Exceptions**
   Raise custom exceptions for domain-specific errors.

6. **Domain Services**
   Add stateless business logic here if it doesn’t belong to an entity/aggregate.

---

## 🛡️ Testing Guidelines

- Use AAA (Arrange, Act, Assert) pattern.
- Name test classes as `Test<ClassName>`.
- Name test methods as `test_<method>_when_<scenario>_then_<result>`.
- One action (Act) per test.
- Use mocks for outbound ports (repositories, etc.).
- Avoid mocks for pure domain logic.

---

## 🧑‍💻 Extending the Domain Layer

- **Add new entities or value objects** as your domain grows.
- **Add outbound ports** for new persistence or integration needs.
- **Add domain services** for complex business rules.
- **Never** import infrastructure, application, or framework code here!

---

## 🏗️ Why This Matters

- **Independence:** Domain logic stays pure and reusable.
- **Testability:** Easy, fast, isolated tests.
- **Maintainability:** Clear separation of business rules from technical detail.

---

**For more examples and full documentation, see the project root [README](../../README.md) or the `/docs` directory.**
