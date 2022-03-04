from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class PyField:
    name: str
    type: Type
