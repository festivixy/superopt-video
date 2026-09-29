from __future__ import annotations

import pytest
from manim import MarkupText, Text

from kit import pics


def test_switch_row_shows_the_value_lsb_on_the_right():
    row = pics.switch_row(108)
    assert [row.bit(i).on for i in range(8)] == [False, False, True, True, False, True, True, False]
    assert row.bit(0).get_x() > row.bit(7).get_x()


def test_switch_row_place_values_double_right_to_left():
    row = pics.switch_row(108, place_values=True)
    assert [p.original_text for p in row.places] == ["128", "64", "32", "16", "8", "4", "2", "1"]


def test_flipped_switch_sits_where_the_old_one_was():
    row = pics.switch_row(108)
    new = pics.flipped(row.bit(2))
    assert new.on is False and row.bit(2).on is True
    assert abs(new.get_x() - row.bit(2).get_x()) < 1e-9


def test_switch_row_rejects_values_that_do_not_fit():
    with pytest.raises(ValueError, match="fit"):
        pics.switch_row(256)


def test_tile_carries_its_instruction_name():
    t = pics.tile("sub")
    assert t.label.original_text == "sub"


@pytest.mark.parametrize("build", [
    pics.press_machine, pics.pointer, pics.marble, pics.magnifier, pics.loop_icon, pics.bug,
    pics.bars_icon, pics.check, pics.flag, pics.book_open, lambda: pics.dot_grid(8, 16),
    lambda: pics.bit_strip([1, 0, 1]), pics.mini_game,
], ids=lambda b: getattr(b, "__name__", "lambda"))
def test_pictures_build_without_sentences(build):
    m = build()
    assert m.width > 0 and m.height > 0
    words = [t for t in m.get_family() if isinstance(t, (Text, MarkupText)) and len(t.original_text.split()) > 2]
    assert not words


def test_bit_strip_marks_ones():
    s = pics.bit_strip([1, 0, 1, 1])
    assert [c.on for c in s.cells] == [True, False, True, True]


def test_program_machine_has_stations_and_a_cover():
    m = pics.program_machine(3, face="x + x")
    assert len(m.stations) == 3
    assert m.cover.get_fill_opacity() == 1
    assert m.face is not None


@pytest.mark.parametrize("build", [
    pics.and_gate, pics.lamp, pics.x_mark, pics.paper, lambda: pics.stamp("UNSAT"),
    lambda: pics.domino(3), lambda: pics.tree(3), lambda: pics.program_machine(2),
], ids=lambda b: getattr(b, "__name__", "lambda"))
def test_new_pictures_build_without_sentences(build):
    m = build()
    assert m.width > 0 and m.height > 0
    words = [t for t in m.get_family() if isinstance(t, (Text, MarkupText)) and len(t.original_text.split()) > 2]
    assert not words


def test_tree_has_a_node_per_position():
    t = pics.tree(3)
    assert len(t.nodes) == 1 + 2 + 4 + 8
    assert len(t.leaves) == 8


def test_domino_holds_pairs():
    d = pics.domino(3)
    assert len(d.dots) == 6


def test_screenshot_frames_a_real_page_in_a_browser_window():
    from manim import ImageMobject

    shot = pics.screenshot("llvm_issue.png", "github.com/llvm/llvm-project/issues/212908", width=8.0)
    assert isinstance(shot.image, ImageMobject)
    assert abs(shot.width - 8.0) < 0.05
    assert shot.image.get_top()[1] < shot.bar.get_bottom()[1] + 0.01
    assert shot.url.original_text.startswith("github.com")


def test_screenshot_rejects_a_missing_file():
    with pytest.raises(FileNotFoundError):
        pics.screenshot("no_such_page.png", "example.com")
