import inspect
import logging
from collections import defaultdict
from dataclasses import dataclass, field as dataclasses_field
from datetime import datetime
from enum import Enum
from typing import (
    List,
    Type,
    TypeVar,
    Any,
    Generic,
    Union,
    Dict,
    Optional,
    cast,
    Set,
)
from typing import _GenericAlias  # type: ignore
from uuid import UUID

from ordered_set import OrderedSet

# Note: this can be removed once support for Python 3.7 is dropped
from typing_inspect import get_args, get_origin, is_optional_type  # type: ignore

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import (
    PyClass,
    RootTaggedUnionInformation,
    TaggedUnionInformation,
)
from py_typescript_generator.model.py_enum import PyEnum, PyEnumValue
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)
from py_typescript_generator.typing_utils.typing_utils import (
    get_wrapped_type_from_optional,
    safe_unwrap,
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


@dataclass
class ModelParserSettings:
    type_mapping_overrides: Dict[Type, Type] = dataclasses_field(default_factory=dict)


class ModelParser:
    def __init__(
        self,
        classes_to_parse: List[Type],
        parsers: List[P],
        settings: ModelParserSettings,
    ):
        self._classes_to_parse = classes_to_parse
        self._parsers = parsers
        self._settings = settings

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
        if cls in {x.type for x in visited_classes}:
            return
        if not self._is_class(cls):
            raise IsNotAClassException(cls)

        type_override = self._settings.type_mapping_overrides.get(cls)
        if type_override:
            return self._parse_class(type_override, visited_classes, visited_enums)

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
                if self._is_tagged_union_class(cls):
                    new_py_cls = self._parse_as_tagged_union_class(
                        py_class, visited_classes, visited_enums
                    )
                    visited_classes.remove(py_class)
                    visited_classes.add(new_py_cls)
                    py_class = new_py_cls
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
                    values=tuple([PyEnumValue(e.name, e.value) for e in cls]),
                )
            )

    def _is_enum(self, cls: Type) -> bool:
        try:
            return issubclass(cls, Enum)
        except TypeError:
            return False

    def _is_tagged_union_class(self, cls: Type) -> bool:
        return self._read_discriminant_union_attribute_name(cls) is not None

    def _parse_as_tagged_union_class(
        self,
        py_class: PyClass,
        visited_classes: OrderedSet[PyClass],
        visited_enums: OrderedSet[PyEnum],
    ) -> PyClass:
        if self._is_tagged_union_root(py_class):
            child_classes = self._get_child_classes(py_class.type)

            discriminant_literals = set()

            parent_discriminator = self._read_discriminant_union_attribute(
                py_class.type
            )
            if parent_discriminator:
                discriminant_literals.add(parent_discriminator)

            for child in child_classes:
                discriminant_literals.add(
                    self._read_discriminant_union_attribute(child)
                )
                self._parse_class(child, visited_classes, visited_enums)

            tagged_union_information: TaggedUnionInformation = (
                RootTaggedUnionInformation(
                    discriminant_attribute=safe_unwrap(
                        self._read_discriminant_union_attribute_name(py_class.type)
                    ),
                    discriminant_literal=safe_unwrap(
                        self._read_discriminant_union_attribute(py_class.type)
                    ),
                    discriminant_literals=frozenset(discriminant_literals),
                    child_types=frozenset(child_classes),
                )
            )
            return py_class.with_tagged_union_information(tagged_union_information)
        else:
            parent_classes = self._get_parent_classes(py_class.type)
            for parent_class in parent_classes:
                self._parse_class(parent_class, visited_classes, visited_enums)
            tagged_union_information = TaggedUnionInformation(
                discriminant_attribute=safe_unwrap(
                    self._read_discriminant_union_attribute_name(py_class.type)
                ),
                discriminant_literal=safe_unwrap(
                    self._read_discriminant_union_attribute(py_class.type)
                ),
            )
            return py_class.with_tagged_union_information(tagged_union_information)

    def _is_tagged_union_root(self, py_class):
        parents = self._get_parent_classes(py_class.type)
        if not parents:
            return True
        return not any(filter(lambda x: self._is_tagged_union_class(x), parents))

    def _get_parent_classes(self, cls: Type) -> Set[Type]:
        parents = {*inspect.getmro(cls)}
        parents.remove(cls)
        parents.remove(object)
        return parents

    def _get_child_classes(self, cls: Type) -> OrderedSet[Type]:
        classes: OrderedSet[Type] = OrderedSet()
        for cl in cls.__subclasses__():
            classes.add(cl)
            classes.update(self._get_child_classes(cl))
        return classes

    def _read_discriminant_union_attribute_name(self, cls: Type) -> Optional[str]:
        try:
            return cast(str, getattr(cls, "__json_type_info_attribute__"))
        except AttributeError:
            return None

    def _read_discriminant_union_attribute(self, cls: Type) -> str:
        attr_name = getattr(cls, "__json_type_info_attribute__")
        try:
            attr = getattr(cls, attr_name)
        except AttributeError:
            return ""
        if isinstance(attr, Enum):
            return attr.name
        return cast(str, attr)
