from typing import List, Type, TypeVar

from ordered_set import OrderedSet

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)

P = TypeVar("P", bound=AbstractClassParser)


class ModelParser:
    def __init__(self, classes_to_parse: List[Type], parsers: List[P]):
        self._classes_to_parse = classes_to_parse
        self._parsers = parsers

    def parse(self) -> Model:
        visited_classes: OrderedSet[PyClass] = OrderedSet()
        for cls in self._classes_to_parse:
            self._parse_class(cls, visited_classes)

        return Model(classes=visited_classes)

    def _parse_class(self, cls: Type, visited_classes: OrderedSet[PyClass]) -> None:
        for parser in self._parsers:
            if parser.accepts_class(cls):
                py_class = parser.parse(cls)
                visited_classes.add(py_class)
                self._parse_fields(py_class, visited_classes)
                return

    def _parse_fields(
        self, py_class: PyClass, visited_classes: OrderedSet[PyClass]
    ) -> None:
        for field in py_class.fields:
            if field.type not in {x.type for x in visited_classes}:
                self._parse_class(field.type, visited_classes)
