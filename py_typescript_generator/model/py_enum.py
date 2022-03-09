from dataclasses import dataclass
from typing import Type, FrozenSet


@dataclass(frozen=True)
class PyEnum:
    name: str
    type: Type
    values: FrozenSet[object]
