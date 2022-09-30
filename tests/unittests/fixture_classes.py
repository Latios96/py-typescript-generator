from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import (
    List,
    Dict,
    TypeVar,
    Generic,
    Type,
    Set,
    Tuple,
    Union,
    FrozenSet,
    DefaultDict,
    Optional,
    OrderedDict,
)
from uuid import UUID

import pytest
from ordered_set import OrderedSet

from py_typescript_generator.model.py_class import (
    PyClass,
    RootTaggedUnionInformation,
    TaggedUnionInformation,
)
from py_typescript_generator.model.py_enum import PyEnum, PyEnumValue
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.typescript_model_compiler.ts_array import TsArray
from py_typescript_generator.typescript_model_compiler.ts_enum import (
    TsEnum,
    TsEnumValue,
)
from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_mapped_type import (
    TsMappedType,
)
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
    TsDiscriminator,
    TsUnionType,
)
from py_typescript_generator.typescript_model_compiler.ts_type import TsType
from py_typescript_generator.typescript_model_compiler.well_known_types import (
    TS_NUMBER,
    TS_ANY,
    TS_STRING,
    TS_BOOLEAN,
)


class EmptyClass:
    pass


class ClassWithEmptyClass:
    empty_class: EmptyClass


class ClassWithClassWithEmptyClass:
    class_with_empty_class: ClassWithEmptyClass


class FirstClassInCycle:
    second = None  # type:  SecondClassInCycle


class SecondClassInCycle:
    first: FirstClassInCycle


class ClassWithInt:
    value: int


class ClassWithFloat:
    value: float


class ClassWithStr:
    value: str


class ClassWithBytes:
    value: bytes


class ClassWithBool:
    value: bool


class ClassWithDatetime:
    value: datetime


class ClassWithUUID:
    value: UUID


class ClassWithStrSet:
    value: Set[str]


class ClassWithStrTuple:
    value: Tuple[str]


class ClassWithStrIntUnion:
    value: Union[str, int]


class ClassWithStrFrozenSet:
    value: FrozenSet[str]


class ClassWithStrOrderedSet:
    value: OrderedSet[str]


class ClassWithStrStrDefaultDict:
    value: DefaultDict[str, str]


class ClassWithStrStrOrderedDict:
    value: OrderedDict[str, str]


class ClassWithStrList:
    str_list: List[str]


class ClassWithStrStrDict:
    str_dict: Dict[str, str]


class ClassWithEmptyClassList:
    empty_class_list: List[EmptyClass]


T = TypeVar("T")


class ClassWithGenericMember(Generic[T]):
    my_member: T


class ClassWithDeepNestedGenerics:
    my_dict: Dict[str, List[Dict[str, EmptyClass]]]


class ClassWithOptionalInt:
    value: Optional[int]


class ClassWithOptionalEmptyClass:
    value: Optional[EmptyClass]


class ClassWithListOfOptionalInt:
    value: List[Optional[int]]


class ClassWithListOfOptionalEmptyClass:
    value: List[Optional[EmptyClass]]


class SimpleIntEnum(Enum):
    FIRST = 0
    SECOND = 1


