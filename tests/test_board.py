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
    assert reg.bit(2)[1][0].get_fill_color().to_hex().upper() == style.BLUE.upper()
    assert reg.bit(0)[1].text == "0"


def test_register_rejects_values_that_do_not_fit():
    with pytest.raises(ValueError, match="does not fit"):
        board.register(256, 8)


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


def test_headline_sits_in_its_zone():
    h = board.headline("numbers are rows of switches")
    z = zones.ZONES["HEADLINE"]
    assert h.get_left()[0] == pytest.approx(z.left)
    assert z.bottom - 1e-6 <= h.get_bottom()[1] and h.get_top()[1] <= z.top + 1e-6


def test_asm_wall_can_colour_parts_of_lines():
    wall = board.asm_wall(["mov eax, 8", "test dil, 8"], columns=1,
                          t2c_for=lambda line: {line.split(", ")[1]: style.ORANGE} if line.startswith("mov") else {})
    first, second = wall.lines
    assert first[-1].get_fill_color().to_hex().upper() == style.ORANGE.upper()
    assert second[-1].get_fill_color().to_hex().upper() != style.ORANGE.upper()
