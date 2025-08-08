from typing import Optional

import pytest

from building_blocks.domain.entity import Entity, TransientEntity


class FakeTransientEntity(TransientEntity[int]):
    def __init__(self, id: Optional[int] = None, name: str = ""):
        super().__init__(id)
        self.name = name


class FakeEntity(Entity[str]):
    def __init__(self, id: str, name: str = ""):
        super().__init__(id)
        self.name = name


class TestTransientEntity:
    def test_eq_when_other_entity_with_same_non_none_id_then_true(self) -> None:
        entity1 = FakeTransientEntity(1)
        entity2 = FakeTransientEntity(1)

        result = entity1 == entity2

        assert result is True, "Entities with the same non-None ID should be equal"

    def test_eq_when_one_id_none_then_false(self) -> None:
        entity1 = FakeTransientEntity(1)
        entity2 = FakeTransientEntity(None)

        result = entity1 == entity2

        assert (
            result is False
        ), "Entity with None ID should not be equal to entity with non-None ID"

    def test_eq_when_both_id_none_then_false(self) -> None:
        entity1 = FakeTransientEntity(None)
        entity2 = FakeTransientEntity(None)

        result = entity1 == entity2

        assert result is False, "Entities with None IDs should not be equal"

    def test_eq_when_other_object_then_false(self) -> None:
        entity = FakeTransientEntity(1)
        other_object = object()

        result = entity == other_object

        assert result is False, "Entity should not be equal to a non-entity object"

    def test_is_persisted_when_id_is_none_then_false(self) -> None:
        entity = FakeTransientEntity(None)

        result = entity.is_persisted()

        assert result is False, "Entity with None ID should not be persisted"

    def test_is_persisted_when_id_is_not_none_then_true(self) -> None:
        entity = FakeTransientEntity(42)

        result = entity.is_persisted()

        assert result is True, "Entity with non-None ID should be persisted"

    def test_str_and_repr(self) -> None:
        entity = FakeTransientEntity(7, name="Test")

        str_result = str(entity)
        repr_result = repr(entity)

        expected = "FakeTransientEntity(id=7)"
        assert str_result == expected
        assert repr_result == expected

    def test_hash_when_id_then_hash_id(self) -> None:
        entity = FakeTransientEntity(123)

        result = hash(entity)

        assert result == hash(123)


class TestEntity:
    def test_eq_when_other_entity_with_same_id_then_true(self) -> None:
        entity1 = FakeEntity("abc")
        entity2 = FakeEntity("abc")

        result = entity1 == entity2

        assert result is True, "Entities with the same ID should be equal"

    def test_eq_when_other_entity_with_different_id_then_false(self) -> None:
        entity1 = FakeEntity("abc")
        entity2 = FakeEntity("def")

        result = entity1 == entity2

        assert result is False, "Entities with different IDs should not be equal"

    def test_eq_when_other_object_then_false(self) -> None:
        entity = FakeEntity("abc")
        other_object = object()

        result = entity == other_object

        assert result is False, "Entity should not be equal to a non-entity object"

    def test_str_and_repr(self) -> None:
        entity = FakeEntity("xyz")

        str_result = str(entity)
        repr_result = repr(entity)

        expected = "FakeEntity(id=xyz)"
        assert str_result == expected
        assert repr_result == expected

    def test_hash_when_id_then_hash_id(self) -> None:
        entity = FakeEntity("some-id")

        result = hash(entity)

        assert result == hash("some-id")

    def test_init_when_id_is_none_then_raises(self) -> None:
        with pytest.raises(ValueError, match="Entity ID cannot be None"):
            FakeEntity(None)  # type: ignore
