import pytest

from py_typescript_generator.typescript_model_compiler.ts_array import TsArray
from py_typescript_generator.typescript_model_compiler.ts_interface import TsInterface
from py_typescript_generator.typescript_model_compiler.ts_mapped_type import (
    TsMappedType,
)
from py_typescript_generator.typescript_model_compiler.ts_type import TsType
from py_typescript_generator.typescript_model_compiler.well_known_types import (
    TS_STRING,
    TS_NUMBER,
)


class TestAsOptionalType:
    @pytest.mark.parametrize(
        "ts_type_before,ts_type_after",
        [
            (
                TsType(name="test", is_optional=False),
                TsType(name="test", is_optional=True),
            ),
            (
                TsInterface(name="test", is_optional=False),
                TsInterface(name="test", is_optional=True),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=False),
                TsArray(wrapped_type=TS_STRING, is_optional=True),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
            ),
        ],
    )
    def test_non_optional_type_should_get_optional(self, ts_type_before, ts_type_after):
        new_ts_type = ts_type_before.as_optional_type()

        assert new_ts_type == ts_type_after

    @pytest.mark.parametrize(
        "ts_type_before,ts_type_after",
        [
            (
                TsType(name="test", is_optional=True),
                TsType(name="test", is_optional=True),
            ),
            (
                TsInterface(name="test", is_optional=True),
                TsInterface(name="test", is_optional=True),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=True),
                TsArray(wrapped_type=TS_STRING, is_optional=True),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
            ),
        ],
    )
    def test_already_optional_type_should_stay_optional(
        self, ts_type_before, ts_type_after
    ):
        new_ts_type = ts_type_before.as_optional_type()

        assert new_ts_type == ts_type_after


class TestAsNonOptionalType:
    @pytest.mark.parametrize(
        "ts_type_before,ts_type_after",
        [
            (
                TsType(name="test", is_optional=True),
                TsType(name="test", is_optional=False),
            ),
            (
                TsInterface(name="test", is_optional=True),
                TsInterface(name="test", is_optional=False),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=True),
                TsArray(wrapped_type=TS_STRING, is_optional=False),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
            ),
        ],
    )
    def test_optional_type_should_get_non_optional(self, ts_type_before, ts_type_after):
        new_ts_type = ts_type_before.as_non_optional_type()

        assert new_ts_type == ts_type_after

    @pytest.mark.parametrize(
        "ts_type_before,ts_type_after",
        [
            (
                TsType(name="test", is_optional=False),
                TsType(name="test", is_optional=False),
            ),
            (
                TsInterface(name="test", is_optional=False),
                TsInterface(name="test", is_optional=False),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=False),
                TsArray(wrapped_type=TS_STRING, is_optional=False),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
            ),
        ],
    )
    def test_already_non_optional_type_should_stay_non_optional(
        self, ts_type_before, ts_type_after
    ):
        new_ts_type = ts_type_before.as_non_optional_type()

        assert new_ts_type == ts_type_after


class TestWithIsOptional:
    @pytest.mark.parametrize(
        "ts_type_before,ts_type_after",
        [
            (
                TsType(name="test", is_optional=False),
                TsType(name="test", is_optional=True),
            ),
            (
                TsInterface(name="test", is_optional=False),
                TsInterface(name="test", is_optional=True),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=False),
                TsArray(wrapped_type=TS_STRING, is_optional=True),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
            ),
        ],
    )
    def test_should_create_optional_type(self, ts_type_before, ts_type_after):
        new_ts_type = ts_type_before.with_is_optional(True)

        assert new_ts_type == ts_type_after

    @pytest.mark.parametrize(
        "ts_type_before,ts_type_after",
        [
            (
                TsType(name="test", is_optional=True),
                TsType(name="test", is_optional=True),
            ),
            (
                TsInterface(name="test", is_optional=True),
                TsInterface(name="test", is_optional=True),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=True),
                TsArray(wrapped_type=TS_STRING, is_optional=True),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
            ),
        ],
    )
    def test_already_optional_type_should_stay_optional(
        self, ts_type_before, ts_type_after
    ):
        new_ts_type = ts_type_before.with_is_optional(True)

        assert new_ts_type == ts_type_after


