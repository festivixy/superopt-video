from __future__ import annotations

import numpy as np
import pytest

from kit import stage
from kit.style import BG


def test_poses_share_one_skeleton_so_they_morph():
    shapes = {name: [len(part.points) for part in stage.stick(name)] for name in stage.POSES}
    assert len(set(map(tuple, shapes.values()))) == 1


def _hand(figure):
    return figure[2].points[-1][:2]


def test_the_jump_puts_his_hand_on_the_bead():
    r = stage.room(lit=False)
    guy = stage.stick("reach", stage.GUY_X, lift=stage.JUMP)
    assert np.allclose(_hand(guy), r.bead.get_center()[:2], atol=1e-6)


def test_the_pull_drags_the_bead_down_with_his_hand():
    r = stage.room(lit=False)
    lamp = stage.pulled(r)
    guy = stage.stick("pull", stage.GUY_X)
    assert np.allclose(_hand(guy), lamp[3].get_center()[:2], atol=1e-6)


def test_zooming_in_makes_the_screen_the_whole_frame():
    screen = stage.zoomed(stage.room(lit=True).screen)
    assert screen.get_center() == pytest.approx([0, 0, 0], abs=1e-6)
    assert screen.width == pytest.approx(14.2222, abs=1e-3)
    assert screen.height == pytest.approx(8.0, abs=1e-2)


def test_the_screen_turns_on_with_the_light_unless_told_otherwise():
    assert stage.room(lit=True).screen.get_fill_color().to_hex().upper() == BG.upper()
    assert stage.room(lit=False).screen.get_fill_color().to_hex().upper() == stage.OFF_SCREEN.upper()
    assert stage.room(lit=True, screen_on=False).screen.get_fill_color().to_hex().upper() == stage.OFF_SCREEN.upper()
