from dataclasses import dataclass

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
