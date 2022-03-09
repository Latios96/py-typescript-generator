from dataclasses import fields
from typing import Type

from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.model_parser.class_parsers.abstract_class_parser import (
    AbstractClassParser,
)


class NotADataclassException(RuntimeError):
    def __init__(self, cls: Type):
        super(NotADataclassException, self).__init__(
            f"The class {cls} is not a dataclass."
        )


class DataclassParser(AbstractClassParser):
    def accepts_class(self, cls: Type) -> bool:
        try:
            fields(cls)
            return True
        except TypeError:
            return False

    def parse(self, cls: Type) -> PyClass:
        if not self.accepts_class(cls):
            raise NotADataclassException(cls)
        py_fields = []
        for field in fields(cls):
            py_fields.append(PyField(name=field.name, type=field.type))

        return PyClass(name=cls.__name__, type=cls, fields=tuple(py_fields))
