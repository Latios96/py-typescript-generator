from dataclasses import dataclass
from typing import List

from ordered_set import OrderedSet

from py_typescript_generator.typescript_model_compiler.ts_enum import TsEnum
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
    TsBaseType,
)


@dataclass
class TsModel:
    types: OrderedSet[TsBaseType]
    enums: OrderedSet[TsEnum]

    @staticmethod
    def of_object_types(object_types):
        # type: (List[TsObjectType])->TsModel
        return TsModel(types=OrderedSet(object_types), enums=OrderedSet())

    @staticmethod
    def of_enums(ts_enum):
        # type: (List[TsEnum])->TsModel
        return TsModel(types=OrderedSet(), enums=OrderedSet(ts_enum))
