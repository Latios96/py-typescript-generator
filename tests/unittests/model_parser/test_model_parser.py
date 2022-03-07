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
    Generic,
    TypeVar,
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
    def test_model_should_contain_just_the_simple_class(self) -> None:
        model_parser = ModelParser([SimpleDemoClass], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(classes=OrderedSet([PY_CLASS_FOR_SIMPLE_DEMO_CLASS]))

    def test_model_should_contain_just_the_simple_class_even_if_supplied_two_timed(
        self,
    ) -> None:
        model_parser = ModelParser([SimpleDemoClass, SimpleDemoClass], [DemoParser()])

        model = model_parser.parse()

        assert model == Model(classes=OrderedSet([PY_CLASS_FOR_SIMPLE_DEMO_CLASS]))


class TestParseClassWithSimpleClass:
    def test_model_should_contain_both_classes_when_passing_only_with_simple_class(
        self,
    ) -> None:
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

    def test_model_should_contain_both_classes_when_passing_both_classes(self) -> None:
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
    def test_should_parse_through_three_levels(self) -> None:
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


@pytest.mark.parametrize(
    "class_combinations,parsed_order",
    [
        (
            [FirstClassInCycle],
            [PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE, PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE],
        ),
        (
            [SecondClassInCycle],
            [
                PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE,
                PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE,
            ],
        ),
        (
            [FirstClassInCycle, SecondClassInCycle],
            [PY_CLASS_FOR_FIRST_CLASS_IN_CYCLE, PY_CLASS_FOR_SECOND_CLASS_IN_CYCLE],
        ),
    ],
)
def test_parsing_cycle_should_terminate(
    class_combinations: List[Type], parsed_order: List[PyClass]
) -> None:
    model_parser = ModelParser(class_combinations, [DemoParser()])

    model = model_parser.parse()
    assert model == Model(classes=OrderedSet(parsed_order))


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
def test_parse_builtin_terminating_types(the_type: Type) -> None:
    class_with_terminating_type = PyClass(
        name="ClassWithTerminatingType",
        type=ClassWithTerminatingType,
        fields=frozenset({PyField(name="the_type", type=the_type)}),
    )

    class TerminatingTypeClassParser(AbstractClassParser):
        def accepts_class(self, cls: Type) -> bool:
            return True

        def parse(self, cls: Type) -> PyClass:
            return class_with_terminating_type

    model_parser = ModelParser(
        [ClassWithTerminatingType], [TerminatingTypeClassParser()]
    )

    model = model_parser.parse()

    assert model == Model(classes=OrderedSet([class_with_terminating_type]))


class TestParseGenericTypes:
    def test_parse_class_with_string_list(self):
        model_parser = ModelParser([ClassWithStrList], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_STR_LIST,
                ]
            )
        )

    def test_parse_class_with_str_str_dict(self):
        model_parser = ModelParser([ClassWithStrStrDict], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_STR_STR_DICT,
                ]
            )
        )

    def test_parse_class_with_simple_demo_class_list(self):
        model_parser = ModelParser([ClassWithSimpleDemoClassList], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_SIMPLE_DEMO_CLASS_LIST,
                    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
                ]
            )
        )

    def test_should_parse_generic_class_with_type_var(self):
        model_parser = ModelParser([ClassWithGenericMember], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet([PY_CLASS_FOR_CLASS_WITH_GENERIC_MEMBER])
        )

    def test_should_parse_deeply_nested_generics(self):
        model_parser = ModelParser([ClassWithDeepNestedGenerics], [DemoParser()])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    PY_CLASS_FOR_CLASS_WITH_DEEP_NESTED_GENERICS,
                    PY_CLASS_FOR_SIMPLE_DEMO_CLASS,
                ]
            )
        )
