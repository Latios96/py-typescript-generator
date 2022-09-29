from dataclasses import dataclass

from py_typescript_generator.generation_pipeline.typescript_generation_pipeline_builder import (
    TypeGenerationPipelineBuilder,
)


def test_build_pipeline(tmp_path):
    @dataclass
    class MyExampleClass:
        value: int

    @dataclass
    class TaggedUnionRoot:
        __json_type_info_attribute__ = "type"

    @dataclass
    class TaggedUnionChild(TaggedUnionRoot):
        type = "CHILD"

    output_file = tmp_path / "some_folder" / "test.ts"
    TypeGenerationPipelineBuilder().for_types(
        [MyExampleClass, TaggedUnionRoot]
    ).with_type_overrides({int: str}).convert_field_names_to_camel_case().to_file(
        output_file
    ).build().run()

    with open(output_file, "r") as f:
        content = f.read()

    assert (
        content
        == """export interface MyExampleClass {
    value: string
}
export interface TaggedUnionChild {
    type: "CHILD"
}
export type TaggedUnionRoot = TaggedUnionChild;
"""
    )
