from dataclasses import dataclass
from typing import List

from py_typescript_generator.model.py_class import PyClass


@dataclass
class Model:
    classes: List[PyClass]
