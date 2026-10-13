import pytest
from services import calculate_result


def test_add_service():
    result = calculate_result(10, 5, "add")

    assert result == 15


def test_subtract_service():
    result = calculate_result(10, 5, "subtract")

    assert result == 5


def test_divide_service():
    result = calculate_result(10, 5, "divide")

    assert result == 2


def test_divide_by_zero_service():
    with pytest.raises(ValueError):
        calculate_result(10, 0, "divide")