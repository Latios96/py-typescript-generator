from dataclasses import dataclass
from typing import Type, Tuple


@dataclass(frozen=True)
class PyEnumValue:
    name: str
    value: object


@dataclass(frozen=True)
class PyEnum:
    name: str
    type: Type
    values: Tuple[PyEnumValue, ...]
