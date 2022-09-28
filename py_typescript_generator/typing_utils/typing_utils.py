from typing import Type, Optional, TypeVar

from typing_inspect import get_args  # type: ignore

T = TypeVar("T")


def get_wrapped_type_from_optional(cls: Type) -> Type:
    args = get_args(cls)
    return args[0]  # type: ignore


def safe_unwrap(optional: Optional[T]) -> T:
    if optional is None:
        raise ValueError("Tried to unwrap an optional, but it was None.")
    return optional
