import pytest

from py_typescript_generator.generation_pipeline.typescript_generation_pipeline_builder import (
    TypeGenerationPipelineBuilder,
    NoOutputFileDefined,
)
from py_typescript_generator.typescript_model_compiler.typescript_model_compiler import (
    CaseFormat,
)


def test_build_fails_because_missing_output_file():
    with pytest.raises(NoOutputFileDefined):
        TypeGenerationPipelineBuilder().build()


def test_with_defaults_and_output_file_builds_correctly():
    pipeline = TypeGenerationPipelineBuilder().to_file("test.ts").build()

    assert pipeline.types == []
    assert pipeline.type_overrides == {}
    assert pipeline.case_format == CaseFormat.KEEP_CASING
    assert pipeline.output_file == "test.ts"


def test_provided_options_builds_correctly():
    pipeline = (
        TypeGenerationPipelineBuilder()
        .for_types([str, int])
        .with_type_overrides({int: str})
        .convert_field_names_to_camel_case()
        .to_file("test.ts")
        .build()
    )

    assert pipeline.types == [str, int]
    assert pipeline.type_overrides == {int: str}
    assert pipeline.case_format == CaseFormat.CAMEL_CASE
    assert pipeline.output_file == "test.ts"
