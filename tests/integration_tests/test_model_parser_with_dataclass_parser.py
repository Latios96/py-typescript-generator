from dataclasses import dataclass
from typing import List, Dict

from ordered_set import OrderedSet

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.model_parser.class_parsers.dataclass_parser import (
    DataclassParser,
)
from py_typescript_generator.model_parser.model_parser import ModelParser


@dataclass
class MySimpleDataClass:
    my_int: int


@dataclass
class MySimpleDataClassWithANestedClass:
    my_simple_data_class: MySimpleDataClass


def test_should_parse_simple_dataclass_correctly():
    model_parser = ModelParser([MySimpleDataClass], [DataclassParser()])

    model = model_parser.parse()

    assert model == Model(
        classes=OrderedSet(
            [
                PyClass(
                    name="MySimpleDataClass",
                    type=MySimpleDataClass,
                    fields=(PyField(name="my_int", type=int),),
                )
            ]
        )
    )


def test_should_parse_simple_dataclass_with_nested_class_correctly():
    model_parser = ModelParser([MySimpleDataClassWithANestedClass], [DataclassParser()])

    model = model_parser.parse()

    assert model == Model(
        classes=OrderedSet(
            [
                PyClass(
                    name="MySimpleDataClassWithANestedClass",
                    type=MySimpleDataClassWithANestedClass,
                    fields=(
                        PyField(name="my_simple_data_class", type=MySimpleDataClass),
                    ),
                ),
                PyClass(
                    name="MySimpleDataClass",
                    type=MySimpleDataClass,
                    fields=(PyField(name="my_int", type=int),),
                ),
            ]
        )
    )


def test_should_parse_dataclass_with_str_list_correctly():
    @dataclass
    class MyDataClass:
        str_list: List[str]

    model_parser = ModelParser([MyDataClass], [DataclassParser()])

    model = model_parser.parse()

    assert model == Model(
        classes=OrderedSet(
            [
                PyClass(
                    name="MyDataClass",
                    type=MyDataClass,
                    fields=(PyField(name="str_list", type=List[str]),),
                )
            ]
        )
    )


def test_should_parse_dataclass_with_custom_class_list_correctly():
    @dataclass
    class CustomClass:
        pass

    @dataclass
    class MyDataClass:
        the_list: List[CustomClass]

    model_parser = ModelParser([MyDataClass], [DataclassParser()])

    model = model_parser.parse()

    assert model == Model(
        classes=OrderedSet(
            [
                PyClass(
                    name="MyDataClass",
                    type=MyDataClass,
                    fields=(PyField(name="the_list", type=List[CustomClass]),),
                ),
                PyClass(name="CustomClass", type=CustomClass, fields=()),
            ]
        )
    )


def test_should_parse_dataclass_with_nested_generics_correctly():
    @dataclass
    class CustomClass:
        pass

    @dataclass
    class MyDataClass:
        the_dict: Dict[str, List[Dict[str, CustomClass]]]

    model_parser = ModelParser([MyDataClass], [DataclassParser()])

    model = model_parser.parse()

    assert model == Model(
        classes=OrderedSet(
            [
                PyClass(
                    name="MyDataClass",
                    type=MyDataClass,
                    fields=(
                        PyField(
                            name="the_dict",
                            type=Dict[str, List[Dict[str, CustomClass]]],
                        ),
                    ),
                ),
                PyClass(name="CustomClass", type=CustomClass, fields=()),
            ]
        )
    )
