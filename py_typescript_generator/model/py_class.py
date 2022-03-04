from dataclasses import dataclass
from typing import Type, FrozenSet

from py_typescript_generator.model.py_field import PyField


@dataclass(frozen=True)
class PyClass:
    name: str
    type: Type
    fields: FrozenSet[PyField]
