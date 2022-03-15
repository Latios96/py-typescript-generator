from dataclasses import dataclass

from py_typescript_generator.generation_pipeline.typescript_generation_pipeline_builder import (
    TypeGenerationPipelineBuilder,
)


def test_build_pipeline(tmp_path):
    @dataclass
    class MyExampleClass:
        value: int

    output_file = tmp_path / "test.ts"
    TypeGenerationPipelineBuilder().for_types([MyExampleClass]).with_type_overrides(
        {int: str}
    ).convert_field_names_to_camel_case().to_file(output_file).build().run()

    with open(output_file, "r") as f:
        content = f.read()

    assert (
        content
        == """export interface MyExampleClass {
    value: string
}
"""
    )
