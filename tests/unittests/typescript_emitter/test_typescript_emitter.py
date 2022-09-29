from typing import List

from py_typescript_generator.typescript_emitter.typescript_emitter import (
    TypescriptEmitter,
)
from py_typescript_generator.typescript_model_compiler.ts_enum import TsEnum
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
    TsBaseType,
)
from tests.unittests.fixture_classes import ClassFixture, EnumFixture


def _emit_object(ts_object_type: TsObjectType) -> str:
    ts_model = TsModel.of_types([ts_object_type])
    return TypescriptEmitter().emit(ts_model)


def _emit_objects(ts_base_types: List[TsBaseType]) -> str:
    ts_model = TsModel.of_types(ts_base_types)
    return TypescriptEmitter().emit(ts_model)


def _emit_enum(ts_enum: TsEnum) -> str:
    ts_model = TsModel.of_enums([ts_enum])
    return TypescriptEmitter().emit(ts_model)


def test_emit_empty_class(empty_class: ClassFixture) -> None:
    assert (
        _emit_object(empty_class.ts_object_type)
        == """export interface EmptyClass {
}
"""
    )


def test_emit_class_with_class_with_empty_class(
    class_with_class_with_empty_class: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_class_with_empty_class.ts_object_type)
        == """export interface ClassWithClassWithEmptyClass {
    class_with_empty_class: ClassWithEmptyClass
}
"""
    )


def test_emit_class_with_str_list(class_with_str_list: ClassFixture) -> None:
    assert (
        _emit_object(class_with_str_list.ts_object_type)
        == """export interface ClassWithStrList {
    str_list: string[]
}
"""
    )


def test_emit_class_with_str_str_dict(class_with_str_str_dict: ClassFixture) -> None:
    assert (
        _emit_object(class_with_str_str_dict.ts_object_type)
        == """export interface ClassWithStrStrDict {
    str_dict: {[index: string]: string}
}
"""
    )


def test_emit_class_with_empty_class_list(
    class_with_empty_class_list: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_empty_class_list.ts_object_type)
        == """export interface ClassWithEmptyClassList {
    empty_class_list: EmptyClass[]
}
"""
    )


def test_emit_class_with_optional_int(class_with_optional_int: ClassFixture) -> None:
    assert (
        _emit_object(class_with_optional_int.ts_object_type)
        == """export interface ClassWithOptionalInt {
    value?: number
}
"""
    )


def test_emit_class_with_optional_empty_class(
    class_with_optional_empty_class: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_optional_empty_class.ts_object_type)
        == """export interface ClassWithOptionalEmptyClass {
    value?: EmptyClass
}
"""
    )


def test_emit_class_with_class_with_list_of_optional_int(
    class_with_list_of_optional_int: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_list_of_optional_int.ts_object_type)
        == """export interface ClassWithListOfOptionalInt {
    value: (number | undefined)[]
}
"""
    )


def test_emit_class_with_class_with_list_of_optional_empty_class(
    class_with_list_of_optional_empty_class: ClassFixture,
) -> None:
    assert (
        _emit_object(class_with_list_of_optional_empty_class.ts_object_type)
        == """export interface ClassWithListOfOptionalEmptyClass {
    value: (EmptyClass | undefined)[]
}
"""
    )


def test_emit_simple_int_enum(simple_int_enum: EnumFixture) -> None:
    assert (
        _emit_enum(simple_int_enum.ts_enum)
        == """export enum SimpleIntEnum {
    FIRST = 0,
    SECOND = 1,
}
"""
    )


def test_emit_simple_str_enum(simple_str_enum: EnumFixture) -> None:
    assert (
        _emit_enum(simple_str_enum.ts_enum)
        == """export enum SimpleStrEnum {
    FIRST = "FIRST",
    SECOND = "SECOND",
}
"""
    )


# parse without children
# parent & child, parse parent
# parent & child, parse child


class TestEmitDiscriminantUnion:
    def test_no_children(self, class_with_tagged_union_discriminant_but_no_children):
        assert (
            _emit_object(
                class_with_tagged_union_discriminant_but_no_children.ts_object_type
            )
            == """export type ClassWithTaggedUnionDiscriminantSingleChild = {};
"""
        )

    def test_single_child_emit_root(
        self, class_with_tagged_union_discriminant_single_child
    ):
        assert (
            _emit_object(
                class_with_tagged_union_discriminant_single_child.ts_object_type
            )
            == """export type ClassWithTaggedUnionDiscriminantSingleChild = ClassWithTaggedUnionDiscriminantSingleChildChild;
"""
        )

    def test_multiple_children_emit_root(
        self, class_with_tagged_union_discriminant_multiple_children
    ):
        assert (
            _emit_object(
                class_with_tagged_union_discriminant_multiple_children.ts_object_type
            )
            == """export type ClassWithTaggedUnionDiscriminantMultipleChildren = ClassWithTaggedUnionDiscriminantMultipleChildrenChild1 | ClassWithTaggedUnionDiscriminantMultipleChildrenChild2;
"""
        )

    def test_single_child_emit_child(
        self, class_with_tagged_union_discriminant_single_child_child
    ):
        assert (
            _emit_object(
                class_with_tagged_union_discriminant_single_child_child.ts_object_type
            )
            == """export interface ClassWithTaggedUnionDiscriminantSingleChildChild {
    type: "CHILD"
}
"""
        )
