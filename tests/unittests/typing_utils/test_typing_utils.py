from typing import Optional

from py_typescript_generator.typing_utils.typing_utils import (
    get_wrapped_type_from_optional,
)


def test_get_wrapped_type_from_optional():
    assert get_wrapped_type_from_optional(Optional[int]) == int
