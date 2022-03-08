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
from tests.unittests.demo_parser_fixture import DemoParser
from tests.unittests.fixture_classes import (
    ClassFixture,
)


def test_should_raise_exception_if_no_parser_for_class_was_found(demo_parser):
    class UnknownClass:
        pass

    model_parser = ModelParser([UnknownClass], [demo_parser])

    with pytest.raises(NoParserForClassFoundException):
        model_parser.parse()


def test_should_raise_exception_if_passed_thing_is_not_a_class(demo_parser):
    model_parser = ModelParser([lambda x: x], [demo_parser])

    with pytest.raises(IsNotAClassException):
        model_parser.parse()


class TestParseSimpleClass:
    def test_model_should_contain_just_the_simple_class(
        self, empty_class: ClassFixture, demo_parser: DemoParser
    ) -> None:
        model_parser = ModelParser([empty_class.cls], [demo_parser])

        model = model_parser.parse()

        assert model == Model(classes=OrderedSet([empty_class.py_class]))

    def test_model_should_contain_just_the_simple_class_even_if_supplied_two_timed(
        self, empty_class: ClassFixture, demo_parser: DemoParser
    ) -> None:
        model_parser = ModelParser([empty_class.cls, empty_class.cls], [demo_parser])

        model = model_parser.parse()

        assert model == Model(classes=OrderedSet([empty_class.py_class]))


class TestParseClassWithSimpleClass:
    def test_model_should_contain_both_classes_when_passing_only_with_simple_class(
        self,
        empty_class: ClassFixture,
        class_with_empty_class: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser([class_with_empty_class.cls], [demo_parser])

        model = model_parser.parse()

        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_empty_class.py_class,
                    empty_class.py_class,
                ]
            )
        )

    def test_model_should_contain_both_classes_when_passing_both_classes(
        self,
        empty_class: ClassFixture,
        class_with_empty_class: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser(
            [class_with_empty_class.cls, empty_class.cls], [demo_parser]
        )

        model = model_parser.parse()

        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_empty_class.py_class,
                    empty_class.py_class,
                ]
            )
        )


class TestClassWithClassWithEmptyClass:
    def test_should_parse_through_three_levels(
        self,
        empty_class: ClassFixture,
        class_with_empty_class: ClassFixture,
        class_with_class_with_empty_class: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser(
            [class_with_class_with_empty_class.cls], [demo_parser]
        )

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_class_with_empty_class.py_class,
                    class_with_empty_class.py_class,
                    empty_class.py_class,
                ]
            )
        )


class TestParsingCycleShouldTerminate:
    def test_parse_only_first_class_in_cycle(
        self,
        first_class_in_cycle: ClassFixture,
        second_class_in_cycle: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser([first_class_in_cycle.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [first_class_in_cycle.py_class, second_class_in_cycle.py_class]
            )
        )

    def test_parse_only_second_class_in_cycle(
        self,
        first_class_in_cycle: ClassFixture,
        second_class_in_cycle: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser([second_class_in_cycle.cls], [demo_parser])

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
        self,
        first_class_in_cycle: ClassFixture,
        second_class_in_cycle: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser(
            [first_class_in_cycle.cls, second_class_in_cycle.cls], [demo_parser]
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
    the_type: Type, class_with_int: ClassFixture
) -> None:
    py_class_with_terminating_type = PyClass(
        name="ClassWithTerminatingType",
        type=class_with_int.cls,
        fields=frozenset({PyField(name="the_type", type=the_type)}),
    )

    class TerminatingTypeClassParser(AbstractClassParser):
        def accepts_class(self, cls: Type) -> bool:
            return True

        def parse(self, cls: Type) -> PyClass:
            return py_class_with_terminating_type

    model_parser = ModelParser([class_with_int.cls], [TerminatingTypeClassParser()])

    model = model_parser.parse()

    assert model == Model(classes=OrderedSet([py_class_with_terminating_type]))


class TestParseGenericTypes:
    def test_parse_class_with_string_list(
        self, class_with_str_list: ClassFixture, demo_parser: DemoParser
    ) -> None:
        model_parser = ModelParser([class_with_str_list.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_str_list.py_class,
                ]
            )
        )

    def test_parse_class_with_str_str_dict(
        self, class_with_str_str_dict: ClassFixture, demo_parser: DemoParser
    ) -> None:
        model_parser = ModelParser([class_with_str_str_dict.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_str_str_dict.py_class,
                ]
            )
        )

    def test_parse_class_with_empty_class_list(
        self,
        empty_class: ClassFixture,
        class_with_empty_class_list: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser([class_with_empty_class_list.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_empty_class_list.py_class,
                    empty_class.py_class,
                ]
            )
        )

    def test_should_parse_generic_class_with_type_var(
        self, class_with_generic_member: ClassFixture, demo_parser: DemoParser
    ) -> None:
        model_parser = ModelParser([class_with_generic_member.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(classes=OrderedSet([class_with_generic_member.py_class]))

    def test_should_parse_deeply_nested_generics(
        self,
        empty_class: ClassFixture,
        class_with_deep_nested_generics: ClassFixture,
        demo_parser: DemoParser,
    ) -> None:
        model_parser = ModelParser([class_with_deep_nested_generics.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(
            classes=OrderedSet(
                [
                    class_with_deep_nested_generics.py_class,
                    empty_class.py_class,
                ]
            )
        )


class TestParseOptional:
    def test_should_parse_optional_int(
        self, class_with_optional_int: ClassFixture, demo_parser: DemoParser
    ) -> None:
        model_parser = ModelParser([class_with_optional_int.cls], [demo_parser])

        model = model_parser.parse()
        assert model == Model(classes=OrderedSet([class_with_optional_int.py_class]))
