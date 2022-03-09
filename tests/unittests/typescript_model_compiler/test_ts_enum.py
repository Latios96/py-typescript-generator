from py_typescript_generator.typescript_model_compiler.ts_enum import TsEnumValue


def test_format_string_value():
    ts_enum_value = TsEnumValue(name="TEST", value="VALUE")

    assert ts_enum_value.format_value() == '"VALUE"'


def test_format_int_value():
    ts_enum_value = TsEnumValue(name="TEST", value=1)

    assert ts_enum_value.format_value() == "1"
