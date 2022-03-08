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
)


class DemoParser(AbstractClassParser):
    def accepts_class(self, cls: Type) -> bool:
        return cls in {
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
        }

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
        raise ValueError(f"Unsupported class: {cls}")


@pytest.fixture
def demo_parser():
    return DemoParser()
