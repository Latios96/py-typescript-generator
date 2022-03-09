from dataclasses import dataclass
from typing import List

from ordered_set import OrderedSet

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_enum import PyEnum


@dataclass
class Model:  # todo rename to PyModel
    classes: OrderedSet[PyClass] = OrderedSet()
    enums: OrderedSet[PyEnum] = OrderedSet()

    @staticmethod
    def of_classes(classes):
        # type: (List[PyClass])->Model
        return Model(classes=OrderedSet(classes), enums=OrderedSet())
