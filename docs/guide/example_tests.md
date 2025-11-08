# Example Tests 🧩

> **For developers using BuildingBlocks** --- this guide teaches how to
> design and test applications that use BuildingBlocks abstractions.\
> It focuses on *how to test your own code* built with BuildingBlocks,
> not on how the toolkit itself is tested.

Practical examples showing how to test each layer using
**BuildingBlocks**.

------------------------------------------------------------------------

## 🧱 Domain Example --- Entity Behavior

``` python
from __future__ import annotations
from building_blocks.domain import Entity

class User(Entity):
    id: int
    name: str

    @classmethod
    def register(cls, id: int, name: str) -> User:
        return cls(id=id, name=name)

def test_user_identity_equality() -> None:
    user_a = User(id=1, name="Alice")
    user_b = User(id=1, name="Alice")
    assert user_a == user_b
```

------------------------------------------------------------------------

## ⚙️ Application Example --- Use Case

``` python
from dataclasses import dataclass
from building_blocks.application import UseCase
from building_blocks.foundation import Error, Ok, Err, Result

@dataclass(frozen=True)
class DivideNumbersRequest:
    dividend: int
    divisor: int

@dataclass(frozen=True)
class DivideNumbersResponse:
    quotient: int

class DivideNumbersError(Error):
    reason: str

DivideNumbersResult = Result[DivideNumbersResponse, DivideNumbersError]

class DivideNumbersUseCase(UseCase[DivideNumbersRequest, DivideNumbersResult]):
    def execute(self, request: DivideNumbersRequest) -> DivideNumbersResult:
        a, b = request.dividend, request.divisor
        if b == 0:
            return Err(DivideNumbersError("division by zero"))
        return Ok(DivideNumbersResponse(a // b))

def test_divide_numbers_use_case_success() -> None:
    use_case = DivideNumbersUseCase()
    result = use_case.execute(DivideNumbersRequest(10, 2))
    assert result.is_ok()
    assert result.unwrap().quotient == 5
```

------------------------------------------------------------------------

## 🧩 Infrastructure Example --- Repository Adapter

``` python
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

from building_blocks.application import Repository
from building_blocks.domain import Entity

class User(Entity[UUID]):
    def __init__(self, id: UUID, name: str) -> None:
        super().__init__(id or uuid4())
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def register(cls, name: str) -> User:
        return cls(id=uuid4(), name=name)

class UserRepository(Repository[User, UUID], Protocol):
    async def delete_by_id(self, user_id: UUID) -> None:
        ...

    async def get_by_id(self, user_id: UUID) -> User | None:
        ...

    async def list_all(self) -> list[User]:
        ...

    async def save(self, user: User) -> None:
        ...

class InMemoryUserRepository(UserRepository):
    def __init__(self, data: dict[UUID, User]) -> None:
        self._data = data

    async def delete_by_id(self, user_id: int) -> None:
        self._data.pop(user_id, None)

    async def get_by_id(self, user_id: int) -> User | None:
        return self._data.get(user_id)

    async def list_all(self) -> list[User]:
        return list(self._data.values())

    async def save(self, user: User) -> None:
        self._data[user.id] = user


@dataclass(frozen=True)
class RegisterUserRequest:

class RegisterUserUseCase(UseCase[]):
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, name: str) -> User:
        user = User.register(name)
        await self._user_repository.save(user)
        return user


def test_in_memory_user_repository() -> None:
    repo = InMemoryUserRepository()
    user = User(id=1, name="Alice")
    repo.add(user)
    assert repo.get(1) == user
```

------------------------------------------------------------------------

## ✅ Summary

Each layer can be tested independently:

  Layer                Focus
  -------------------- -------------------------------------------
  **Domain**           Pure business logic and invariants
  **Application**      Use cases and orchestration through ports
  **Infrastructure**   Adapters and persistence details

Testing with **BuildingBlocks** enforces clean boundaries and explicit
contracts between layers.
