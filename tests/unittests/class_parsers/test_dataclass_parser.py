from dataclasses import dataclass
from typing import List, Dict

import pytest

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.model_parser.class_parsers.dataclass_parser import (
    DataclassParser,
    NotADataclassException,
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

    assert py_class == PyClass(name="EmptyDataClass", type=EmptyDataClass, fields=())


def test_should_parse_dataclass_class():
    @dataclass
    class MyDataClass:
        value: int

    dataclass_parser = DataclassParser()

    py_class = dataclass_parser.parse(MyDataClass)

    assert py_class == PyClass(
        name="MyDataClass",
        type=MyDataClass,
        fields=(PyField(name="value", type=int),),
    )


def test_parsing_a_non_dataclass_should_raise_NotADataclassException():
    class NotADataclass:
        pass

    dataclass_parser = DataclassParser()

    with pytest.raises(NotADataclassException):
        dataclass_parser.parse(NotADataclass)


def test_parse_dataclass_with_str_list():
    @dataclass
    class MyDataClass:
        str_list: List[str]

    dataclass_parser = DataclassParser()

    py_class = dataclass_parser.parse(MyDataClass)

    assert py_class == PyClass(
        name="MyDataClass",
        type=MyDataClass,
        fields=(PyField(name="str_list", type=List[str]),),
    )


def test_parse_dataclass_with_custom_class_list():
    class CustomClass:
        pass

    @dataclass
    class MyDataClass:
        the_list: List[CustomClass]

    dataclass_parser = DataclassParser()

    py_class = dataclass_parser.parse(MyDataClass)

    assert py_class == PyClass(
        name="MyDataClass",
        type=MyDataClass,
        fields=(PyField(name="the_list", type=List[CustomClass]),),
    )


def test_parse_dataclass_with_nested_generics():
    class CustomClass:
        pass

    @dataclass
    class MyDataClass:
        the_dict: Dict[str, List[Dict[str, CustomClass]]]

    dataclass_parser = DataclassParser()

    py_class = dataclass_parser.parse(MyDataClass)

    assert py_class == PyClass(
        name="MyDataClass",
        type=MyDataClass,
        fields=(
            PyField(name="the_dict", type=Dict[str, List[Dict[str, CustomClass]]]),
        ),
    )
