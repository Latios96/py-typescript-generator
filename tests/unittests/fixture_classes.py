from dataclasses import dataclass
from datetime import datetime
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
)
from uuid import UUID

import pytest

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField


class SimpleDemoClass:
    pass


class ClassWithSimpleDemoClass:
    simple_demo_class: SimpleDemoClass


class ClassWithClassWithSimpleDemoClass:
    class_with_simple_demo_class: ClassWithSimpleDemoClass


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


class ClassWithStrStrDefaultDict:
    value: DefaultDict[str, str]


class ClassWithStrList:
    str_list: List[str]


class ClassWithStrStrDict:
    str_dict: Dict[str, str]


class ClassWithSimpleDemoClassList:
    simple_demo_class_list: List[SimpleDemoClass]


T = TypeVar("T")


class ClassWithGenericMember(Generic[T]):
    my_member: T


class ClassWithDeepNestedGenerics:
    my_dict: Dict[str, List[Dict[str, SimpleDemoClass]]]


PY_CLASS_FOR_SIMPLE_DEMO_CLASS = PyClass(
    name="SimpleDemoClass", type=SimpleDemoClass, fields=frozenset()
)
PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS = PyClass(
    name="ClassWithSimpleDemoClass",
    type=ClassWithSimpleDemoClass,
    fields=frozenset({PyField(name="simple_demo_class", type=SimpleDemoClass)}),
)
PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS = PyClass(
    name="ClassWithClassWithSimpleDemoClass",
    type=ClassWithClassWithSimpleDemoClass,
    fields=frozenset(
        {PyField(name="class_with_simple_demo_class", type=ClassWithSimpleDemoClass)}
    ),
)
PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE = PyClass(
    name="FirstClassInCycle",
    type=FirstClassInCycle,
    fields=frozenset({PyField(name="second", type=SecondClassInCycle)}),
)
PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE = PyClass(
    name="SecondClassInCycle",
    type=SecondClassInCycle,
    fields=frozenset({PyField(name="first", type=FirstClassInCycle)}),
)
PY_CLASS_FOR_CLASS_WITH_INT = PyClass(
    name="ClassWithInt",
    type=ClassWithInt,
    fields=frozenset({PyField(name="value", type=int)}),
)
PY_CLASS_FOR_CLASS_WITH_STR_LIST = PyClass(
    name="ClassWithStrList",
    type=ClassWithStrList,
    fields=frozenset({PyField(name="str_list", type=List[str])}),
)
PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT = PyClass(
    name="ClassWithStrStrDict",
    type=ClassWithStrStrDict,
    fields=frozenset({PyField(name="str_dict", type=Dict[str, str])}),
)
PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST = PyClass(
    name="ClassWithSimpleDemoClassList",
    type=ClassWithSimpleDemoClassList,
    fields=frozenset(
        {PyField(name="simple_demo_class_list", type=List[SimpleDemoClass])}
    ),
)
PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER = PyClass(
    name="ClassWithGenericMember",
    type=ClassWithGenericMember,
    fields=frozenset({PyField(name="my_member", type=T)}),  # type: ignore
)
PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS = PyClass(
    name="ClassWithDeepNestedGenerics",
    type=ClassWithDeepNestedGenerics,
    fields=frozenset(
        {PyField(name="my_dict", type=Dict[str, List[Dict[str, SimpleDemoClass]]])}
    ),
)


PY_CLASS_FOR_CLASS_WITH_FLOAT = PyClass(
    name="ClassWithFloat",
    type=ClassWithFloat,
    fields=frozenset({PyField(name="value", type=float)}),
)
PY_CLASS_FOR_CLASS_WITH_STR = PyClass(
    name="ClassWithStr",
    type=ClassWithStr,
    fields=frozenset({PyField(name="value", type=str)}),
)
PY_CLASS_FOR_CLASS_WITH_BYTES = PyClass(
    name="ClassWithBytes",
    type=ClassWithBytes,
    fields=frozenset({PyField(name="value", type=bytes)}),
)
PY_CLASS_FOR_CLASS_WITH_BOOL = PyClass(
    name="ClassWithBool",
    type=ClassWithBool,
    fields=frozenset({PyField(name="value", type=bool)}),
)
PY_CLASS_FOR_CLASS_WITH_DATETIME = PyClass(
    name="ClassWithDatetime",
    type=ClassWithDatetime,
    fields=frozenset({PyField(name="value", type=datetime)}),
)
PY_CLASS_FOR_CLASS_WITH_UUID = PyClass(
    name="ClassWithUUID",
    type=ClassWithUUID,
    fields=frozenset({PyField(name="value", type=UUID)}),
)
PY_CLASS_FOR_CLASS_WITH_STR_SET = PyClass(
    name="ClassWithStrSet",
    type=ClassWithStrSet,
    fields=frozenset({PyField(name="value", type=Set[str])}),
)

