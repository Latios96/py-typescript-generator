from dataclasses import dataclass

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.model_parser.class_parsers.dataclass_parser import (
    DataclassParser,
)


class TestAccept:
    def test_should_accept_dataclass(self):
        @dataclass
        class MyDataClass:
            pass

        dataclass_parser = DataclassParser()

        assert dataclass_parser.accepts_class(MyDataClass)

    def test_should_not_accept_non_dataclass(self):
        class NotADataclass:
            pass

        dataclass_parser = DataclassParser()

        assert not dataclass_parser.accepts_class(NotADataclass)


def test_should_parse_empty_dataclass_class():
    @dataclass
    class EmptyDataClass:
        pass

    dataclass_parser = DataclassParser()

    py_class = dataclass_parser.parse(EmptyDataClass)

    assert py_class == PyClass(
        name="EmptyDataClass", type=EmptyDataClass, fields=frozenset()
    )


def test_should_parse_dataclass_class():
    @dataclass
    class MyDataClass:
        value: int

    dataclass_parser = DataclassParser()

    py_class = dataclass_parser.parse(MyDataClass)

    assert py_class == PyClass(
        name="MyDataClass",
        type=MyDataClass,
        fields=frozenset([PyField(name="value", type=int)]),
    )
