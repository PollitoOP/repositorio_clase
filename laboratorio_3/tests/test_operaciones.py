import math

import pytest

from src.operaciones import division, suma


def test_suma_basica() -> None:
    assert suma(2, 3) == 5.0


def test_division_basica() -> None:
    assert division(10.0, 2.0) == 5.0


def test_division_por_cero() -> None:
    with pytest.raises(ZeroDivisionError):
        division(1.0, 0.0)


def test_suma_float_int_mix() -> None:
    res = suma(2, 2.5)
    assert math.isclose(res, 4.5)
