from datetime import datetime
from typing import Type, Optional
from uuid import UUID

from ordered_set import OrderedSet
from typing_extensions import get_args
from typing_inspect import is_optional_type, get_origin  # type: ignore

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_mapped_type import (
    TsMappedType,
)
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)
from py_typescript_generator.typescript_model_compiler.ts_type import TsType
from py_typescript_generator.typescript_model_compiler.ts_array import TsArray
from py_typescript_generator.typescript_model_compiler.well_known_types import (
    TS_NUMBER,
    TS_STRING,
    TS_BOOLEAN,
)


class UnsupportedGenericParameterCount(RuntimeError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class TypescriptModelCompiler:
    def compile(self, model: Model) -> TsModel:
        types: OrderedSet[TsObjectType] = OrderedSet()
        for py_class in model.classes:
            types.append(self._compile_class(py_class))

        return TsModel(types=types)

    def _compile_class(self, py_class: PyClass) -> TsObjectType:
        fields = []
        for py_field in py_class.fields:
            fields.append(
                TsField(name=py_field.name, type=self._compile_type(py_field.type))
            )
        return TsObjectType(name=py_class.name, fields=frozenset(fields))

    def _compile_type(self, cls: Type, optional: bool = False) -> TsType:
        mapped_type = self._map_scalar_type(cls)
        if mapped_type:
            if optional:
                return mapped_type.as_optional_type()  # todo use with_is_optional
            return mapped_type

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
            has_str_key = get_args(cls)[0] == str
            if not has_str_key:
                raise ValueError()
            return TsMappedType(
                wrapped_type=self._compile_type(get_args(cls)[0]),
                is_optional=is_optional,
            )

        raise ValueError("not supported")
