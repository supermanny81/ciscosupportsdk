from enum import Enum
from functools import wraps
from inspect import signature
from typing import Callable


class CheckSizeOperation(Enum):
    LESS_THAN = 1
    LESS_THAN_OR_EQUALS = 2
    GREATER_THAN = 3
    GREATER_THAN_OR_EQUALS = 4


class CheckSize(object):
    """Validates a parameter passed is meets expectations on size."""

    def __init__(
        self,
        field: str,
        size: int,
        operation: CheckSizeOperation = CheckSizeOperation.LESS_THAN_OR_EQUALS,
    ):
        self.field: str = field
        self.size: int = size
        self.operation: CheckSizeOperation = operation

    """
    :params: original_func
    """

    def __call__(self, original_func: Callable):
        # needs to behave when called, return docstring, etc
        @wraps(original_func)
        def wrappee(*args, **kwargs):
            _list: list = kwargs.get(self.field, None)

            if _list is None and len(args) > 0:
                pos = 0
                sig = signature(original_func)
                for name, _ in sig.parameters.items():
                    if name == self.field:
                        if type(args[pos]) == list:
                            _list = args[pos]
                            break
                    pos += 1

            if _list is None:
                raise AttributeError(f"Missing field {self.field}")

            if self.operation == CheckSizeOperation.GREATER_THAN:
                if not len(_list) > self.size:
                    raise ValueError(
                        f"Too many {self.field} passed ({len(_list)})"
                        f", max allowable size {self.size}."
                    )
            elif self.operation == CheckSizeOperation.GREATER_THAN_OR_EQUALS:
                if not len(_list) >= self.size:
                    raise ValueError(
                        f"Too many {self.field} passed ({len(_list)})"
                        f", max allowable size {self.size - 1}."
                    )
            elif self.operation == CheckSizeOperation.LESS_THAN:
                if not len(_list) < self.size:
                    raise ValueError(
                        f"Too few {self.field} passed ({len(_list)})"
                        f", min allowable size {self.size}."
                    )
            elif self.operation == CheckSizeOperation.LESS_THAN_OR_EQUALS:
                if not len(_list) <= self.size:
                    raise ValueError(
                        f"Too few {self.field} passed ({len(_list)})"
                        f", min allowable size {self.size + 1}."
                    )
            return original_func(*args, **kwargs)

        return wrappee
