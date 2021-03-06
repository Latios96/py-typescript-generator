from py_typescript_generator.typescript_model_compiler.ts_field import TsField
from py_typescript_generator.typescript_model_compiler.ts_model import TsModel
from py_typescript_generator.typescript_model_compiler.ts_object_type import (
    TsObjectType,
)


class TypescriptEmitter:
    def emit(self, ts_model: TsModel) -> str:
        typescript_str = ""
        for ts_enum in ts_model.enums:
            typescript_str += self._emit_enum(ts_enum)
        for ts_type in ts_model.types:
            typescript_str += self._emit_type(ts_type)
        return typescript_str

    def _emit_enum(self, ts_enum):
        enum_template = "export enum "
        enum_template += ts_enum.name
        enum_template += " {\n"

        for value in ts_enum.values:
            enum_template += f"    {value.name} = {value.format_value()},\n"

        enum_template += "}\n"

        return enum_template

    def _emit_type(self, ts_type: TsObjectType) -> str:
        type_template = "export interface "
        type_template += ts_type.name
        type_template += " {\n"

        for field in ts_type.fields:
            field_optional_specifier = self._emit_field_optional_specifier(field)
            field_type = self._emit_field_type(field)
            type_template += (
                f"    {field.name}{field_optional_specifier}: {field_type}\n"
            )

        type_template += "}\n"

        return type_template

    def _emit_field_optional_specifier(self, field: TsField) -> str:
        if field.type.is_optional:
            return "?"
        return ""

    def _emit_field_type(self, field: TsField) -> str:
        if field.type.is_optional:
            return field.type.as_non_optional_type().format_as_type_reference()
        return field.type.format_as_type_reference()
