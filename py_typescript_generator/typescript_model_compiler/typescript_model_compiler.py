from datetime import datetime
from typing import Type, Optional
from uuid import UUID

from ordered_set import OrderedSet

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)
from py_typescript_generator.typescript_model_compiler.ts_type import TsType
from py_typescript_generator.typescript_model_compiler.well_known_types import (
    TS_NUMBER,
    TS_STRING,
    TS_BOOLEAN,
)


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

    def _compile_type(self, cls: Type) -> TsType:
        mapped_type = self._map_type(cls)
        if mapped_type:
            return mapped_type

        return TsType(name=cls.__name__)

    def _map_type(self, cls: Type) -> Optional[TsType]:
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
