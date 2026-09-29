from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"

EXAMPLE = 108
EXAMPLE_MINUS_ONE = 107
EXAMPLE_AND = 104
CLANG_CLEAR_LOWEST_BIT = 98
TRICK_INSTRUCTIONS = 2

OPS = ("add", "sub", "mul", "and", "or", "xor", "not", "neg", "shl", "lshr", "ashr")

TIMELINE = (
    ("May 29", "start"),
    ("Jun 9", "first search"),
    ("Jun 17", "synthesis"),
    ("Jul 28", "bug fixed"),
    ("Jul 29", "compiler survey"),
    ("Aug 12", "done"),
)

C_SOURCE = (ASSETS / "code" / "clear_lowest_bit.c").read_text(encoding="utf-8").strip("\n")


def _asm_body(path: Path) -> tuple[str, ...]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    start = lines.index("clear_lowest_bit:")
    return tuple(line for line in lines[start:] if line and not line.startswith("#"))


CLANG_ASM_LINES = _asm_body(ASSETS / "code" / "clang_clear_lowest_bit.s")


def count_instructions(lines: Iterable[str]) -> int:
    count = 0
    for line in lines:
        if line.endswith(":") or line.startswith("."):
            continue
        if line.split()[0] == "ret":
            continue
        count += 1
    return count
