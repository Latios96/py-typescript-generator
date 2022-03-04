from dataclasses import dataclass

from ordered_set import OrderedSet

from py_typescript_generator.model.py_class import PyClass


@dataclass
class Model:
    classes: OrderedSet[PyClass]
