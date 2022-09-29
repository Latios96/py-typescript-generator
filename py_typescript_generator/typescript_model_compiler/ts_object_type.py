from dataclasses import dataclass
from typing import Tuple, Optional

from py_typescript_generator.typescript_model_compiler.ts_field import TsField


@dataclass(frozen=True)
class TsDiscriminator:
    name: str
    value: str


@dataclass(frozen=True)
class TsBaseType:
    name: str


@dataclass(frozen=True)
class TsObjectType(TsBaseType):
    fields: Tuple[TsField, ...]
    discriminator: Optional[TsDiscriminator] = None


@dataclass(frozen=True)
class TsUnionType(TsBaseType):
    union_members: Tuple[str, ...]
