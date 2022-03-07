import inspect
from collections import defaultdict
from datetime import datetime
from typing import (
    List,
    Type,
    TypeVar,
    Any,
    Generic,
    get_origin,
    Union,
)
from typing import _GenericAlias  # type: ignore
from uuid import UUID


from ordered_set import OrderedSet
from typing_inspect import get_args

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)

import logging

logger = logging.getLogger(__name__)

P = TypeVar("P", bound=AbstractClassParser)


class NoParserForClassFoundException(RuntimeError):
    def __init__(self, cls: Type):
        super(NoParserForClassFoundException, self).__init__(
            f"No parser found for class {cls}."
        )


class IsNotAClassException(RuntimeError):
    def __init__(self, object: Any):
        super(IsNotAClassException, self).__init__(
            f"Passed object {object} is not a class."
        )


TERMINATING_CLASSES = {
    int,
    float,
    complex,
    str,
    bytes,
    bool,
    datetime,
    UUID,
    list,
    set,
    dict,
    frozenset,
    tuple,
    defaultdict,
    Union,
}


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
        if not self._is_class(cls):
            raise IsNotAClassException(cls)

        has_generic_args = len(get_args(cls)) > 0
        if has_generic_args:
            for arg in get_args(cls):
                self._parse_class(arg, visited_classes)

        if self._is_terminating_class(cls):
            return

        for parser in self._parsers:
            if parser.accepts_class(cls):
                py_class = parser.parse(cls)
                visited_classes.add(py_class)
                self._parse_fields(py_class, visited_classes)
                return

        raise NoParserForClassFoundException(cls)

    def _parse_fields(
        self, py_class: PyClass, visited_classes: OrderedSet[PyClass]
    ) -> None:
        for field in py_class.fields:
            if field.type not in {x.type for x in visited_classes}:
                self._parse_class(field.type, visited_classes)

    def _is_class(self, cls: Type) -> bool:
        if (
            isinstance(cls, _GenericAlias)
            or isinstance(cls, Generic)  # type: ignore
            or isinstance(cls, TypeVar)
        ):
            return True
        return inspect.isclass(cls)

    def _is_terminating_class(self, cls: Type) -> bool:
        origin = get_origin(cls)
        if origin:
            return origin in TERMINATING_CLASSES
        if isinstance(cls, TypeVar):
            return True
        return cls in TERMINATING_CLASSES
