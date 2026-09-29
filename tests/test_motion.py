from __future__ import annotations

import pytest
from manim import Square, rate_functions

from kit import motion


def test_looped_rate_returns_to_start_every_cycle():
    wave = motion.looped(rate_functions.there_and_back, 3)
    assert wave(0) == pytest.approx(0)
    assert wave(1) == pytest.approx(0)
    assert wave(1 / 6) == pytest.approx(1)


def test_colour_cycle_ends_on_the_original_colour():
    sq = Square(stroke_color="#58A6FF", fill_color="#58A6FF", fill_opacity=0.5)
    anim = motion.ColorCycle(sq, ["#58A6FF", "#FF7EE3", "#7EE787"], cycles=2)
    anim.begin()
    anim.interpolate(0.4)
    assert sq.get_fill_color().to_hex().upper() != "#58A6FF"
    anim.interpolate(1.0)
    assert sq.get_fill_color().to_hex().upper() == "#58A6FF"


def test_colour_cycle_must_start_from_the_current_colour():
    sq = Square(fill_color="#FFFFFF", fill_opacity=0.5)
    with pytest.raises(ValueError, match="start"):
        motion.ColorCycle(sq, ["#58A6FF", "#FF7EE3"])
