from __future__ import annotations

import pytest
from manim import Rectangle

from kit import zones

EPS = 1e-6


def box(w, h):
    return Rectangle(width=w, height=h)


def inside(m, z):
    return (
        m.get_left()[0] >= z.left - EPS and m.get_right()[0] <= z.right + EPS
        and m.get_bottom()[1] >= z.bottom - EPS and m.get_top()[1] <= z.top + EPS
    )


@pytest.mark.parametrize("name", sorted(zones.ZONES))
def test_fit_puts_large_things_inside(name):
    m = zones.fit(box(40, 30), name)
    assert inside(m, zones.ZONES[name])


def test_fit_never_scales_up():
    m = zones.fit(box(0.5, 0.25), "WORK")
    assert m.width == pytest.approx(0.5)


@pytest.mark.parametrize("align", ["left", "right", "top", "bottom", "top_left"])
def test_alignments_touch_the_edge(align):
    z = zones.ZONES["SIDE"]
    m = zones.fit(box(1, 1), "SIDE", align=align)
    if "left" in align:
        assert m.get_left()[0] == pytest.approx(z.left)
    if align == "right":
        assert m.get_right()[0] == pytest.approx(z.right)
    if "top" in align:
        assert m.get_top()[1] == pytest.approx(z.top)
    if align == "bottom":
        assert m.get_bottom()[1] == pytest.approx(z.bottom)


def test_unknown_align_is_rejected():
    with pytest.raises(ValueError, match="align"):
        zones.fit(box(1, 1), "WORK", align="diagonal")


def test_kept_slots_are_disjoint_and_inside_kept():
    slots = [zones.kept_slot(i) for i in range(zones.KEPT_SLOTS)]
    for a, b in zip(slots, slots[1:]):
        assert a.right <= b.left + EPS
    k = zones.ZONES["KEPT"]
    assert slots[0].left >= k.left - EPS and slots[-1].right <= k.right + EPS


def test_to_kept_fits_the_slot_and_rejects_bad_slots():
    m = zones.to_kept(box(6, 2), 1)
    assert inside(m, zones.kept_slot(1))
    with pytest.raises(ValueError, match="slot"):
        zones.to_kept(box(1, 1), zones.KEPT_SLOTS)


def test_main_zones_do_not_overlap():
    names = ["HEADLINE", "WORK", "RULE", "NOTES", "KEPT"]
    zs = [zones.ZONES[n] for n in names]
    for i, a in enumerate(zs):
        for b in zs[i + 1:]:
            overlap_x = min(a.right, b.right) - max(a.left, b.left)
            overlap_y = min(a.top, b.top) - max(a.bottom, b.bottom)
            assert overlap_x <= EPS or overlap_y <= EPS
