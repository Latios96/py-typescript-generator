from datetime import datetime
from typing import (
    Type,
    List,
    Set,
    Dict,
    Tuple,
    Union,
    FrozenSet,
    DefaultDict,
)
from uuid import UUID

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
from tests.unittests.fixture_classes import (
    SimpleDemoClass,
    ClassWithSimpleDemoClass,
    ClassWithClassWithSimpleDemoClass,
    FirstClassInCycle,
    SecondClassInCycle,
    ClassWithTerminatingType,
    ClassWithStrList,
    ClassWithStrStrDict,
    ClassWithSimpleDemoClassList,
    ClassWithGenericMember,
    ClassWithDeepNestedGenerics,
    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS,
    PY_CLASS_FOR_CLASS_WITH_CLASS_WITH_SIMPLE_DEMO_CLASS,
    PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE,
    PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE,
    PY_CLASS_FOR_CLASS_WITH_TERMINATING_TYPE,
    PY_CLASS_FOR_CLASS_WITH_STR_LIST,
    PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT,
    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST,
    PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER,
    PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
    ClassFixture,
)


class DemoParser(AbstractClassParser):
    def accepts_class(self, cls: Type) -> bool:
        return cls in {
            SimpleDemoClass,
            ClassWithSimpleDemoClass,
            ClassWithClassWithSimpleDemoClass,
            FirstClassInCycle,
            SecondClassInCycle,
            ClassWithTerminatingType,
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
        elif cls == ClassWithTerminatingType:
            return PY_CLASS_FOR_CLASS_WITH_TERMINATING_TYPE
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
    def test_model_should_contain_just_the_simple_class(
        self, simple_demo_class: ClassFixture
    ) -> None:
        model_parser = ModelParser([simple_demo_class.cls], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(classes=OrderedSet([simple_demo_class.py_class]))

    def test_model_should_contain_just_the_simple_class_even_if_supplied_two_timed(
        self, simple_demo_class: ClassFixture
    ) -> None:
        model_parser = ModelParser(
            [simple_demo_class.cls, simple_demo_class.cls], [DemoParser()]
        )

        model = model_parser.parse()

        assert model == Model(classes=OrderedSet([simple_demo_class.py_class]))


class TestParseClassWithSimpleClass:
    def test_model_should_contain_both_classes_when_passing_only_with_simple_class(
        self,
        simple_demo_class: ClassFixture,
        class_with_simple_demo_class: ClassFixture,
    ) -> None:
        model_parser = ModelParser([class_with_simple_demo_class.cls], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_simple_demo_class.py_class,
                    simple_demo_class.py_class,
                ]
            )
        )

    def test_model_should_contain_both_classes_when_passing_both_classes(
        self,
        simple_demo_class: ClassFixture,
        class_with_simple_demo_class: ClassFixture,
    ) -> None:
        model_parser = ModelParser(
            [class_with_simple_demo_class.cls, simple_demo_class.cls], [DemoParser()]
        )

        model = model_parser.parse()

        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_simple_demo_class.py_class,
                    simple_demo_class.py_class,
                ]
            )
        )


class TestClassWithClassWithSimpleDemoClass:
    def test_should_parse_through_three_levels(
        self,
        simple_demo_class: ClassFixture,
        class_with_simple_demo_class: ClassFixture,
        class_with_class_with_simple_demo_class: ClassFixture,
    ) -> None:
        model_parser = ModelParser(
            [class_with_class_with_simple_demo_class.cls], [DemoParser()]
        )

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_class_with_simple_demo_class.py_class,
                    class_with_simple_demo_class.py_class,
                    simple_demo_class.py_class,
                ]
            )
        )


class TestParsingCycleShouldTerminate:
    def test_parse_only_first_class_in_cycle(
        self, first_class_in_cycle: ClassFixture, second_class_in_cycle: ClassFixture
    ) -> None:
        model_parser = ModelParser([first_class_in_cycle.cls], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [first_class_in_cycle.py_class, second_class_in_cycle.py_class]
            )
        )

    def test_parse_only_second_class_in_cycle(
        self, first_class_in_cycle: ClassFixture, second_class_in_cycle: ClassFixture
    ) -> None:
        model_parser = ModelParser([second_class_in_cycle.cls], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    second_class_in_cycle.py_class,
                    first_class_in_cycle.py_class,
                ]
            )
        )

    def test_parse_all_in_cycle(
        self, first_class_in_cycle: ClassFixture, second_class_in_cycle: ClassFixture
    ) -> None:
        model_parser = ModelParser(
            [first_class_in_cycle.cls, second_class_in_cycle.cls], [DemoParser()]
        )

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [first_class_in_cycle.py_class, second_class_in_cycle.py_class]
            )
        )


@pytest.mark.parametrize(
    "the_type",
    [
        int,
        float,
        complex,
        str,
        bytes,
        bool,
        datetime,
        UUID,
        List[int],
        Set[int],
        Dict[str, str],
        Tuple[int],
        Union[str, int],
        FrozenSet[int],
        DefaultDict[str, str],
    ],
)
def test_parse_builtin_terminating_types(
    the_type: Type, class_with_terminating_type: ClassFixture
) -> None:
    py_class_with_terminating_type = PyClass(
        name="ClassWithTerminatingType",
        type=class_with_terminating_type.cls,
        fields=frozenset({PyField(name="the_type", type=the_type)}),
    )

    class TerminatingTypeClassParser(AbstractClassParser):
        def accepts_class(self, cls: Type) -> bool:
            return True

        def parse(self, cls: Type) -> PyClass:
            return py_class_with_terminating_type

    model_parser = ModelParser(
        [class_with_terminating_type.cls], [TerminatingTypeClassParser()]
    )

    model = model_parser.parse()

    assert model == Model(classes=OrderedSet([py_class_with_terminating_type]))


class TestParseGenericTypes:
    def test_parse_class_with_string_list(
        self, class_with_str_list: ClassFixture
    ) -> None:
        model_parser = ModelParser([class_with_str_list.cls], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_str_list.py_class,
                ]
            )
        )

    def test_parse_class_with_str_str_dict(
        self, class_with_str_str_dict: ClassFixture
    ) -> None:
        model_parser = ModelParser([class_with_str_str_dict.cls], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_str_str_dict.py_class,
                ]
            )
        )

    def test_parse_class_with_simple_demo_class_list(self, simple_demo_class):
        model_parser = ModelParser([ClassWithSimpleDemoClassList], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST,
                    simple_demo_class.py_class,
                ]
            )
        )

    def test_should_parse_generic_class_with_type_var(self):
        model_parser = ModelParser([ClassWithGenericMember], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet([PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER])
        )

    def test_should_parse_deeply_nested_generics(self, simple_demo_class):
        model_parser = ModelParser([ClassWithDeepNestedGenerics], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
                    simple_demo_class.py_class,
                ]
            )
        )
