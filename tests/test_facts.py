from __future__ import annotations

from pathlib import Path

import pytest

import facts


def test_example_arithmetic():
    assert facts.EXAMPLE == 64 + 32 + 8 + 4 == 0b01101100
    assert facts.EXAMPLE_MINUS_ONE == facts.EXAMPLE - 1 == 0b01101011
    assert facts.EXAMPLE_AND == facts.EXAMPLE & (facts.EXAMPLE - 1) == 0b01101000


def test_clang_count_follows_the_counting_rule():
    assert facts.count_instructions(facts.CLANG_ASM_LINES) == facts.CLANG_CLEAR_LOWEST_BIT == 98
    assert 32 * 3 + 2 == facts.CLANG_CLEAR_LOWEST_BIT


def test_asm_lines_start_at_the_function_label():
    assert facts.CLANG_ASM_LINES[0] == "clear_lowest_bit:"
    assert facts.CLANG_ASM_LINES[1:4] == ("mov     eax, 1", "test    dil, 1", "jne     .LBB0_33")


def test_c_source_is_the_naive_loop():
    assert "for (int i = 0; i < 32; i++)" in facts.C_SOURCE
    assert "return x ^ (1u << i);" in facts.C_SOURCE


def test_eleven_ops():
    assert facts.OPS == ("add", "sub", "mul", "and", "or", "xor", "not", "neg", "shl", "lshr", "ashr")


def test_ops_match_superopt_ir_when_checked_out():
    ir = Path("../superopt/ir.py")
    if not ir.exists():
        pytest.skip("superopt checkout not next to superopt-video")
    text = ir.read_text(encoding="utf-8")
    for name in facts.OPS:
        assert f'= "{name}"' in text


def test_timeline_is_in_order():
    assert [d for d, _ in facts.TIMELINE] == ["May 29", "Jun 9", "Jun 17", "Jul 28", "Jul 29", "Aug 12"]
