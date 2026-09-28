from __future__ import annotations

from pathlib import Path

import pytest

import render


def test_class_names():
    assert render.class_name("I.4") == "B_I_4"
    assert render.class_name("2.3") == "B_2_3"


def test_beats_in_part_follow_script_order():
    assert render.beats_in_part("intro") == [f"I.{i}" for i in range(1, 10)]
    assert render.beats_in_part("1") == ["1.1", "1.2", "1.3", "1.4"]


def test_unknown_part_is_rejected():
    with pytest.raises(ValueError, match="unknown part"):
        render.beats_in_part("99")


def test_manim_command_and_output_path():
    cmd = render.manim_command("beats/part2.py", "B_2_3", "preview")
    assert cmd[-2:] == ["beats/part2.py", "B_2_3"] and "-ql" in cmd
    assert render.output_path("beats/part2.py", "B_2_3", "preview").as_posix().endswith(
        "renders/media/videos/part2/480p15/B_2_3.mp4"
    )
    assert "1080p60" in render.output_path("beats/part2.py", "B_2_3", "final").as_posix()


def test_concat_list_escapes_quotes():
    text = render.concat_list_text([Path("a/b's.mp4")])
    assert text.strip() == "file '" + Path("a/b's.mp4").resolve().as_posix().replace("'", "'\\''") + "'"