@pytest.mark.parametrize(
    "ts_type,the_str",
    [
        (
            TsType(name="test", is_optional=False),
            "TsType(name='test', is_optional='False')",
        ),
        (
            TsInterface(name="test", is_optional=False),
            "TsInterface(name='test', is_optional='False')",
        ),
        (
            TsArray(wrapped_type=TS_STRING, is_optional=False),
            "TsArray(name='string[]', wrapped_type=TsType(name='string', is_optional='False'), is_optional='False')",
        ),
        (
            TsMappedType(wrapped_type=TS_STRING, is_optional=False),
            "TsMappedType(name='{[index: string]: string}', wrapped_type=TsType(name='string', is_optional='False'), is_optional='False')",
        ),
    ],
)
def test_dunder_str(ts_type, the_str):
    assert str(ts_type) == the_str


@pytest.mark.parametrize(
    "ts_type,the_repr",
    [
        (
            TsType(name="test", is_optional=False),
            "TsType(name='test', is_optional='False')",
        ),
        (
            TsInterface(name="test", is_optional=False),
            "TsInterface(name='test', is_optional='False')",
        ),
        (
            TsArray(wrapped_type=TS_STRING, is_optional=False),
            "TsArray(name='string[]', wrapped_type=TsType(name='string', is_optional='False'), is_optional='False')",
        ),
        (
            TsMappedType(wrapped_type=TS_STRING, is_optional=False),
            "TsMappedType(name='{[index: string]: string}', wrapped_type=TsType(name='string', is_optional='False'), is_optional='False')",
        ),
    ],
)
def test_dunder_repr(ts_type, the_repr):
    assert repr(ts_type) == the_repr


class TestEqualsAndHash:
    @pytest.mark.parametrize(
        "ts_type1,ts_type2",
        [
            (
                TsType(name="test", is_optional=False),
                TsType(name="test", is_optional=False),
            ),
            (
                TsInterface(name="test", is_optional=False),
                TsInterface(name="test", is_optional=False),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=False),
                TsArray(wrapped_type=TS_STRING, is_optional=False),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
            ),
        ],
    )
    def test_equal_ts_types_should_have_same_hash(self, ts_type1, ts_type2):
        assert ts_type1 == ts_type2
        assert hash(ts_type1) == hash(ts_type2)
        assert len({ts_type1, ts_type1}) == 1

    @pytest.mark.parametrize(
        "ts_type1,ts_type2",
        [
            (
                TsType(name="test1", is_optional=False),
                TsType(name="test2", is_optional=False),
            ),
            (
                TsType(name="test", is_optional=True),
                TsType(name="test", is_optional=False),
            ),
            (
                TsInterface(name="test1", is_optional=False),
                TsInterface(name="test2", is_optional=False),
            ),
            (
                TsInterface(name="test", is_optional=True),
                TsInterface(name="test", is_optional=False),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=False),
                TsArray(wrapped_type=TS_NUMBER, is_optional=False),
            ),
            (
                TsArray(wrapped_type=TS_STRING, is_optional=False),
                TsArray(wrapped_type=TS_STRING, is_optional=True),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
                TsMappedType(wrapped_type=TS_NUMBER, is_optional=False),
            ),
            (
                TsMappedType(wrapped_type=TS_STRING, is_optional=False),
                TsMappedType(wrapped_type=TS_STRING, is_optional=True),
            ),
        ],
    )
    def test_ts_types_with_not_equal_name_should_have_same_hash(
        self, ts_type1, ts_type2
    ):
        assert ts_type1 != ts_type2
        assert hash(ts_type1) != hash(ts_type2)
        assert len({ts_type1, ts_type1}) == 1


@pytest.mark.parametrize(
    "ts_type,the_str",
    [
        (TsType("TheType"), "TheType"),
        (TsArray(wrapped_type=TsType("TheType")), "TheType[]"),
        (TsInterface("TheType"), "TheType"),
        (TsMappedType(TsType("TheType")), "{[index: string]: TheType}"),
        (TsType("TheType", is_optional=True), "(TheType | undefined)"),
        (
            TsArray(wrapped_type=TsType("TheType"), is_optional=True),
            "(TheType[] | undefined)",
        ),
        (TsInterface("TheType", is_optional=True), "(TheType | undefined)"),
        (
            TsMappedType(TsType("TheType"), is_optional=True),
            "({[index: string]: TheType} | undefined)",
        ),
    ],
)
def test_format_as_type_reference(ts_type: TsType, the_str: str) -> None:
    assert ts_type.format_as_type_reference() == the_str
