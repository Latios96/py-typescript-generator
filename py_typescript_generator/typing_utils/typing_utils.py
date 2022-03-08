from typing import Type

from typing_inspect import get_args  # type: ignore


def get_wrapped_type_from_optional(cls: Type) -> Type:
    args = get_args(cls)
    return args[0]  # type: ignore
