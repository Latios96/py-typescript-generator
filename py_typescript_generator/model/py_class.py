from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class PyClass:
    name: str
    type: Type
