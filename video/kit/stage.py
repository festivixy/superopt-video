from __future__ import annotations

import numpy as np
from manim import Circle, Dot, Line, Rectangle, RoundedRectangle, Transform, VGroup, rate_functions

from kit import motion, pics, style
from kit.cartoon import BOLD, MID, THIN_PROP, _poly
from kit.style import BG, BLUE, DIM, GREEN, INK

FLOOR_Y = -3.0
SCREEN_CENTER = np.array([0.0, 0.8, 0.0])
SCREEN_W, SCREEN_H = 4.16, 2.34
ZOOM = 14.2222 / SCREEN_W
OFF_SCREEN = "#030405"
CHAIN_X = 4.85
BEAD_TOP = 0.15
PULL = 0.8


def room(lit: bool, screen_on: bool | None = None) -> VGroup:
    screen_on = lit if screen_on is None else screen_on
    ink = INK if lit else DIM
    floor = Line([-7.4, FLOOR_Y, 0], [7.4, FLOOR_Y, 0]).set_stroke(DIM, THIN_PROP)
    top = _poly((-3.2, -1.1), (3.2, -1.1), color=ink, width=MID)
    legs = VGroup(_poly((-2.9, -1.1), (-2.9, FLOOR_Y), color=ink, width=MID),
                  _poly((2.9, -1.1), (2.9, FLOOR_Y), color=ink, width=MID))
    desk = VGroup(top, legs)
    bezel = RoundedRectangle(corner_radius=0.15, width=SCREEN_W + 0.34, height=SCREEN_H + 0.4).move_to(SCREEN_CENTER + [0, -0.03, 0])
    bezel.set_stroke(ink, MID).set_fill(opacity=0)
    screen = Rectangle(width=SCREEN_W, height=SCREEN_H).move_to(SCREEN_CENTER).set_stroke(ink, THIN_PROP)
    screen.set_fill(BG if screen_on else OFF_SCREEN, 1)
    cursor = Rectangle(width=0.14, height=0.26).set_stroke(width=0).set_fill(BLUE, 1 if screen_on else 0)
    cursor.move_to(screen.get_corner([-1, 1, 0]) + np.array([0.35, -0.35, 0]))
    power = Dot(radius=0.05, color=GREEN if screen_on else DIM).move_to(bezel.get_bottom() + np.array([1.9, 0.1, 0]))
    stand = VGroup(_poly((0, bezel.get_bottom()[1]), (0, -0.98), color=ink, width=MID),
                   _poly((-0.6, -1.02), (0.6, -1.02), color=ink, width=MID))
    keyboard = RoundedRectangle(corner_radius=0.05, width=1.7, height=0.14).move_to([-1.9, -0.99, 0])
    keyboard.set_stroke(ink, THIN_PROP).set_fill(opacity=0)
    monitor = VGroup(bezel, screen, cursor, power, stand)
    cord = Line([4.6, 4.2, 0], [4.6, 2.85, 0]).set_stroke(ink, THIN_PROP)
    bulb = pics.lamp(on=lit, size=1.0).rotate(np.pi)
    bulb.next_to(cord.get_end(), [0, -1, 0], buff=0)
    if not lit:
        bulb.bulb.set_stroke(DIM)
        for line in bulb[2]:
            line.set_stroke(DIM)
    chain = Line([CHAIN_X, 2.6, 0], [CHAIN_X, BEAD_TOP, 0]).set_stroke(ink, THIN_PROP)
    bead = Dot(radius=0.08, color=ink).move_to([CHAIN_X, BEAD_TOP, 0])
    lamp = VGroup(cord, bulb, chain, bead)
    r = VGroup(floor, desk, keyboard, monitor, lamp)
    r.screen, r.cursor, r.monitor, r.lamp, r.chain, r.bead = screen, cursor, monitor, lamp, chain, bead
    return r


def pulled(r: VGroup) -> VGroup:
    lamp = r.lamp.copy()
    lamp[2].put_start_and_end_on(lamp[2].get_start(), lamp[2].get_end() + np.array([0, -PULL, 0]))
    lamp[3].shift(np.array([0, -PULL, 0]))
    return lamp


def zoomed(m):
    return m.scale(ZOOM, about_point=SCREEN_CENTER).shift(-SCREEN_CENTER)


