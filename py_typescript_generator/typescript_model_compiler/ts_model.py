from dataclasses import dataclass
from typing import List

from ordered_set import OrderedSet

from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)


@dataclass
class TsModel:
    types: OrderedSet[TsObjectType]

    @staticmethod
    def of_object_types(object_types):
        # type: (List[TsObjectType])->TsModel
        return TsModel(types=OrderedSet(object_types))
