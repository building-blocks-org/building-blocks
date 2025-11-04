from collections.abc import Hashable

from building_blocks.domain.value_object import ValueObject


class FakeValueObject(ValueObject):
    """A fake value object for testing purposes.

    This class is used to create a mock value object with equality components.
    It inherits from the ValueObject class and implements the required methods.
    """

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)


class EmptyValueObject(ValueObject):
    @property
    def value(self) -> None:
        return None

    def _equality_components(self) -> tuple[Hashable, ...]:
        return ()


class MultiValueObject(ValueObject):
    def __init__(self, value1: str, value2: int):
        self._value1 = value1
        self._value2 = value2

    @property
    def value(self) -> tuple[str, int]:
        return (self._value1, self._value2)

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value1, self._value2)


class TestValueObject:
    def test_eq_when_another_value_object_with_same_value_then_true(self):
        vo1 = FakeValueObject("test")
        vo2 = FakeValueObject("test")

        result = vo1 == vo2

        expected_result = True
        assert result is expected_result, "Value objects with the same value should be equal"

    def test_eq_when_different_value_object_with_same_value_then_false(self):
        class DifferentFakeValueObject(ValueObject):
            """A different fake value object for testing purposes.

            This class is used to create a mock value object with a different equality
            component.
            It inherits from the ValueObject class and implements the required methods.
            """

            def __init__(self, value: str):
                self._value = value

            @property
            def value(self) -> str:
                return self._value

            def _equality_components(self) -> tuple[Hashable, ...]:
                return (self._value,)

        vo1 = FakeValueObject("test")
        vo2 = DifferentFakeValueObject("test")

        result = vo1 == vo2

        expected_result = False
        assert result is expected_result, "Value objects with the same value should be equal"

    def test_eq_when_another_value_object_with_different_value_then_false(self):
        vo1 = FakeValueObject("test1")
        vo2 = FakeValueObject("test2")

        result = vo1 == vo2

        expected_result = False
        assert result is expected_result, "Value objects with different values should not be equal"

    def test_eq_when_another_object_then_false(self):
        vo = FakeValueObject("test")
        other_object = object()

        result = vo == other_object

        expected_result = False
        assert result is expected_result, "Value object should not be equal to a non-value object"

    def test_str_representation(self):
        vo = FakeValueObject("test")

        result = str(vo)

        expected_result = "FakeValueObject(test)"
        assert result == expected_result, f"String representation should be '{expected_result}'"

    def test_repr_representation(self):
        vo = FakeValueObject("test")

        result = repr(vo)

        expected_result = "FakeValueObject(test)"
        assert result == expected_result, f"Repr representation should be '{expected_result}'"

    def test_hash_when_value_then_hash_value(self):
        value = "test"
        vo = FakeValueObject(value)

        result = hash(vo)

        print("*" * 20)
        print(f"Debug result: {repr(result)}")
        print("*" * 20)
        expected_hash = hash((value,))  # note the tuple to ensure consistent hashing
        result_assertion = result == expected_hash
        assert result_assertion, "Hash values should be eql for VOs with the same value"

    def test_hash_when_different_value_then_different_hash(self):
        value1 = "test1"
        value2 = "test2"
        vo1 = FakeValueObject(value1)
        vo2 = FakeValueObject(value2)

        hash1 = hash(vo1)
        hash2 = hash(vo2)

        result_assertion = hash1 != hash2
        assert result_assertion, "Hash values should be diff for VOs with diff values"

    def test_str_when_no_value_then_empty_string(self):
        vo = EmptyValueObject()

        result = str(vo)

        expected_result = "EmptyValueObject()"
        assert result == expected_result, f"String representation should be '{expected_result}'"

    def test_repr_when_no_value_then_empty_string(self):
        vo = EmptyValueObject()

        result = repr(vo)

        expected_result = "EmptyValueObject()"
        assert result == expected_result, f"Repr representation should be '{expected_result}'"

    def test_str_when_multiple_values_then_tuple_representation(self):
        vo = MultiValueObject("test", 42)

        # Debug the components
        components = vo._equality_components()
        print(f"Components: {components}")
        print(f"Length: {len(components)}")

        result = str(vo)
        print(f"Actual result: {repr(result)}")

        expected_result = "MultiValueObject('test', 42)"
        assert result == expected_result, f"String representation should be '{expected_result}'"
