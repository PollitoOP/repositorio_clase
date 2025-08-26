# src/main.py
from __future__ import annotations

from src.operaciones import division, suma


def main() -> None:
    print("3 + 5 =", suma(3, 5))
    print("10 / 2 =", division(10, 2))
    try:
        print("10 / 0 =", division(10, 0))
    except ZeroDivisionError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
