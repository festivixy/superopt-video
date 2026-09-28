from __future__ import annotations

import pytest

from kit import board, style, zones


def glyphs(row):
    return "".join(t.text for t in row.digits)


def test_char_row_keeps_columns_for_spaces():
    row = board.char_row("01 1")
    assert sorted(row.columns) == [0, 1, 3]
    gap = row.columns[3].get_x() - row.columns[1].get_x()
    step = row.columns[1].get_x() - row.columns[0].get_x()
    assert gap == pytest.approx(2 * step, rel=1e-3)


def test_register_shows_108_msb_first_and_colors_ones():
    reg = board.register(108, 8, place_values=True)
    assert glyphs(reg) == "01101100"
    assert [p.text for p in reg.places] == ["128", "64", "32", "16", "8", "4", "2", "1"]
    assert reg.bit(2)[1].text == "1"
    assert reg.bit(2)[1][0].get_fill_color().to_hex().upper() == style.BLUE.upper()  # glyph fill; Text container reports #000000 in Manim 0.21
    assert reg.bit(0)[1].text == "0"


def test_register_rejects_values_that_do_not_fit():
    with pytest.raises(ValueError, match="does not fit"):
        board.register(256, 8)


def test_column_op_right_aligns_rows_and_counts_digits_from_the_right():
    op = board.column_op([("x", "0110 1100"), ("− 1", "1"), ("", "0110 1011")])
    assert op.digit(1, 0).get_x() == pytest.approx(op.digit(0, 0).get_x())
    assert op.digit(0, 2).text == "1"
    assert op.digit(2, 2).text == "0"
    assert op.rule.get_y() > op.rows[2].get_y()


def test_borrow_marks_one_per_k():
    op = board.column_op([("", "1000"), ("− 1", "1"), ("", "0999")])
    marks = board.borrow_marks(op, 0, (2, 1, 0))
    assert len(marks) == 3


def test_truth_table_and():
    lines = board.truth_table("&")
    assert ["".join(t.text for t in l.digits) for l in lines] == ["1&1=1", "1&0=0", "0&1=0", "0&0=0"]


def test_program_card_keeps_indentation():
    card = board.program_card(["for i:", "  body"])
    assert card.lines[1].get_left()[0] > card.lines[0].get_left()[0]


def test_code_card_one_entry_per_source_line():
    src = "a\n\n  b"
    card = board.code_card(src)
    assert len(card.lines) == 3
    assert card.lines[2].get_left()[0] > card.lines[0].get_left()[0]


def test_asm_wall_keeps_order_across_columns():
    lines = [f"l{i}" for i in range(10)]
    wall = board.asm_wall(lines, columns=2)
    assert [m.text for m in wall.lines] == lines
    assert wall.lines[5].get_x() > wall.lines[4].get_x()


def test_count_bars_are_proportional():
    bars = board.count_bars([("a", 98, style.ORANGE), ("b", 2, style.GREEN)], width=6.0)
    assert bars.bars[0].width == pytest.approx(6.0)
    assert bars.bars[1].width == pytest.approx(max(0.06, 6.0 * 2 / 98))


def test_timeline_one_tick_per_entry_left_to_right():
    t = board.timeline([("May 29", "start"), ("Aug 12", "done")])
    assert len(t.ticks) == 2
    assert t.ticks[0].get_x() < t.ticks[1].get_x()


def test_headline_sits_in_its_zone():
    h = board.headline("numbers are rows of switches")
    z = zones.ZONES["HEADLINE"]
    assert h.get_left()[0] == pytest.approx(z.left)
    assert z.bottom - 1e-6 <= h.get_bottom()[1] and h.get_top()[1] <= z.top + 1e-6
