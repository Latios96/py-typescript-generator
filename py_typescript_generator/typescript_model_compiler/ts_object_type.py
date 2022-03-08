from dataclasses import dataclass
from typing import FrozenSet

from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_type import TsType


@dataclass(frozen=True)
class TsObjectType(TsType):
    name: str
    fields: FrozenSet[TsField]
