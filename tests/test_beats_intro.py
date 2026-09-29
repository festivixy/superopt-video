from __future__ import annotations

from pathlib import Path

import pytest

import timing
from beats import all_beats
from kit.beat import fingerprint, replay
from tests.conftest import render_dry
from tools.script_timing import parse

PREFIX = "I"
SCRIPT_BEATS = [b.id for b in parse(Path("script/script.md").read_text(encoding="utf-8"))
                if b.id.split(".")[0] == PREFIX]


def test_every_script_beat_has_a_scene_and_board_slot():
    from boards.intro import BOARD

    assert list(BOARD.beats) == SCRIPT_BEATS
    registered = [b for b in all_beats() if b.split(".")[0] == PREFIX]
    assert sorted(registered) == sorted(SCRIPT_BEATS)


@pytest.mark.parametrize("beat_id", SCRIPT_BEATS)
def test_beat_ends_on_its_board_and_on_time(beat_id):
    cls = all_beats()[beat_id]
    scene = render_dry(cls)
    expected = replay(cls.board.records_through(beat_id))
    assert {k: fingerprint(m) for k, m in scene.items.items()} == {k: fingerprint(m) for k, m in expected.items()}
    assert scene.elapsed == pytest.approx(timing.TIMING[beat_id], abs=0.5)
