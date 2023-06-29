from dataclasses import dataclass, field
from typing import List

from ordered_set import OrderedSet

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_enum import PyEnum


@dataclass
class Model:  # todo rename to PyModel
    classes: OrderedSet[PyClass] = field(default_factory=OrderedSet)
    enums: OrderedSet[PyEnum] = field(default_factory=OrderedSet)

    @staticmethod
    def of_classes(classes):
        # type: (List[PyClass])->Model
        return Model(classes=OrderedSet(classes), enums=OrderedSet())
