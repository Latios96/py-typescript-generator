import inspect
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import (
    List,
    Type,
    TypeVar,
    Any,
    Generic,
    Union,
)
from typing import _GenericAlias  # type: ignore
from uuid import UUID


from ordered_set import OrderedSet

# Note: this can be removed once support for Python 3.7 is dropped
from typing_inspect import get_args, get_origin, is_optional_type  # type: ignore

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_enum import PyEnum, PyEnumValue
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)

import logging

from py_typescript_generator.typing_utils.typing_utils import (
    get_wrapped_type_from_optional,
)

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
        visited_enums: OrderedSet[PyEnum] = OrderedSet()
        for cls in self._classes_to_parse:
            self._parse_class(cls, visited_classes, visited_enums)

        return Model(classes=visited_classes, enums=visited_enums)

    def _parse_class(
        self,
        cls: Type,
        visited_classes: OrderedSet[PyClass],
        visited_enums: OrderedSet[PyEnum],
    ) -> None:
        if not self._is_class(cls):
            raise IsNotAClassException(cls)

        is_enum = self._is_enum(cls)
        if is_enum:
            self._parse_enum(cls, visited_enums)
            return

        if is_optional_type(cls):
            self._parse_class(
                get_wrapped_type_from_optional(cls), visited_classes, visited_enums
            )
            return

        has_generic_args = len(get_args(cls)) > 0
        if has_generic_args:
            for arg in get_args(cls):
                self._parse_class(arg, visited_classes, visited_enums)

        if self._is_terminating_class(cls):
            return

        for parser in self._parsers:
            if parser.accepts_class(cls):
                py_class = parser.parse(cls)
                visited_classes.add(py_class)
                self._parse_fields(py_class, visited_classes, visited_enums)
                return

        raise NoParserForClassFoundException(cls)

    def _parse_fields(
        self,
        py_class: PyClass,
        visited_classes: OrderedSet[PyClass],
        visited_enums: OrderedSet[PyEnum],
    ) -> None:
        for field in py_class.fields:
            if field.type not in {x.type for x in visited_classes}:
                self._parse_class(field.type, visited_classes, visited_enums)

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

    def _parse_enum(self, cls: Type, visited_enums: OrderedSet[PyEnum]) -> None:
        if cls not in {x.type for x in visited_enums}:
            visited_enums.add(
                PyEnum(
                    name=cls.__name__,
                    type=cls,
                    values=frozenset([PyEnumValue(e.name, e.value) for e in cls]),
                )
            )

    def _is_enum(self, cls: Type) -> bool:
        try:
            return issubclass(cls, Enum)
        except TypeError:
            return False
