from typing import List, Type

from py_typescript_generator.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)
from py_typescript_generator.model.model import Model


class ModelParser:
    def __init__(self, types_to_parse: List[Type], parsers: AbstractClassParser):
        self._types_to_parse = types_to_parse
        self._parsers = parsers

    def parse(self) -> Model:
        pass
