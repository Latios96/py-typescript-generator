from typing import Type

import pytest
from ordered_set import OrderedSet

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)
from py_typescript_generator.model_parser.model_parser import (
    ModelParser,
    NoParserForClassFoundException,
    IsNotAClassException,
)


class SimpleDemoClass:
    pass


class ClassWithSimpleDemoClass:
    simple_demo_class: SimpleDemoClass


class ClassWithClassWithSimpleDemoClass:
    class_with_simple_demo_class: ClassWithSimpleDemoClass


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


class DemoParser(AbstractClassParser):
    def accepts_class(self, cls: Type) -> bool:
        return cls in {
            SimpleDemoClass,
            ClassWithSimpleDemoClass,
            ClassWithClassWithSimpleDemoClass,
        }

    def parse(self, cls: Type) -> PyClass:
        if cls == SimpleDemoClass:
            return PY_CLASS_FOR_SIMPLE_DEMO_CLASS
        elif cls == ClassWithSimpleDemoClass:
            return PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS
        elif cls == ClassWithClassWithSimpleDemoClass:
            return PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS
        raise ValueError(f"Unsupported class: {cls}")


# todo test cyclic dependencies


def test_should_raise_exception_if_no_parser_for_class_was_found():
    class UnknownClass:
        pass

    model_parser = ModelParser([UnknownClass], [DemoParser()])

    with pytest.raises(NoParserForClassFoundException):
        model_parser.parse()


def test_should_raise_exception_if_passed_thing_is_not_a_class():
    model_parser = ModelParser([lambda x: x], [DemoParser()])

    with pytest.raises(IsNotAClassException):
        model_parser.parse()


class TestParseSimpleClass:
    def test_model_should_contain_just_the_simple_class(self):
        model_parser = ModelParser([SimpleDemoClass], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(classes=[PY_CLASS_FOR_SIMPLE_DEMO_CLASS])

    def test_model_should_contain_just_the_simple_class_even_if_supplied_two_timed(
        self,
    ):
        model_parser = ModelParser([SimpleDemoClass, SimpleDemoClass], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(classes=[PY_CLASS_FOR_SIMPLE_DEMO_CLASS])


class TestParseClassWithSimpleClass:
    def test_model_should_contain_both_classes_when_passing_only_with_simple_class(
        self,
    ):
        model_parser = ModelParser([ClassWithSimpleDemoClass], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS,
                    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
                ]
            )
        )

    def test_model_should_contain_both_classes_when_passing_both_classes(self):
        model_parser = ModelParser(
            [ClassWithSimpleDemoClass, SimpleDemoClass], [DemoParser()]
        )

        model = model_parser.parse()

        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS,
                    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
                ]
            )
        )


class TestClassWithClassWithSimpleDemoClass:
    def test_should_parse_through_three_levels(self):
        model_parser = ModelParser([ClassWithClassWithSimpleDemoClass], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS,
                    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS,
                    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
                ]
            )
        )