PY_CLASS_FOR_CLASS_WITH_STR_TUPLE = PyClass(
    name="ClassWithStrTuple",
    type=ClassWithStrTuple,
    fields=frozenset({PyField(name="value", type=Tuple[str])}),  # type: ignore
)
PY_CLASS_FOR_CLASS_WITH_STR_INT_UNION = PyClass(
    name="ClassWithStrIntUnion",
    type=ClassWithStrIntUnion,
    fields=frozenset({PyField(name="value", type=Union[str, int])}),  # type: ignore
)
PY_CLASS_FOR_CLASS_WITH_STR_FROZEN_SET = PyClass(
    name="ClassWithStrFrozenSet",
    type=ClassWithStrFrozenSet,
    fields=frozenset({PyField(name="value", type=FrozenSet[str])}),
)
PY_CLASS_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT = PyClass(
    name="ClassWithStrStrDefaultDict",
    type=ClassWithStrStrDefaultDict,
    fields=frozenset({PyField(name="value", type=DefaultDict[str, str])}),
)


@dataclass
class ClassFixture:
    cls: Type
    py_class: PyClass


# todo classes for each terminating type


@pytest.fixture
def simple_demo_class():  # todo rename to EmptyDemoClass
    return ClassFixture(cls=SimpleDemoClass, py_class=PY_CLASS_FOR_SIMPLE_DEMO_CLASS)


@pytest.fixture
def class_with_simple_demo_class():
    return ClassFixture(
        cls=ClassWithSimpleDemoClass, py_class=PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS
    )


@pytest.fixture
def class_with_class_with_simple_demo_class():
    return ClassFixture(
        cls=ClassWithClassWithSimpleDemoClass,
        py_class=PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS,
    )


@pytest.fixture
def first_class_in_cycle():
    return ClassFixture(
        cls=FirstClassInCycle, py_class=PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE
    )


@pytest.fixture
def second_class_in_cycle():
    return ClassFixture(
        cls=SecondClassInCycle, py_class=PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE
    )


@pytest.fixture
def class_with_int():
    return ClassFixture(cls=ClassWithInt, py_class=PY_CLASS_FOR_CLASS_WITH_INT)


@pytest.fixture
def class_with_float():
    return ClassFixture(cls=ClassWithFloat, py_class=PY_CLASS_FOR_CLASS_WITH_FLOAT)


@pytest.fixture
def class_with_str():
    return ClassFixture(cls=ClassWithStr, py_class=PY_CLASS_FOR_CLASS_WITH_STR)


@pytest.fixture
def class_with_bytes():
    return ClassFixture(cls=ClassWithBytes, py_class=PY_CLASS_FOR_CLASS_WITH_BYTES)


@pytest.fixture
def class_with_bool():
    return ClassFixture(cls=ClassWithBool, py_class=PY_CLASS_FOR_CLASS_WITH_BOOL)


@pytest.fixture
def class_with_datetime():
    return ClassFixture(
        cls=ClassWithDatetime, py_class=PY_CLASS_FOR_CLASS_WITH_DATETIME
    )


@pytest.fixture
def class_with_uuid():
    return ClassFixture(cls=ClassWithUUID, py_class=PY_CLASS_FOR_CLASS_WITH_UUID)


@pytest.fixture
def class_with_str_set():
    return ClassFixture(cls=ClassWithStrSet, py_class=PY_CLASS_FOR_CLASS_WITH_STR_SET)


@pytest.fixture
def class_with_str_tuple():
    return ClassFixture(
        cls=ClassWithStrTuple, py_class=PY_CLASS_FOR_CLASS_WITH_STR_TUPLE
    )


@pytest.fixture
def class_with_str_int_union():
    return ClassFixture(
        cls=ClassWithStrIntUnion, py_class=PY_CLASS_FOR_CLASS_WITH_STR_INT_UNION
    )


@pytest.fixture
def class_with_str_frozen_set():
    return ClassFixture(
        cls=ClassWithStrFrozenSet, py_class=PY_CLASS_FOR_CLASS_WITH_STR_FROZEN_SET
    )


@pytest.fixture
def class_with_str_str_default_dict():
    return ClassFixture(
        cls=ClassWithStrStrDefaultDict,
        py_class=PY_CLASS_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT,
    )


@pytest.fixture
def class_with_str_list():
    return ClassFixture(cls=ClassWithStrList, py_class=PY_CLASS_FOR_CLASS_WITH_STR_LIST)


@pytest.fixture
def class_with_str_str_dict():
    return ClassFixture(
        cls=ClassWithStrStrDict, py_class=PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT
    )


@pytest.fixture
def class_with_simple_demo_class_list():
    return ClassFixture(
        cls=ClassWithSimpleDemoClassList,
        py_class=PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST,
    )


@pytest.fixture
def class_with_generic_member():
    return ClassFixture(
        cls=ClassWithGenericMember,
        py_class=PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER,
    )


@pytest.fixture
def class_with_deep_nested_generics():
    return ClassFixture(
        cls=ClassWithDeepNestedGenerics,
        py_class=PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
    )
