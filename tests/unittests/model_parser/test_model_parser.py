from typing import Type, List

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)
from py_typescript_generator.model_parser.model_parser import ModelParser


class SimpleDemoClass:
    pass


PY_CLASS_FOR_SIMPLE_DEMO_CLASS = PyClass(name="SimpleDemoClass", type=SimpleDemoClass)


class DemoParser(AbstractClassParser):
    def accepts_class(self, cls: Type) -> bool:
        return cls in {SimpleDemoClass}

    def parse(self, cls: Type) -> PyClass:
        if cls == SimpleDemoClass:
            return PY_CLASS_FOR_SIMPLE_DEMO_CLASS
        raise ValueError(f"Unsupported class: {cls}")


def test_parse_single_simple_class():
    model_parser = ModelParser([SimpleDemoClass], [DemoParser()])

    model = model_parser.parse()

    assert model == Model(classes=[PY_CLASS_FOR_SIMPLE_DEMO_CLASS])
