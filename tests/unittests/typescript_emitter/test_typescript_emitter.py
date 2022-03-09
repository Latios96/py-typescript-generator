from py_typescript_generator.typescript_emitter.typescript_emitter import (
    TypescriptEmitter,
)
from py_typescript_generator.typescript_model_compiler.ts_enum import TsEnum
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)
from tests.unittests.fixture_classes import ClassFixture, EnumFixture


def _emit_object(ts_object_type: TsObjectType) -> str:
    ts_model = TsModel.of_object_types([ts_object_type])
    return TypescriptEmitter().emit(ts_model)


def _emit_enum(ts_enum: TsEnum) -> str:
    ts_model = TsModel.of_enums([ts_enum])
    return TypescriptEmitter().emit(ts_model)


def test_emit_empty_class(empty_class: ClassFixture) -> None:
    assert (
        _emit_object(empty_class.ts_object_type)
        == """interface EmptyClass {
}
"""
    )


def test_emit_class_with_class_with_empty_class(
    class_with_class_with_empty_class: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_class_with_empty_class.ts_object_type)
        == """interface ClassWithClassWithEmptyClass {
    class_with_empty_class: ClassWithEmptyClass
}
"""
    )


def test_emit_class_with_str_list(class_with_str_list: ClassFixture) -> None:
    assert (
        _emit_object(class_with_str_list.ts_object_type)
        == """interface ClassWithStrList {
    str_list: string[]
}
"""
    )


def test_emit_class_with_str_str_dict(class_with_str_str_dict: ClassFixture) -> None:
    assert (
        _emit_object(class_with_str_str_dict.ts_object_type)
        == """interface ClassWithStrStrDict {
    str_dict: {[index: string]: string}
}
"""
    )


def test_emit_class_with_empty_class_list(
    class_with_empty_class_list: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_empty_class_list.ts_object_type)
        == """interface ClassWithEmptyClassList {
    empty_class_list: EmptyClass[]
}
"""
    )


def test_emit_class_with_optional_int(class_with_optional_int: ClassFixture) -> None:
    assert (
        _emit_object(class_with_optional_int.ts_object_type)
        == """interface ClassWithOptionalInt {
    value: number | undefined
}
"""
    )


def test_emit_class_with_optional_empty_class(
    class_with_optional_empty_class: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_optional_empty_class.ts_object_type)
        == """interface ClassWithOptionalEmptyClass {
    value: EmptyClass | undefined
}
"""
    )


def test_emit_simple_int_enum(simple_int_enum: EnumFixture) -> None:
    assert (
        _emit_enum(simple_int_enum.ts_enum)
        == """enum SimpleIntEnum {
    FIRST = 0,
    SECOND = 1,
}
"""
    )


def test_emit_simple_str_enum(simple_str_enum: EnumFixture) -> None:
    assert (
        _emit_enum(simple_str_enum.ts_enum)
        == """enum SimpleStrEnum {
    FIRST = "FIRST",
    SECOND = "SECOND",
}
"""
    )
