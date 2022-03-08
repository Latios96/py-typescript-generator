from typing import Type

import pytest

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)
from tests.unittests.fixture_classes import (
    SimpleDemoClass,
    ClassWithSimpleDemoClass,
    ClassWithClassWithSimpleDemoClass,
    FirstClassInCycle,
    SecondClassInCycle,
    ClassWithInt,
    ClassWithStrList,
    ClassWithSimpleDemoClassList,
    ClassWithGenericMember,
    ClassWithStrStrDict,
    ClassWithDeepNestedGenerics,
    ClassWithFloat,
    ClassWithStr,
    ClassWithBytes,
    ClassWithBool,
    ClassWithDatetime,
    ClassWithUUID,
    ClassWithStrSet,
    ClassWithStrTuple,
    ClassWithStrIntUnion,
    ClassWithStrFrozenSet,
    ClassWithStrStrDefaultDict,
    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS,
    PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS,
    PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE,
    PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE,
    PY_CLASS_FOR_CLASS_WITH_INT,
    PY_CLASS_FOR_CLASS_WITH_STR_LIST,
    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST,
    PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER,
    PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT,
    PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
    PY_CLASS_FOR_CLASS_WITH_FLOAT,
    PY_CLASS_FOR_CLASS_WITH_BYTES,
    PY_CLASS_FOR_CLASS_WITH_STR,
    PY_CLASS_FOR_CLASS_WITH_BOOL,
    PY_CLASS_FOR_CLASS_WITH_DATETIME,
    PY_CLASS_FOR_CLASS_WITH_UUID,
    PY_CLASS_FOR_CLASS_WITH_STR_SET,
    PY_CLASS_FOR_CLASS_WITH_STR_TUPLE,
    PY_CLASS_FOR_CLASS_WITH_STR_INT_UNION,
    PY_CLASS_FOR_CLASS_WITH_STR_FROZEN_SET,
    PY_CLASS_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT,
)


class DemoParser(AbstractClassParser):
    def accepts_class(self, cls: Type) -> bool:
        return cls in [
            SimpleDemoClass,
            ClassWithSimpleDemoClass,
            ClassWithClassWithSimpleDemoClass,
            FirstClassInCycle,
            SecondClassInCycle,
            ClassWithInt,
            ClassWithStrList,
            ClassWithSimpleDemoClassList,
            ClassWithGenericMember,
            ClassWithStrStrDict,
            ClassWithDeepNestedGenerics,
            ClassWithFloat,
            ClassWithStr,
            ClassWithBytes,
            ClassWithBool,
            ClassWithDatetime,
            ClassWithUUID,
            ClassWithStrSet,
            ClassWithStrTuple,
            ClassWithStrIntUnion,
            ClassWithStrFrozenSet,
            ClassWithStrStrDefaultDict,
        ]

    def parse(self, cls: Type) -> PyClass:
        if cls == SimpleDemoClass:
            return PY_CLASS_FOR_SIMPLE_DEMO_CLASS
        elif cls == ClassWithSimpleDemoClass:
            return PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS
        elif cls == ClassWithClassWithSimpleDemoClass:
            return PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS
        elif cls == FirstClassInCycle:
            return PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE
        elif cls == SecondClassInCycle:
            return PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE
        elif cls == ClassWithInt:
            return PY_CLASS_FOR_CLASS_WITH_INT
        elif cls == ClassWithStrList:
            return PY_CLASS_FOR_CLASS_WITH_STR_LIST
        elif cls == ClassWithSimpleDemoClassList:
            return PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST
        elif cls == ClassWithGenericMember:
            return PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER
        elif cls == ClassWithStrStrDict:
            return PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT
        elif cls == ClassWithDeepNestedGenerics:
            return PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS
        elif cls == ClassWithFloat:
            return PY_CLASS_FOR_CLASS_WITH_FLOAT
        elif cls == ClassWithStr:
            return PY_CLASS_FOR_CLASS_WITH_STR
        elif cls == ClassWithBytes:
            return PY_CLASS_FOR_CLASS_WITH_BYTES
        elif cls == ClassWithBool:
            return PY_CLASS_FOR_CLASS_WITH_BOOL
        elif cls == ClassWithDatetime:
            return PY_CLASS_FOR_CLASS_WITH_DATETIME
        elif cls == ClassWithUUID:
            return PY_CLASS_FOR_CLASS_WITH_UUID
        elif cls == ClassWithStrSet:
            return PY_CLASS_FOR_CLASS_WITH_STR_SET
        elif cls == ClassWithStrTuple:
            return PY_CLASS_FOR_CLASS_WITH_STR_TUPLE
        elif cls == ClassWithStrIntUnion:
            return PY_CLASS_FOR_CLASS_WITH_STR_INT_UNION
        elif cls == ClassWithStrFrozenSet:
            return PY_CLASS_FOR_CLASS_WITH_STR_FROZEN_SET
        elif cls == ClassWithStrStrDefaultDict:
            return PY_CLASS_FOR_CLASS_WITH_STR_STR_DEFAULT_DICT
        raise ValueError(f"Unsupported class: {cls}")


@pytest.fixture
def demo_parser():
    return DemoParser()
