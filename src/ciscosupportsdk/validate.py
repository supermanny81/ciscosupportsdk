from datetime import datetime
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
                        if isinstance(args[pos], list):
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


def check_date_range(
    from_date: str,
    to_date: str,
    max_days: int,
    date_format: str = "%Y-%m-%d",
) -> None:
    """Validates that a from/to date pair spans no more than ``max_days``.

    Several Cisco Support APIs cap how wide a date range may be (30 days for
    RMAs, 90 days for cases). Validating locally turns a server-side error
    into a clear, immediate one.

    :param: from_date: str: start of the range, ``None`` skips the check
    :param: to_date: str: end of the range, ``None`` skips the check
    :param: max_days: int: widest permitted range, in days
    :param: date_format: str: strptime format the API expects
    """
    if from_date is None or to_date is None:
        return

    try:
        start = datetime.strptime(from_date, date_format)
        end = datetime.strptime(to_date, date_format)
    except ValueError as exc:
        raise ValueError(
            f"Dates must be formatted as {date_format}: {exc}"
        ) from exc

    if end < start:
        raise ValueError(
            f"End date ({to_date}) precedes start date ({from_date})."
        )

    span = (end - start).days
    if span > max_days:
        raise ValueError(
            f"Date range of {span} days exceeds the maximum "
            f"supported range of {max_days} days."
        )
