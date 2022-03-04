from typing import Type

from py_typescript_generator.model.py_class import PyClass


class AbstractClassParser:
    def accepts_class(self, cls: Type) -> bool:
        raise NotImplementedError()

    def parse(self, cls: Type) -> PyClass:
        raise NotImplementedError()
