from dataclasses import dataclass
from typing import FrozenSet

from py_typescript_generator.typescript_model_compiler.ts_field import TsField


@dataclass(frozen=True)
class TsObjectType:
    name: str
    fields: FrozenSet[TsField]
