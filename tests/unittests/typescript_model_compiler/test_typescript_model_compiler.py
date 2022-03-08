from datetime import datetime
from uuid import UUID

from ordered_set import OrderedSet

from py_typescript_generator.model.model import Model
from py_typescript_generator.model.py_class import PyClass
from py_typescript_generator.model.py_field import PyField
from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)
from py_typescript_generator.typescript_model_compiler.typescript_model_compiler import (
    TypescriptModelCompiler,
)
from py_typescript_generator.typescript_model_compiler.well_known_types import (
    TS_STRING,
    TS_NUMBER,
    TS_BOOLEAN,
)


class ClassWithScalarTypes:
    string_value: str
    int_value: int
    float_value: float
    boolean_value: bool
    bytes_value: bytes
    datetime_value: datetime
    uuid_value: UUID


def test_should_compile_simple_class():
    model = Model.of_classes(
        [
            PyClass(
                name="ClassWithScalarTypes",
                type=ClassWithScalarTypes,
                fields=frozenset(
                    [
                        PyField(name="string_value", type=str),
                        PyField(name="int_value", type=int),
                        PyField(name="float_value", type=float),
                        PyField(name="boolean_value", type=bool),
                        PyField(name="bytes_value", type=bytes),
                        PyField(name="datetime_value", type=datetime),
                        PyField(name="uuid_value", type=UUID),
                    ]
                ),
            )
        ]
    )
    model_compiler = TypescriptModelCompiler()

    ts_model = model_compiler.compile(model)

    assert ts_model == TsModel(
        types=OrderedSet(
            [
                TsObjectType(
                    name="ClassWithScalarTypes",
                    fields=frozenset(
                        [
                            TsField(name="string_value", type=TS_STRING),
                            TsField(name="int_value", type=TS_NUMBER),
                            TsField(name="float_value", type=TS_NUMBER),
                            TsField(name="boolean_value", type=TS_BOOLEAN),
                            TsField(name="bytes_value", type=TS_STRING),
                            TsField(name="datetime_value", type=TS_STRING),
                            TsField(name="uuid_value", type=TS_STRING),
                        ]
                    ),
                )
            ]
        )
    )
