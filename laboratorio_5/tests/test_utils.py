import math
import pytest
from utils import normalize_text, is_palindrome, moving_average

# --- normalize_text ---
def test_normalize_text_basic():
    assert normalize_text("  Hola   Mundo  ") == "hola mundo"

def test_normalize_text_empty():
    assert normalize_text("   ") == ""

def test_normalize_text_type_error():
    with pytest.raises(TypeError):
        normalize_text(123)  # type: ignore

# --- is_palindrome ---
@pytest.mark.parametrize("txt,expected", [
    ("Reconocer", True),
    ("Anita lava la tina", True),
    ("No es palindromo", False),
    ("", True),  # cadena vacía se considera palíndromo por definición
])
def test_is_palindrome(txt, expected):
    assert is_palindrome(txt) is expected

def test_is_palindrome_type_error():
    with pytest.raises(TypeError):
        is_palindrome(None)  # type: ignore

# --- moving_average ---
def test_moving_average_basic():
    assert moving_average([1,2,3,4,5], 3) == [2.0, 3.0, 4.0]

def test_moving_average_window_one():
    assert moving_average([10, 20], 1) == [10.0, 20.0]

def test_moving_average_errors():
    with pytest.raises(ValueError):
        moving_average([1,2], 0)
    with pytest.raises(ValueError):
        moving_average([1,2], 3)
    with pytest.raises(TypeError):
        moving_average([1, "x"], 2)  # type: ignore
    with pytest.raises(TypeError):
        moving_average([1,2], 2.5)  # type: ignore
