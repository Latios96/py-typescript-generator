from dataclasses import dataclass
from typing import Type


@dataclass
class PyClass:
    name: str
    type: Type
