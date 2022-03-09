from enum import Enum
from typing import Dict

import pytest
from ordered_set import OrderedSet

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_enum import PyEnum
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.typescript_model_compiler import (
    TypescriptModelCompiler,
    UnsupportedKeyTypeForMappedType,
    UnsupportedEnumValue,
)
from tests.unittests.fixture_classes import ClassFixture, EnumFixture


def _compile_py_class(py_class: PyClass) -> TsModel:
    model = Model.of_classes([py_class])
    model_compiler = TypescriptModelCompiler()
    ts_model = model_compiler.compile(model)
    return ts_model


def _compile_py_enum(py_enum: PyEnum) -> TsModel:
    model = Model(enums=OrderedSet([py_enum]))
    model_compiler = TypescriptModelCompiler()
    ts_model = model_compiler.compile(model)
    return ts_model


def test_should_compile_empty_class(empty_class):
    ts_model = _compile_py_class(empty_class.py_class)

    assert ts_model == TsModel.of_object_types([empty_class.ts_object_type])


def test_should_compile_class_with_empty_class(class_with_empty_class):
    ts_model = _compile_py_class(class_with_empty_class.py_class)

    assert ts_model == TsModel.of_object_types([class_with_empty_class.ts_object_type])


def test_should_compile_class_with_class_with_empty_class(
    class_with_class_with_empty_class,
):
    ts_model = _compile_py_class(class_with_class_with_empty_class.py_class)

    assert ts_model == TsModel.of_object_types(
        [class_with_class_with_empty_class.ts_object_type]
    )


def test_should_compile_classes_with_cycle(first_class_in_cycle, second_class_in_cycle):
    model = Model.of_classes(
        [first_class_in_cycle.py_class, second_class_in_cycle.py_class]
    )
    model_compiler = TypescriptModelCompiler()

    ts_model = model_compiler.compile(model)

    assert ts_model == TsModel.of_object_types(
        [first_class_in_cycle.ts_object_type, second_class_in_cycle.ts_object_type]
    )


@pytest.mark.parametrize(
    "fixture_name",
    [
        "class_with_int",
        "class_with_str",
        "class_with_float",
        "class_with_bool",
        "class_with_bytes",
        "class_with_datetime",
        "class_with_uuid",
    ],
)
def test_should_compile_class_with_scalar_types(fixture_name, request):
    class_fixture = request.getfixturevalue(fixture_name)
    ts_model = _compile_py_class(class_fixture.py_class)

    assert ts_model == TsModel.of_object_types([class_fixture.ts_object_type])


def test_should_compile_class_with_optional_int(class_with_optional_int):
    ts_model = _compile_py_class(class_with_optional_int.py_class)

    assert ts_model == TsModel.of_object_types([class_with_optional_int.ts_object_type])


def test_should_compile_class_with_optional_empty_class(
    class_with_optional_empty_class,
):
    ts_model = _compile_py_class(class_with_optional_empty_class.py_class)

    assert ts_model == TsModel.of_object_types(
        [class_with_optional_empty_class.ts_object_type]
    )


class TestTypesMappedToArray:
    def test_should_compile_class_with_str_list(self, class_with_str_list):
        ts_model = _compile_py_class(class_with_str_list.py_class)

        assert ts_model == TsModel.of_object_types([class_with_str_list.ts_object_type])

    def test_should_compile_class_with_str_set(self, class_with_str_set):
        ts_model = _compile_py_class(class_with_str_set.py_class)

        assert ts_model == TsModel.of_object_types([class_with_str_set.ts_object_type])

    def test_should_compile_class_with_str_frozen_set(self, class_with_str_frozen_set):
        ts_model = _compile_py_class(class_with_str_frozen_set.py_class)

        assert ts_model == TsModel.of_object_types(
            [class_with_str_frozen_set.ts_object_type]
        )

    def test_should_compile_class_with_str_ordered_set(
        self, class_with_str_ordered_set
    ):
        ts_model = _compile_py_class(class_with_str_ordered_set.py_class)

        assert ts_model == TsModel.of_object_types(
            [class_with_str_ordered_set.ts_object_type]
        )

    def test_should_compile_class_with_optional_empty_class(
        self, class_with_optional_empty_class: ClassFixture
    ) -> None:
        ts_model = _compile_py_class(class_with_optional_empty_class.py_class)

        assert ts_model == TsModel.of_object_types(
            [class_with_optional_empty_class.ts_object_type]
        )


class TestTypesMappedToObject:
    def test_should_fail_if_key_type_is_not_str(self):
        class ClassWithIntStrDict:
            pass

        py_class = PyClass(
            name="ClassWithIntStrDict",
            type=ClassWithIntStrDict,
            fields=frozenset({PyField(name="int_dict", type=Dict[int, str])}),
        )
        with pytest.raises(UnsupportedKeyTypeForMappedType):
            _compile_py_class(py_class)

    def test_should_compile_str_str_dict(
        self, class_with_str_str_dict: ClassFixture
    ) -> None:
        ts_model = _compile_py_class(class_with_str_str_dict.py_class)

        assert ts_model == TsModel.of_object_types(
            [class_with_str_str_dict.ts_object_type]
        )

    def test_should_compile_str_str_default_dict(
        self, class_with_str_str_default_dict: ClassFixture
    ) -> None:
        ts_model = _compile_py_class(class_with_str_str_default_dict.py_class)

        assert ts_model == TsModel.of_object_types(
            [class_with_str_str_default_dict.ts_object_type]
        )

    def test_should_compile_str_str_ordered_dict(
        self, class_with_str_str_ordered_dict: ClassFixture
    ) -> None:
        ts_model = _compile_py_class(class_with_str_str_ordered_dict.py_class)

        assert ts_model == TsModel.of_object_types(
            [class_with_str_str_ordered_dict.ts_object_type]
        )


class TestCompileEnum:
    def test_should_compile_int_enum(self, simple_int_enum: EnumFixture) -> None:
        ts_model = _compile_py_enum(simple_int_enum.py_enum)

        assert ts_model == TsModel.of_enums([simple_int_enum.ts_enum])

    def test_should_compile_str_enum(self, simple_str_enum: EnumFixture) -> None:
        ts_model = _compile_py_enum(simple_str_enum.py_enum)

        assert ts_model == TsModel.of_enums([simple_str_enum.ts_enum])

    def test_compile_enum_with_non_str_int_values_should_fail(self) -> None:
        class MyEnum(Enum):
            pass

        py_enum = PyEnum(name="test", type=MyEnum, values=frozenset([(1,), 1]))

        with pytest.raises(UnsupportedEnumValue):
            _compile_py_enum(py_enum)