POSES = {
    "stand": dict(neck=(0, 1.75), hip=(0, 1.0), head=(0, 2.05),
                  arm_a=((0.2, 1.4), (0.25, 1.05)), arm_b=((-0.2, 1.4), (-0.25, 1.05)),
                  leg_a=((0.12, 0.5), (0.2, 0)), leg_b=((-0.12, 0.5), (-0.2, 0))),
    "run1": dict(neck=(0.25, 1.72), hip=(0, 1.05), head=(0.42, 1.98),
                 arm_a=((0.55, 1.45), (0.8, 1.72)), arm_b=((-0.12, 1.35), (-0.45, 1.2)),
                 leg_a=((0.45, 0.68), (0.5, 0.15)), leg_b=((-0.2, 0.55), (-0.62, 0.35))),
    "run2": dict(neck=(0.25, 1.72), hip=(0, 1.05), head=(0.42, 1.98),
                 arm_a=((-0.12, 1.35), (-0.45, 1.2)), arm_b=((0.55, 1.45), (0.8, 1.72)),
                 leg_a=((-0.2, 0.55), (-0.62, 0.35)), leg_b=((0.45, 0.68), (0.5, 0.15))),
    "reach": dict(neck=(0.05, 1.8), hip=(0, 1.05), head=(0.12, 2.1),
                  arm_a=((0.2, 2.2), (0.3, 2.6)), arm_b=((-0.3, 1.6), (-0.5, 1.8)),
                  leg_a=((0.25, 0.6), (0.15, 0.25)), leg_b=((-0.2, 0.6), (-0.1, 0.2))),
    "pull": dict(neck=(0.05, 1.5), hip=(-0.05, 0.8), head=(0.12, 1.8),
                 arm_a=((0.3, 1.95), (0.3, 2.35)), arm_b=((-0.3, 1.25), (-0.35, 0.95)),
                 leg_a=((0.35, 0.42), (0.3, 0)), leg_b=((-0.35, 0.42), (-0.3, 0))),
    "bow": dict(neck=(0.55, 1.5), hip=(0, 1.0), head=(0.8, 1.3),
                arm_a=((0.35, 1.1), (0.15, 0.85)), arm_b=((0.1, 1.3), (-0.3, 1.2)),
                leg_a=((0.1, 0.5), (0.2, 0)), leg_b=((-0.08, 0.5), (-0.2, 0))),
}
HAND_REACH = POSES["reach"]["arm_a"][1]
GUY_X = CHAIN_X - HAND_REACH[0]
JUMP = BEAD_TOP - FLOOR_Y - HAND_REACH[1]


def stick(pose: str, x: float = 0.0, lift: float = 0.0) -> VGroup:
    p = POSES[pose]
    at = np.array([x, FLOOR_Y + lift, 0.0])

    def limb(start, joints):
        return _poly(start, *joints, width=BOLD)

    head = Circle(radius=0.25).set_fill(INK, 1).set_stroke(width=0).move_to(np.array([*p["head"], 0.0]))
    torso = _poly(p["hip"], p["neck"], width=BOLD)
    figure = VGroup(head, torso, limb(p["neck"], p["arm_a"]), limb(p["neck"], p["arm_b"]),
                    limb(p["hip"], p["leg_a"]), limb(p["hip"], p["leg_b"]))
    return figure.shift(at)


def speech(text: str) -> VGroup:
    label = style.mono(text, 36, INK)
    bubble = RoundedRectangle(corner_radius=0.25, width=label.width + 0.6, height=label.height + 0.5).move_to(label)
    bubble.set_stroke(INK, MID).set_fill(BG, 1)
    tail = _poly((bubble.get_bottom()[0] + 0.2, bubble.get_bottom()[1]),
                 (bubble.get_bottom()[0] + 0.55, bubble.get_bottom()[1] - 0.35),
                 (bubble.get_bottom()[0] + 0.55, bubble.get_bottom()[1]), width=MID)
    return VGroup(bubble, tail, label)


class StageMoves:
    def run_to(self, guy, x_from: float, x_to: float, strides: int, stride_time: float = 0.13) -> None:
        step = (x_to - x_from) / strides
        for k in range(1, strides + 1):
            pose = "run2" if k % 2 else "run1"
            self.play(Transform(guy, stick(pose, x_from + step * k), rate_func=rate_functions.linear),
                      run_time=stride_time)
        self.play(Transform(guy, stick("stand", x_to), rate_func=motion.SPRING), run_time=0.2)

    def pull_chain(self, guy, lamp_room, lit_after: bool) -> None:
        x = GUY_X
        self.play(Transform(guy, stick("reach", x, lift=JUMP), rate_func=rate_functions.ease_out_quad),
                  run_time=0.25)
        self.play(Transform(guy, stick("pull", x), rate_func=rate_functions.ease_in_quad),
                  Transform(lamp_room.lamp, pulled(lamp_room)), run_time=0.22)
        after = room(lit=lit_after, screen_on=False)
        self.play(Transform(guy, stick("stand", x), rate_func=motion.SPRING),
                  Transform(lamp_room, after, rate_func=motion.SPRING), run_time=0.45)
