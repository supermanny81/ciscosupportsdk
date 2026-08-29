import pytest

from ciscosupportsdk.validate import (
    CheckSize,
    CheckSizeOperation,
    check_date_range,
)


class TestValidate(object):
    # test harness
    def check_operation(
        self, size: int, values: list, operation: CheckSizeOperation
    ):
        @CheckSize("field", size, operation)
        def f(field: list):
            pass

        f(field=values)

    def test_check_less_than(self):
        # LESS_THAN followed by LESS_THAN_OR_EQUALS
        self.check_operation(3, [1, 2], CheckSizeOperation.LESS_THAN)
        self.check_operation(2, [1, 2], CheckSizeOperation.LESS_THAN_OR_EQUALS)

    def test_check_LESS_THAN_negative(self):
        # make sure we throw a ValueError
        with pytest.raises(ValueError):
            self.check_operation(1, [1, 2], CheckSizeOperation.LESS_THAN)
        with pytest.raises(ValueError):
            self.check_operation(
                1, [1, 2], CheckSizeOperation.LESS_THAN_OR_EQUALS
            )

    def test_check_greater_than(self):
        self.check_operation(0, [1, 2], CheckSizeOperation.GREATER_THAN)
        self.check_operation(
            2, [1, 2], CheckSizeOperation.GREATER_THAN_OR_EQUALS
        )

    def test_check_greater_than_negative(self):
        # make sure we throw a ValueError
        with pytest.raises(ValueError):
            self.check_operation(3, [1, 2], CheckSizeOperation.GREATER_THAN)
        with pytest.raises(ValueError):
            self.check_operation(
                3, [1, 2], CheckSizeOperation.GREATER_THAN_OR_EQUALS
            )

    def test_field_not_passes(self):
        with pytest.raises(AttributeError):

            @CheckSize("DOES NOT EXIST", 0)
            def f():
                pass

            f()

    def test_call_without_keywords(self):
        @CheckSize("field", 10, CheckSizeOperation.LESS_THAN)
        def f(sample_field: str, field: list):
            pass

        f("test", [1, 2, 3])

    def test_call_without_keywords_negative(self):
        with pytest.raises(AttributeError):

            @CheckSize("field", 10, CheckSizeOperation.LESS_THAN)
            def f(field: list):
                pass

            f()


class TestCheckDateRange(object):
    def test_accepts_a_range_within_the_limit(self):
        check_date_range("2024-01-01", "2024-01-20", 30)

    def test_skips_when_either_bound_is_missing(self):
        check_date_range(None, "2024-01-20", 30)
        check_date_range("2024-01-01", None, 30)

    def test_rejects_a_range_wider_than_the_limit(self):
        with pytest.raises(ValueError, match="exceeds the maximum"):
            check_date_range("2024-01-01", "2024-03-01", 30)

    def test_rejects_an_inverted_range(self):
        with pytest.raises(ValueError, match="precedes start date"):
            check_date_range("2024-02-01", "2024-01-01", 30)

    def test_rejects_a_malformed_date(self):
        with pytest.raises(ValueError, match="must be formatted"):
            check_date_range("01/01/2024", "20/01/2024", 30)

    def test_honours_an_alternate_format(self):
        check_date_range(
            "2024-01-01T00:00:00Z",
            "2024-03-01T00:00:00Z",
            90,
            "%Y-%m-%dT%H:%M:%SZ",
        )
