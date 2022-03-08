from py_typescript_generator.typescript_model_compiler.ts_type import TsType


class TestAsOptionalType:
    def test_non_optional_type_should_get_optional(self):
        ts_type = TsType(name="test", is_optional=False)

        new_ts_type = ts_type.as_optional_type()

        assert new_ts_type.is_optional

    def test_already_optional_type_should_stay_optional(self):
        ts_type = TsType(name="test", is_optional=True)

        new_ts_type = ts_type.as_optional_type()

        assert new_ts_type.is_optional


class TestWithIsOptional:
    def test_should_create_optional_type(self):
        ts_type = TsType(name="test", is_optional=False)

        new_ts_type = ts_type.with_is_optional(True)

        assert new_ts_type.is_optional

    def test_already_optional_type_should_stay_optional(self):
        ts_type = TsType(name="test", is_optional=False)

        new_ts_type = ts_type.with_is_optional(True)

        assert new_ts_type.is_optional
