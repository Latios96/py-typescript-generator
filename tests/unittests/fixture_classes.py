from dataclasses import dataclass
from typing import List, Dict, TypeVar, Generic, Type

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


class ClassWithTerminatingType:
    an_int: int


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
PY_CLASS_FOR_CLASS_WITH_TERMINATING_TYPE = PyClass(
    name="ClassWithTerminatingType",
    type=ClassWithTerminatingType,
    fields=frozenset({PyField(name="an_int", type=int)}),
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
