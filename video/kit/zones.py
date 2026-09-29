from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Mobject


@dataclass(frozen=True)
class Zone:
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> np.ndarray:
        return np.array([self.x, self.y, 0.0])

    @property
    def left(self) -> float:
        return self.x - self.width / 2

    @property
    def right(self) -> float:
        return self.x + self.width / 2

    @property
    def top(self) -> float:
        return self.y + self.height / 2

    @property
    def bottom(self) -> float:
        return self.y - self.height / 2


ZONES: dict[str, Zone] = {
    "HEADLINE": Zone(-2.5, 3.55, 8.6, 0.7),
    "WORK": Zone(-2.5, 0.2, 8.6, 5.6),
    "RULE": Zone(4.55, 2.05, 4.5, 3.0),
    "NOTES": Zone(4.55, -1.6, 4.5, 3.9),
    "KEPT": Zone(-2.5, -3.35, 8.6, 0.8),
    "ART": Zone(-4.0, 0.0, 5.4, 5.8),
    "SIDE": Zone(2.9, 0.3, 7.4, 5.6),
    "STRIP": Zone(0.0, -3.5, 13.6, 0.9),
    "CENTER": Zone(0.0, 0.0, 12.0, 6.5),
    "HALF_L": Zone(-3.5, 0.0, 6.4, 6.2),
    "HALF_R": Zone(3.5, 0.0, 6.4, 6.2),
    "RIGHT": Zone(4.55, 0.0, 4.5, 7.2),
}

ALIGNS = ("center", "left", "right", "top", "bottom", "top_left")
KEPT_SLOTS = 3


def _fit_into(m: Mobject, z: Zone, align: str) -> Mobject:
    if align not in ALIGNS:
        raise ValueError(f"unknown align {align!r}; expected one of {ALIGNS}")
    factors = [1.0]
    if m.width > 0:
        factors.append(z.width / m.width)
    if m.height > 0:
        factors.append(z.height / m.height)
    scale = min(factors)
    if scale < 1.0:
        m.scale(scale)
    m.move_to(z.center)
    if "left" in align:
        m.align_to(np.array([z.left, 0.0, 0.0]), LEFT)
    if align == "right":
        m.align_to(np.array([z.right, 0.0, 0.0]), RIGHT)
    if "top" in align:
        m.align_to(np.array([0.0, z.top, 0.0]), UP)
    if align == "bottom":
        m.align_to(np.array([0.0, z.bottom, 0.0]), DOWN)
    return m


def fit(m: Mobject, zone: str, align: str = "center") -> Mobject:
    return _fit_into(m, ZONES[zone], align)


def kept_slot(i: int) -> Zone:
    if not 0 <= i < KEPT_SLOTS:
        raise ValueError(f"kept slot {i} out of range 0..{KEPT_SLOTS - 1}")
    k = ZONES["KEPT"]
    w = k.width / KEPT_SLOTS
    return Zone(k.left + w * (i + 0.5), k.y, w - 0.2, k.height)


def to_kept(m: Mobject, slot: int) -> Mobject:
    return _fit_into(m, kept_slot(slot), "center")
