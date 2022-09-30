from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Type, Optional, Tuple, cast, Dict
from uuid import UUID

from caseconverter import camelcase  # type: ignore
from ordered_set import OrderedSet
from typing_extensions import get_args
from typing_inspect import is_optional_type, get_origin  # type: ignore

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass, RootTaggedUnionInformation
from py_typescript_generator.model.py_enum import PyEnum
from py_typescript_generator.typescript_model_compiler.ts_array import TsArray
from py_typescript_generator.typescript_model_compiler.ts_enum import (
    TsEnum,
    TsEnumValue,
)
from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_mapped_type import (
    TsMappedType,
)
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
    TsDiscriminator,
    TsBaseType,
    TsUnionType,
)
from py_typescript_generator.typescript_model_compiler.ts_type import TsType
from py_typescript_generator.typescript_model_compiler.well_known_types import (
    TS_NUMBER,
    TS_STRING,
    TS_BOOLEAN,
)


class UnsupportedGenericParameterCount(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UnsupportedKeyTypeForMappedType(RuntimeError):
    def __init__(self, cls: Type) -> None:
        super().__init__(
            f"The type {cls} is not supported as a key for a mapped type since JSON only supports string keys."
        )


class UnsupportedEnumValue(RuntimeError):
    def __init__(self, cls: Type) -> None:
        super().__init__(
            f"Typescript enums only support int and string values, provided type was {cls}."
        )


class CaseFormat(Enum):
    KEEP_CASING = "KEEP_CASING"
    CAMEL_CASE = "CAMEL_CASE"


@dataclass
class TypescriptModelCompilerSettings:
    field_case_format: CaseFormat = CaseFormat.KEEP_CASING
    type_mapping_overrides: Dict[Type, Type] = field(default_factory=dict)


class TypescriptModelCompiler:
    def __init__(self, typescript_compiler_settings: TypescriptModelCompilerSettings):
        self.typescript_compiler_settings = typescript_compiler_settings

    def compile(self, model: Model) -> TsModel:
        types: OrderedSet[TsBaseType] = OrderedSet()
        for py_class in model.classes:
            types.append(self._compile_class(py_class))

        enums: OrderedSet[TsEnum] = OrderedSet()
        for py_enum in model.enums:
            enums.append(self._compile_enum(py_enum))

        return TsModel(types=types, enums=enums)

    def _compile_class(self, py_class: PyClass) -> TsBaseType:
        if py_class.tagged_union_information and isinstance(
            py_class.tagged_union_information, RootTaggedUnionInformation
        ):
            return TsUnionType(
                name=py_class.name,
                union_members=tuple(
                    x.__name__ for x in py_class.tagged_union_information.child_types
                ),
            )
        fields = []
        for py_field in py_class.fields:
            fields.append(
                TsField(
                    name=self._adjust_casing(py_field.name),
                    type=self._compile_type(py_field.type),
                )
            )
        if not py_class.tagged_union_information:
            return TsObjectType(name=py_class.name, fields=tuple(fields))
        return TsObjectType(
            name=py_class.name,
            fields=tuple(fields),
            discriminator=TsDiscriminator(
                name=self._adjust_casing(
                    py_class.tagged_union_information.discriminant_attribute
                ),
                value=py_class.tagged_union_information.discriminant_literal,
            ),
        )

    def _compile_type(self, cls: Type, optional: bool = False) -> TsType:
        type_override = self.typescript_compiler_settings.type_mapping_overrides.get(
            cls
        )
        if type_override:
            return self._compile_type(type_override, optional)
        mapped_type = self._map_scalar_type(cls)
        if mapped_type:
            return mapped_type.with_is_optional(optional)

        if is_optional_type(cls):
            return self._compile_type(get_args(cls)[0], optional=True)

        has_generic_args = len(get_args(cls)) > 0
        if has_generic_args:
            return self._map_generic_type(cls, optional)

        return TsType(name=cls.__name__, is_optional=optional)

    def _map_scalar_type(self, cls: Type) -> Optional[TsType]:
        if cls == str:
            return TS_STRING
        elif cls == float:
            return TS_NUMBER
        elif cls == int:
            return TS_NUMBER
        elif cls == bool:
            return TS_BOOLEAN
        elif cls == datetime:
            return TS_STRING
        elif cls == bytes:
            return TS_STRING
        elif cls == UUID:
            return TS_STRING
        return None

    def _map_generic_type(self, cls: Type, is_optional: bool) -> TsType:
        generic_origin_type = get_origin(cls)
        is_mapped_to_array = generic_origin_type in {list, set, frozenset, OrderedSet}
        if is_mapped_to_array:
            if len(get_args(cls)) != 1:
                raise UnsupportedGenericParameterCount(
                    "A type which is mapped to an array can only have one generic parameter."
                )
            return TsArray(
                wrapped_type=self._compile_type(get_args(cls)[0]),
                is_optional=is_optional,
            )

        is_mapped_to_mapped_type = issubclass(generic_origin_type, dict)
        if is_mapped_to_mapped_type:
            key_cls = get_args(cls)[0]
            has_str_key = key_cls == str
            if not has_str_key:
                raise UnsupportedKeyTypeForMappedType(key_cls)
            return TsMappedType(
                wrapped_type=self._compile_type(key_cls),
                is_optional=is_optional,
            )

        raise ValueError("not supported")

    def _compile_enum(self, enum: PyEnum) -> TsEnum:
        for py_enum_value in enum.values:
            if type(py_enum_value.value) not in {int, str}:
                raise UnsupportedEnumValue(type(py_enum_value.value))
        values: Tuple[TsEnumValue, ...] = [TsEnumValue(x.name, x.value) for x in enum.values]  # type: ignore
        return TsEnum(name=enum.name, values=tuple(values))

    def _adjust_casing(self, name: str) -> str:
        if self.typescript_compiler_settings.field_case_format == CaseFormat.CAMEL_CASE:
            return cast(str, camelcase(name))
        return name
