from typing import List, Type, Set, TypeVar

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
        visited_classes: Set[PyClass] = set()
        for cls in self._classes_to_parse:
            for parser in self._parsers:
                if parser.accepts_class(cls):
                    py_class = parser.parse(cls)
                    visited_classes.add(py_class)
                    continue

        return Model(classes=list(visited_classes))