class SimpleStrEnum(Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"


class ClassWithTaggedUnionDiscriminantButNoChildren:
    __json_type_info_attribute__ = "type"
    type = "TEST"


class ClassWithTaggedUnionDiscriminantNoDiscriminatorForRoot:
    __json_type_info_attribute__ = "type"


class ClassWithTaggedUnionDiscriminantSingleChild:
    __json_type_info_attribute__ = "my_type"
    my_type = "BASE"


class ClassWithTaggedUnionDiscriminantSingleChildChild(
    ClassWithTaggedUnionDiscriminantSingleChild
):
    my_type = "CHILD"


class ClassWithTaggedUnionDiscriminantMultipleChildren:
    __json_type_info_attribute__ = "type"
    type = "BASE"


class ClassWithTaggedUnionDiscriminantMultipleChildrenChild1(
    ClassWithTaggedUnionDiscriminantMultipleChildren
):
    type = "CHILD_1"


class ClassWithTaggedUnionDiscriminantMultipleChildrenChild2(
    ClassWithTaggedUnionDiscriminantMultipleChildren
):
    type = "CHILD_2"


class ClassWithTaggedUnionDiscriminantEnumDiscriminatorDiscriminator(Enum):
    BASE = "BASE"
    CHILD = "CHILD"


class ClassWithTaggedUnionDiscriminantEnumDiscriminator:
    __json_type_info_attribute__ = "type"
    type = ClassWithTaggedUnionDiscriminantEnumDiscriminatorDiscriminator.BASE


class ClassWithTaggedUnionDiscriminantEnumDiscriminatorChild(
    ClassWithTaggedUnionDiscriminantEnumDiscriminator
):
    type = ClassWithTaggedUnionDiscriminantEnumDiscriminatorDiscriminator.CHILD


PY_CLASS_FOR_EMPTY_CLASS = PyClass(name="EmptyClass", type=EmptyClass, fields=())
TS_OBJECT_TYPE_FOR_EMPTY_CLASS = TsObjectType(
    name="EmptyClass",
    fields=tuple(),
)
PY_CLASS_FOR_CLASS_WITH_EMPTY_CLASS = PyClass(
    name="ClassWithEmptyClass",
    type=ClassWithEmptyClass,
    fields=tuple({PyField(name="empty_class", type=EmptyClass)}),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_EMPTY_CLASS = TsObjectType(
    name="ClassWithEmptyClass",
    fields=(TsField(name="empty_class", type=TsType("EmptyClass")),),
)
PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_EMPTY_CLASS = PyClass(
    name="ClassWithClassWithEmptyClass",
    type=ClassWithClassWithEmptyClass,
    fields=(PyField(name="class_with_empty_class", type=ClassWithEmptyClass),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_CLASS_WITH_EMPTY_CLASS = TsObjectType(
    name="ClassWithClassWithEmptyClass",
    fields=(
        TsField(
            name="class_with_empty_class",
            type=TsType("ClassWithEmptyClass"),
        ),
    ),
)
PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE = PyClass(
    name="FirstClassInCycle",
    type=FirstClassInCycle,
    fields=(PyField(name="second", type=SecondClassInCycle),),
)
TS_OBJECT_TYPE_FOR_FIRST_CLASS_IN_CYCLE = TsObjectType(
    name="FirstClassInCycle",
    fields=(TsField(name="second", type=TsType("SecondClassInCycle")),),
)
PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE = PyClass(
    name="SecondClassInCycle",
    type=SecondClassInCycle,
    fields=(PyField(name="first", type=FirstClassInCycle),),
)
TS_OBJECT_TYPE_FOR_SECOND_CLASS_IN_CYCLE = TsObjectType(
    name="SecondClassInCycle",
    fields=(TsField(name="first", type=TsType("FirstClassInCycle")),),
)
PY_CLASS_FOR_CLASS_WITH_INT = PyClass(
    name="ClassWithInt",
    type=ClassWithInt,
    fields=(PyField(name="value", type=int),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_INT = TsObjectType(
    name="ClassWithInt",
    fields=(TsField(name="value", type=TS_NUMBER),),
)
PY_CLASS_FOR_CLASS_WITH_STR_LIST = PyClass(
    name="ClassWithStrList",
    type=ClassWithStrList,
    fields=(PyField(name="str_list", type=List[str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_LIST = TsObjectType(
    name="ClassWithStrList",
    fields=(TsField(name="str_list", type=TsArray(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT = PyClass(
    name="ClassWithStrStrDict",
    type=ClassWithStrStrDict,
    fields=(PyField(name="str_dict", type=Dict[str, str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_STR_DICT = TsObjectType(
    name="ClassWithStrStrDict",
    fields=(TsField(name="str_dict", type=TsMappedType(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_EMPTY_CLASS_LIST = PyClass(
    name="ClassWithEmptyClassList",
    type=ClassWithEmptyClassList,
    fields=(PyField(name="empty_class_list", type=List[EmptyClass]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_EMPTY_CLASS_LIST = TsObjectType(
    name="ClassWithEmptyClassList",
    fields=(TsField(name="empty_class_list", type=TsArray(TsType("EmptyClass"))),),
)
PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER = PyClass(
    name="ClassWithGenericMember",
    type=ClassWithGenericMember,
    fields=(PyField(name="my_member", type=T),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_GENERIC_MEMBER = TsObjectType(
    name="ClassWithGenericMember",
    fields=(TsField(name="my_member", type=TS_ANY),),  # type: ignore
)
PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS = PyClass(
    name="ClassWithDeepNestedGenerics",
    type=ClassWithDeepNestedGenerics,
    fields=(PyField(name="my_dict", type=Dict[str, List[Dict[str, EmptyClass]]]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_DEEP_NESTED_GENERICS = TsObjectType(
    name="ClassWithDeepNestedGenerics",
    fields=(TsField(name="my_dict", type=TS_ANY),),
)
PY_CLASS_FOR_CLASS_WITH_FLOAT = PyClass(
    name="ClassWithFloat",
    type=ClassWithFloat,
    fields=(PyField(name="value", type=float),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_FLOAT = TsObjectType(
    name="ClassWithFloat",
    fields=(TsField(name="value", type=TS_NUMBER),),
)
PY_CLASS_FOR_CLASS_WITH_STR = PyClass(
    name="ClassWithStr",
    type=ClassWithStr,
    fields=(PyField(name="value", type=str),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR = TsObjectType(
    name="ClassWithStr",
    fields=(TsField(name="value", type=TS_STRING),),
)
PY_CLASS_FOR_CLASS_WITH_BYTES = PyClass(
    name="ClassWithBytes",
    type=ClassWithBytes,
    fields=(PyField(name="value", type=bytes),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_BYTES = TsObjectType(
    name="ClassWithBytes",
    fields=(TsField(name="value", type=TS_STRING),),
)
PY_CLASS_FOR_CLASS_WITH_BOOL = PyClass(
    name="ClassWithBool",
    type=ClassWithBool,
    fields=(PyField(name="value", type=bool),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_BOOL = TsObjectType(
    name="ClassWithBool",
    fields=(TsField(name="value", type=TS_BOOLEAN),),
)
PY_CLASS_FOR_CLASS_WITH_DATETIME = PyClass(
    name="ClassWithDatetime",
    type=ClassWithDatetime,
    fields=(PyField(name="value", type=datetime),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_DATETIME = TsObjectType(
    name="ClassWithDatetime",
    fields=(TsField(name="value", type=TS_STRING),),
)
PY_CLASS_FOR_CLASS_WITH_UUID = PyClass(
    name="ClassWithUUID",
    type=ClassWithUUID,
    fields=(PyField(name="value", type=UUID),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_UUID = TsObjectType(
    name="ClassWithUUID",
    fields=(TsField(name="value", type=TS_STRING),),
)
PY_CLASS_FOR_CLASS_WITH_STR_SET = PyClass(
    name="ClassWithStrSet",
    type=ClassWithStrSet,
    fields=(PyField(name="value", type=Set[str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_SET = TsObjectType(
    name="ClassWithStrSet",
    fields=(TsField(name="value", type=TsArray(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_STR_TUPLE = PyClass(
    name="ClassWithStrTuple",
    type=ClassWithStrTuple,
    fields=(PyField(name="value", type=Tuple[str]),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_TUPLE = TsObjectType(
    name="ClassWithStrTuple",
    fields=(TsField(name="value", type=TS_ANY),),
)
PY_CLASS_FOR_CLASS_WITH_STR_INT_UNION = PyClass(
    name="ClassWithStrIntUnion",
    type=ClassWithStrIntUnion,
    fields=(PyField(name="value", type=Union[str, int]),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_INT_UNION = TsObjectType(
    name="ClassWithStrIntUnion",
    fields=(TsField(name="value", type=TS_ANY),),
)
PY_CLASS_FOR_CLASS_WITH_STR_FROZEN_SET = PyClass(
    name="ClassWithStrFrozenSet",
    type=ClassWithStrFrozenSet,
    fields=(PyField(name="value", type=FrozenSet[str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_FROZEN_SET = TsObjectType(
    name="ClassWithStrFrozenSet",
    fields=(TsField(name="value", type=TsArray(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_STR_ORDERED_SET = PyClass(
    name="ClassWithStrOrderedSet",
    type=ClassWithStrOrderedSet,
    fields=(PyField(name="value", type=FrozenSet[str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_ORDERED_SET = TsObjectType(
    name="ClassWithStrOrderedSet",
    fields=(TsField(name="value", type=TsArray(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT = PyClass(
    name="ClassWithStrStrDefaultDict",
    type=ClassWithStrStrDefaultDict,
    fields=(PyField(name="value", type=DefaultDict[str, str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT = TsObjectType(
    name="ClassWithStrStrDefaultDict",
    fields=(TsField(name="value", type=TsMappedType(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_STR_STR_ORDERED_DICT = PyClass(
    name="ClassWithStrStrOrderedDict",
    type=ClassWithStrStrOrderedDict,
    fields=(PyField(name="value", type=DefaultDict[str, str]),),
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_STR_ORDERED_DICT = TsObjectType(
    name="ClassWithStrStrOrderedDict",
    fields=(TsField(name="value", type=TsMappedType(TS_STRING)),),
)
PY_CLASS_FOR_CLASS_WITH_OPTIONAL_INT = PyClass(
    name="ClassWithOptionalInt",
    type=ClassWithOptionalInt,
    fields=(PyField(name="value", type=Optional[int]),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_OPTIONAL_INT = TsObjectType(
    name="ClassWithOptionalInt",
    fields=(TsField(name="value", type=TS_NUMBER.as_optional_type()),),
)

PY_CLASS_FOR_CLASS_WITH_OPTIONAL_EMPTY_CLASS = PyClass(
    name="ClassWithOptionalEmptyClass",
    type=ClassWithOptionalEmptyClass,
    fields=(PyField(name="value", type=Optional[EmptyClass]),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_OPTIONAL_EMPTY_CLASS = TsObjectType(
    name="ClassWithOptionalEmptyClass",
    fields=(TsField(name="value", type=TsType("EmptyClass", is_optional=True)),),
)
PY_CLASS_FOR_CLASS_WITH_LIST_OF_OPTIONAL_INT = PyClass(
    name="ClassWithListOfOptionalInt",
    type=ClassWithListOfOptionalInt,
    fields=(PyField(name="value", type=List[Optional[int]]),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_LIST_OF_OPTIONAL_INT = TsObjectType(
    name="ClassWithListOfOptionalInt",
    fields=(TsField(name="value", type=TsArray(TS_NUMBER.as_optional_type())),),
)

PY_CLASS_FOR_CLASS_WITH_LIST_OF_OPTIONAL_EMPTY_CLASS = PyClass(
    name="ClassWithListOfOptionalEmptyClass",
    type=ClassWithListOfOptionalEmptyClass,
    fields=(PyField(name="value", type=List[Optional[EmptyClass]]),),  # type: ignore
)
TS_OBJECT_TYPE_FOR_CLASS_WITH_LIST_OF_OPTIONAL_EMPTY_CLASS = TsObjectType(
    name="ClassWithListOfOptionalEmptyClass",
    fields=(
        TsField(name="value", type=TsArray(TsType("EmptyClass", is_optional=True))),
    ),
)
PY_ENUM_FOR_SIMPLE_INT_ENUM = PyEnum(
    name="SimpleIntEnum",
    type=SimpleIntEnum,
    values=(
        PyEnumValue(name="FIRST", value=0),
        PyEnumValue(name="SECOND", value=1),
    ),
)
TS_ENUM_FOR_SIMPLE_INT_ENUM = TsEnum(
    name="SimpleIntEnum",
    values=(
        TsEnumValue(name="FIRST", value=0),
        TsEnumValue(name="SECOND", value=1),
    ),
)
PY_ENUM_FOR_SIMPLE_STR_ENUM = PyEnum(
    name="SimpleStrEnum",
    type=SimpleStrEnum,
    values=(
        PyEnumValue(name="FIRST", value="FIRST"),
        PyEnumValue(name="SECOND", value="SECOND"),
    ),
)
TS_ENUM_FOR_SIMPLE_STR_ENUM = TsEnum(
    name="SimpleStrEnum",
    values=(
        TsEnumValue(name="FIRST", value="FIRST"),
        TsEnumValue(name="SECOND", value="SECOND"),
    ),
)
PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_BUT_NO_CHILDREN = PyClass(
    name="ClassWithTaggedUnionDiscriminantButNoChildren",
    type=ClassWithTaggedUnionDiscriminantButNoChildren,
    fields=(),
    tagged_union_information=RootTaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="TEST",
        discriminant_literals=frozenset({"TEST"}),
        child_types=frozenset(),
    ),
)

PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_NO_DISCRIMINANT_FOR_ROOT = PyClass(
    name="ClassWithTaggedUnionDiscriminantNoDiscriminatorForRoot",
    type=ClassWithTaggedUnionDiscriminantNoDiscriminatorForRoot,
    fields=(),
    tagged_union_information=RootTaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="",
        discriminant_literals=frozenset(),
        child_types=frozenset(),
    ),
)
PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_SINGLE_CHILD = PyClass(
    name="ClassWithTaggedUnionDiscriminantSingleChild",
    type=ClassWithTaggedUnionDiscriminantSingleChild,
    fields=(),
    tagged_union_information=RootTaggedUnionInformation(
        discriminant_attribute="my_type",
        discriminant_literal="BASE",
        discriminant_literals=frozenset({"BASE", "CHILD"}),
        child_types=frozenset({ClassWithTaggedUnionDiscriminantSingleChildChild}),
    ),
)
PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_SINGLE_CHILD_CHILD = PyClass(
    name="ClassWithTaggedUnionDiscriminantSingleChildChild",
    type=ClassWithTaggedUnionDiscriminantSingleChildChild,
    fields=(),
    tagged_union_information=TaggedUnionInformation(
        discriminant_attribute="my_type",
        discriminant_literal="CHILD",
    ),
)

PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_MULTIPLE_CHILDREN = PyClass(
    name="ClassWithTaggedUnionDiscriminantMultipleChildren",
    type=ClassWithTaggedUnionDiscriminantMultipleChildren,
    fields=(),
    tagged_union_information=RootTaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="BASE",
        discriminant_literals=frozenset({"BASE", "CHILD_1", "CHILD_2"}),
        child_types=frozenset(
            {
                ClassWithTaggedUnionDiscriminantMultipleChildrenChild1,
                ClassWithTaggedUnionDiscriminantMultipleChildrenChild2,
            }
        ),
    ),
)

PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_MULTIPLE_CHILDREN_CHILD_1 = PyClass(
    name="ClassWithTaggedUnionDiscriminantMultipleChildrenChild1",
    type=ClassWithTaggedUnionDiscriminantMultipleChildrenChild1,
    fields=(),
    tagged_union_information=TaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="CHILD_1",
    ),
)

PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_MULTIPLE_CHILDREN_CHILD_2 = PyClass(
    name="ClassWithTaggedUnionDiscriminantMultipleChildrenChild2",
    type=ClassWithTaggedUnionDiscriminantMultipleChildrenChild2,
    fields=(),
    tagged_union_information=TaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="CHILD_2",
    ),
)


PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_ENUM_DISCRIMINATOR = PyClass(
    name="ClassWithTaggedUnionDiscriminantEnumDiscriminator",
    type=ClassWithTaggedUnionDiscriminantEnumDiscriminator,
    fields=(),
    tagged_union_information=RootTaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="BASE",
        discriminant_literals=frozenset({"BASE", "CHILD"}),
        child_types=frozenset(
            {
                ClassWithTaggedUnionDiscriminantEnumDiscriminatorChild,
            }
        ),
    ),
)
PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_ENUM_DISCRIMINATOR_CHILD = PyClass(
    name="ClassWithTaggedUnionDiscriminantEnumDiscriminatorChild",
    type=ClassWithTaggedUnionDiscriminantEnumDiscriminatorChild,
    fields=(),
    tagged_union_information=TaggedUnionInformation(
        discriminant_attribute="type",
        discriminant_literal="CHILD",
    ),
)


@dataclass
class ClassFixture:
    cls: Type
    py_class: PyClass
    ts_object_type: TsObjectType


@dataclass
class EnumFixture:
    cls: Type
    py_enum: PyEnum
    ts_enum: TsEnum


@pytest.fixture
def empty_class():
    return ClassFixture(
        cls=EmptyClass,
        py_class=PY_CLASS_FOR_EMPTY_CLASS,
        ts_object_type=TS_OBJECT_TYPE_FOR_EMPTY_CLASS,
    )


@pytest.fixture
def class_with_empty_class():
    return ClassFixture(
        cls=ClassWithEmptyClass,
        py_class=PY_CLASS_FOR_CLASS_WITH_EMPTY_CLASS,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_EMPTY_CLASS,
    )


@pytest.fixture
def class_with_class_with_empty_class():
    return ClassFixture(
        cls=ClassWithClassWithEmptyClass,
        py_class=PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_EMPTY_CLASS,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_CLASS_WITH_EMPTY_CLASS,
    )


@pytest.fixture
def first_class_in_cycle():
    return ClassFixture(
        cls=FirstClassInCycle,
        py_class=PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE,
        ts_object_type=TS_OBJECT_TYPE_FOR_FIRST_CLASS_IN_CYCLE,
    )


@pytest.fixture
def second_class_in_cycle():
    return ClassFixture(
        cls=SecondClassInCycle,
        py_class=PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE,
        ts_object_type=TS_OBJECT_TYPE_FOR_SECOND_CLASS_IN_CYCLE,
    )


@pytest.fixture
def class_with_int():
    return ClassFixture(
        cls=ClassWithInt,
        py_class=PY_CLASS_FOR_CLASS_WITH_INT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_INT,
    )


@pytest.fixture
def class_with_float():
    return ClassFixture(
        cls=ClassWithFloat,
        py_class=PY_CLASS_FOR_CLASS_WITH_FLOAT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_FLOAT,
    )


@pytest.fixture
def class_with_str():
    return ClassFixture(
        cls=ClassWithStr,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR,
    )


@pytest.fixture
def class_with_bytes():
    return ClassFixture(
        cls=ClassWithBytes,
        py_class=PY_CLASS_FOR_CLASS_WITH_BYTES,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_BYTES,
    )


@pytest.fixture
def class_with_bool():
    return ClassFixture(
        cls=ClassWithBool,
        py_class=PY_CLASS_FOR_CLASS_WITH_BOOL,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_BOOL,
    )


@pytest.fixture
def class_with_datetime():
    return ClassFixture(
        cls=ClassWithDatetime,
        py_class=PY_CLASS_FOR_CLASS_WITH_DATETIME,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_DATETIME,
    )


@pytest.fixture
def class_with_uuid():
    return ClassFixture(
        cls=ClassWithUUID,
        py_class=PY_CLASS_FOR_CLASS_WITH_UUID,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_UUID,
    )


@pytest.fixture
def class_with_str_set():
    return ClassFixture(
        cls=ClassWithStrSet,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_SET,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_SET,
    )


@pytest.fixture
def class_with_str_tuple():
    return ClassFixture(
        cls=ClassWithStrTuple,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_TUPLE,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_TUPLE,
    )


@pytest.fixture
def class_with_str_int_union():
    return ClassFixture(
        cls=ClassWithStrIntUnion,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_INT_UNION,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_INT_UNION,
    )


@pytest.fixture
def class_with_str_frozen_set():
    return ClassFixture(
        cls=ClassWithStrFrozenSet,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_FROZEN_SET,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_FROZEN_SET,
    )


@pytest.fixture
def class_with_str_ordered_set():
    return ClassFixture(
        cls=ClassWithStrOrderedSet,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_ORDERED_SET,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_ORDERED_SET,
    )


@pytest.fixture
def class_with_str_str_default_dict():
    return ClassFixture(
        cls=ClassWithStrStrDefaultDict,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT,
    )


@pytest.fixture
def class_with_str_str_ordered_dict():
    return ClassFixture(
        cls=ClassWithStrStrOrderedDict,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_STR_ORDERED_DICT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_STR_ORDERED_DICT,
    )


@pytest.fixture
def class_with_str_list():
    return ClassFixture(
        cls=ClassWithStrList,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_LIST,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_LIST,
    )


@pytest.fixture
def class_with_str_str_dict():
    return ClassFixture(
        cls=ClassWithStrStrDict,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_STR_STR_DICT,
    )


@pytest.fixture
def class_with_empty_class_list():
    return ClassFixture(
        cls=ClassWithEmptyClassList,
        py_class=PY_CLASS_FOR_CLASS_WITH_EMPTY_CLASS_LIST,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_EMPTY_CLASS_LIST,
    )


@pytest.fixture
def class_with_generic_member():
    return ClassFixture(
        cls=ClassWithGenericMember,
        py_class=PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_GENERIC_MEMBER,
    )


@pytest.fixture
def class_with_deep_nested_generics():
    return ClassFixture(
        cls=ClassWithDeepNestedGenerics,
        py_class=PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
    )


@pytest.fixture
def class_with_optional_int():
    return ClassFixture(
        cls=ClassWithOptionalInt,
        py_class=PY_CLASS_FOR_CLASS_WITH_OPTIONAL_INT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_OPTIONAL_INT,
    )


@pytest.fixture
def class_with_optional_empty_class():
    return ClassFixture(
        cls=ClassWithOptionalEmptyClass,
        py_class=PY_CLASS_FOR_CLASS_WITH_OPTIONAL_EMPTY_CLASS,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_OPTIONAL_EMPTY_CLASS,
    )


@pytest.fixture
def class_with_list_of_optional_int():
    return ClassFixture(
        cls=ClassWithListOfOptionalInt,
        py_class=PY_CLASS_FOR_CLASS_WITH_LIST_OF_OPTIONAL_INT,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_LIST_OF_OPTIONAL_INT,
    )


@pytest.fixture
def class_with_list_of_optional_empty_class():
    return ClassFixture(
        cls=ClassWithListOfOptionalEmptyClass,
        py_class=PY_CLASS_FOR_CLASS_WITH_LIST_OF_OPTIONAL_EMPTY_CLASS,
        ts_object_type=TS_OBJECT_TYPE_FOR_CLASS_WITH_LIST_OF_OPTIONAL_EMPTY_CLASS,
    )


@pytest.fixture
def simple_int_enum():
    return EnumFixture(
        cls=SimpleIntEnum,
        py_enum=PY_ENUM_FOR_SIMPLE_INT_ENUM,
        ts_enum=TS_ENUM_FOR_SIMPLE_INT_ENUM,
    )


@pytest.fixture
def simple_str_enum():
    return EnumFixture(
        cls=SimpleStrEnum,
        py_enum=PY_ENUM_FOR_SIMPLE_STR_ENUM,
        ts_enum=TS_ENUM_FOR_SIMPLE_STR_ENUM,
    )


@pytest.fixture
def class_with_tagged_union_discriminant_but_no_children():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantButNoChildren,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_BUT_NO_CHILDREN,
        ts_object_type=TsUnionType(
            name="ClassWithTaggedUnionDiscriminantSingleChild",
            union_members=(),
        ),
    )


@pytest.fixture
def class_with_tagged_union_discriminant_no_discriminant_for_root():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantNoDiscriminatorForRoot,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_NO_DISCRIMINANT_FOR_ROOT,
        ts_object_type=TsUnionType(
            name="ClassWithTaggedUnionDiscriminantSingleChild",
            union_members=(),
        ),
    )


@pytest.fixture
def class_with_tagged_union_discriminant_single_child():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantSingleChild,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_SINGLE_CHILD,
        ts_object_type=TsUnionType(
            name="ClassWithTaggedUnionDiscriminantSingleChild",
            union_members=("ClassWithTaggedUnionDiscriminantSingleChildChild",),
        ),
    )


@pytest.fixture
def class_with_tagged_union_discriminant_single_child_child():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantSingleChildChild,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_SINGLE_CHILD_CHILD,
        ts_object_type=TsObjectType(
            name="ClassWithTaggedUnionDiscriminantSingleChildChild",
            fields=(),
            discriminator=TsDiscriminator(name="myType", value="CHILD"),
        ),
    )


@pytest.fixture
def class_with_tagged_union_discriminant_multiple_children():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantMultipleChildren,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_MULTIPLE_CHILDREN,
        ts_object_type=TsUnionType(
            name="ClassWithTaggedUnionDiscriminantMultipleChildren",
            union_members=(
                "ClassWithTaggedUnionDiscriminantMultipleChildrenChild1",
                "ClassWithTaggedUnionDiscriminantMultipleChildrenChild2",
            ),
        ),
    )


@pytest.fixture
def class_with_tagged_union_discriminant_multiple_children_child_1():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantMultipleChildren,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_MULTIPLE_CHILDREN_CHILD_1,
        ts_object_type=None,
    )


@pytest.fixture
def class_with_tagged_union_discriminant_multiple_children_child_2():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantMultipleChildren,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_MULTIPLE_CHILDREN_CHILD_2,
        ts_object_type=None,
    )


@pytest.fixture
def class_with_tagged_union_discriminant_enum_discriminant():
    return ClassFixture(
        cls=ClassWithTaggedUnionDiscriminantEnumDiscriminator,
        py_class=PY_CLASS_FOR_CLASS_WITH_TAGGED_UNION_DISCRIMINANT_ENUM_DISCRIMINATOR,
        ts_object_type=None,
    )
