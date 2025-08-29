from __future__ import annotations
import re
from typing import Iterable, List

def normalize_text(s: str) -> str:
    """Normalize whitespace and case.
    - Lowercase
    - Strip leading/trailing whitespace
    - Collapse internal whitespace to a single space
    Raises:
        TypeError: if s is not a str
    """
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    s = s.strip().lower()
    # Replace any run of whitespace with a single space
    return re.sub(r"\s+", " ", s)

def is_palindrome(s: str) -> bool:
    """Return True if *s* is a palindrome ignoring case, spaces and punctuation."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    cleaned = re.sub(r"[^a-z0-9]", "", s.lower())
    return cleaned == cleaned[::-1]

def moving_average(values: Iterable[float], window: int) -> List[float]:
    """Compute simple moving average over *values* with window size *window*.
    Args:
        values: iterable of ints/floats
        window: positive int, must be <= len(values)
    Returns:
        list of floats of length len(values) - window + 1
    Raises:
        ValueError: if window < 1 or window > len(values)
        TypeError: if any value is not int/float
    """
    vals = list(values)
    if not isinstance(window, int):
        raise TypeError("window must be int")
    if window < 1:
        raise ValueError("window must be >= 1")
    if window > len(vals):
        raise ValueError("window cannot exceed length of values")
    # Type check
    for v in vals:
        if not isinstance(v, (int, float)):
            raise TypeError("all values must be numeric")
    out = []
    cumsum = 0.0
    for i, v in enumerate(vals):
        cumsum += v
        if i >= window:
            cumsum -= vals[i - window]
        if i >= window - 1:
            out.append(cumsum / window)
    return out
