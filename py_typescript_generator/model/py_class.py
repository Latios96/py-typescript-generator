from dataclasses import dataclass
from typing import Type, Tuple, Optional, FrozenSet

from py_typescript_generator.model.py_field import PyField


@dataclass(frozen=True)
class TaggedUnionInformation:
    discriminant_attribute: str
    discriminant_literal: str


@dataclass(frozen=True)
class RootTaggedUnionInformation(TaggedUnionInformation):
    discriminant_literals: FrozenSet[str]
    child_types: FrozenSet[Type]


@dataclass(frozen=True)
class PyClass:
    name: str
    type: Type
    fields: Tuple[PyField, ...]
    tagged_union_information: Optional[TaggedUnionInformation] = None

    def with_tagged_union_information(self, tagged_union_information):
        # type: (TaggedUnionInformation)->PyClass
        return PyClass(
            name=self.name,
            type=self.type,
            fields=self.fields,
            tagged_union_information=tagged_union_information,
        )
