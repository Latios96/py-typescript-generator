from dataclasses import dataclass

from ordered_set import OrderedSet

from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)


@dataclass
class TsModel:
    types: OrderedSet[TsObjectType]
