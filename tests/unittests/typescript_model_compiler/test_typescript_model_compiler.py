import pytest

from py_typescript_generator.model.model import Model
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.typescript_model_compiler import (
    TypescriptModelCompiler,
)


@pytest.mark.parametrize(
    "fixture_name",
    [
        "class_with_int",
        "class_with_str",
        "class_with_float",
        "class_with_bool",
        "class_with_bytes",
        "class_with_datetime",
        "class_with_uuid",
    ],
)
def test_should_compile_class_with_scalar_types(fixture_name, request):
    class_fixture = request.getfixturevalue(fixture_name)
    model = Model.of_classes([class_fixture.py_class])
    model_compiler = TypescriptModelCompiler()

    ts_model = model_compiler.compile(model)

    assert ts_model == TsModel.of_object_types([class_fixture.ts_object_type])
