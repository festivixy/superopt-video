from __future__ import annotations

import numpy as np
from manim import DOWN, Circle, Line, Rectangle, RoundedRectangle, VGroup, VMobject

from kit.style import BLUE, DIM, GREEN, INK, MAGENTA, ORANGE

BOLD = 7
MID = 4
THIN_PROP = 2.5


def _stroke(m: VMobject, color: str = INK, width: float = MID) -> VMobject:
    m.set_stroke(color=color, width=width)
    m.set_fill(opacity=0)
    try:
        from manim.constants import CapStyleType

        m.set_cap_style(CapStyleType.ROUND)
    except (ImportError, AttributeError):
        pass
    return m


def _poly(*pts, color: str = INK, width: float = MID, closed: bool = False) -> VMobject:
    m = VMobject()
    points = [np.array([x, y, 0.0]) for x, y in pts]
    if closed:
        points.append(points[0])
    m.set_points_as_corners(points)
    return _stroke(m, color, width)


def stick_guy() -> VGroup:
    head = Circle(radius=0.26).set_fill(INK, 1).set_stroke(INK, 0).move_to([0.18, 1.55, 0])
    body = _poly((0.1, 1.25), (-0.1, 0.45), width=BOLD)
    arms = _poly((0.55, 1.05), (0.05, 1.05), (0.6, 0.85), width=BOLD)
    legs = _poly((-0.45, -0.3), (-0.1, 0.45), (0.3, -0.3), width=BOLD)
    guy = VGroup(body, arms, legs, head)
    guy.head, guy.arms = head, arms
    return guy


_S = 0.93 * 14.2222 / 200


def _p(x: float, y: float) -> tuple[float, float]:
    return ((x - 100) * _S, (56 - y) * _S)


def _mp(*pts, **kw) -> VMobject:
    return _poly(*[_p(*q) for q in pts], **kw)


def _rect(x0: float, y0: float, x1: float, y1: float, radius: float = 0.0) -> RoundedRectangle:
    (ax, ay), (bx, by) = _p(x0, y0), _p(x1, y1)
    r = RoundedRectangle(corner_radius=radius, width=abs(bx - ax), height=abs(by - ay)) if radius else \
        Rectangle(width=abs(bx - ax), height=abs(by - ay))
    return r.move_to([(ax + bx) / 2, (ay + by) / 2, 0])


_SCREENS = {"left": (19, 13, 93, 53), "right": (107, 13, 181, 53)}


def screen_zone(side: str):
    from kit.zones import ZONES, Zone

    if side not in _SCREENS:
        return ZONES[side]
    x0, y0, x1, y1 = _SCREENS[side]
    (ax, ay), (bx, by) = _p(x0, y0), _p(x1, y1)
    return Zone((ax + bx) / 2, (ay + by) / 2, abs(bx - ax), abs(by - ay))


def on_screen(m, side: str, align: str = "center"):
    from kit.zones import _fit_into

    return _fit_into(m, screen_zone(side), align)


def code_lines(side: str, rows: int = 7, seed: int = 0) -> VGroup:
    import random

    rng = random.Random(seed)
    z = screen_zone(side)
    step = z.height / (rows + 1)
    block = VGroup()
    indent = 0
    for r in range(rows):
        y = z.top - step * (r + 1)
        x = z.left + 0.25 + indent * 0.35
        kind = rng.random()
        if kind < 0.18:
            segs = [(rng.uniform(0.35, 0.6), DIM)]
        else:
            segs = [(rng.uniform(0.1, 0.18), MAGENTA if kind > 0.85 else BLUE), (rng.uniform(0.2, 0.5), INK)]
        for frac, colour in segs:
            length = frac * (z.width - 0.5 - indent * 0.35)
            block.add(Line([x, y, 0], [x + length, y, 0]).set_stroke(colour, 6))
            x += length + 0.18
        indent = max(0, min(3, indent + rng.choice([-1, 0, 1, 1])))
    return block


def pov_desk() -> VGroup:
    led = _rect(14, 60, 186, 63).set_stroke(width=0).set_fill(BLUE, 0.7)
    left_monitor = VGroup(_stroke(_rect(14, 8, 98, 58, 0.18)),
                          _mp((54, 58), (54, 66)), _mp((44, 66), (64, 66)))
    right_monitor = VGroup(_stroke(_rect(102, 8, 186, 58, 0.18)),
                           _mp((146, 58), (146, 66)), _mp((136, 66), (156, 66)))
    desk_edge = _mp((0, 72), (200, 72), color=DIM, width=THIN_PROP)

    arm = _mp((11, 63), (14, 60), width=THIN_PROP)
    robot = VGroup(
        _stroke(_rect(4, 54, 12, 61, 0.08), width=THIN_PROP),
        Circle(radius=0.05).set_fill(GREEN, 1).set_stroke(width=0).move_to([*_p(6.5, 57.5), 0]),
        Circle(radius=0.05).set_fill(GREEN, 1).set_stroke(width=0).move_to([*_p(9.5, 57.5), 0]),
        _mp((8, 54), (8, 51), width=THIN_PROP),
        Circle(radius=0.06).set_fill(MAGENTA, 1).set_stroke(width=0).move_to([*_p(8, 50.4), 0]),
        _stroke(_rect(5, 61, 11, 69, 0.06), width=THIN_PROP),
        arm,
    )
    robot.arm, robot.pivot = arm, np.array([*_p(11, 63), 0.0])

    headphones = VGroup(_mp((190, 71), (190, 58), width=THIN_PROP), _mp((184, 60), (190, 52.5), (196, 60), width=THIN_PROP),
                        _stroke(_rect(182.5, 59, 185.5, 65, 0.06), width=THIN_PROP),
                        _stroke(_rect(194.5, 59, 197.5, 65, 0.06), width=THIN_PROP))
    keyboard = VGroup(_mp((60, 80), (140, 80), (148, 96), (52, 96), closed=True),
                      _mp((58, 85), (142, 85), color=DIM, width=THIN_PROP), _mp((56, 90), (144, 90), color=DIM, width=THIN_PROP))
    controller = VGroup(_stroke(_rect(10, 80, 38, 94, 0.3)),
                        _mp((15, 86), (19, 86), width=THIN_PROP), _mp((17, 84), (17, 88), width=THIN_PROP),
                        Circle(radius=0.07).set_fill(ORANGE, 1).set_stroke(width=0).move_to([*_p(31, 85), 0]),
                        Circle(radius=0.07).set_fill(BLUE, 1).set_stroke(width=0).move_to([*_p(33.5, 87.5), 0]))
    tiles = VGroup(*[_rect(x, y, x + 3.3, y + 3.3).set_stroke(width=0).set_fill(c, 0.8)
                     for (x, y), c in zip(((161, 81), (164.4, 84.4), (167.7, 87.7)), (MAGENTA, ORANGE, GREEN))])
    cube = VGroup(_stroke(_rect(160, 80, 172, 92, 0.06), width=THIN_PROP), tiles)
    cube.tiles = tiles
    can = VGroup(_stroke(_rect(178, 80, 186, 94), BLUE, THIN_PROP), _mp((178, 83), (186, 83), color=BLUE, width=THIN_PROP))
    plant = VGroup(_mp((192, 94), (198, 94), (197, 88), (193, 88), closed=True, color=GREEN, width=THIN_PROP),
                   _mp((195, 88), (192, 82), (194, 80), color=GREEN, width=THIN_PROP),
                   _mp((195, 88), (198, 83), (197, 80), color=GREEN, width=THIN_PROP))

    def hand(sx, sy, fx, fy):
        fist = Circle(radius=3.4 * _S).set_fill(INK, 1).set_stroke(width=0).move_to([*_p(fx, fy), 0])
        h = VGroup(_mp((sx, sy), (fx, fy), width=BOLD + 2), fist)
        h.shoulder = np.array([*_p(sx, sy), 0.0])
        return h

    hands = VGroup(hand(40, 132, 84, 90), hand(160, 132, 116, 91))

    desk = VGroup(led, left_monitor, right_monitor, desk_edge, robot, headphones, keyboard,
                  controller, cube, can, plant, hands)
    desk.led, desk.left_monitor, desk.right_monitor = led, left_monitor, right_monitor
    desk.robot, desk.headphones, desk.keyboard, desk.controller = robot, headphones, keyboard, controller
    desk.cube, desk.can, desk.plant, desk.hands = cube, can, plant, hands
    return desk


def desk_idle(desk: VGroup) -> list:
    from manim import Rotate, rate_functions

    from kit import motion

    anims = [
        Rotate(desk.robot.arm, angle=-0.8, about_point=desk.robot.pivot,
               rate_func=motion.looped(rate_functions.there_and_back, 3)),
        motion.ColorCycle(desk.led, [BLUE, MAGENTA, GREEN, ORANGE]),
    ]
    palettes = ([MAGENTA, BLUE, GREEN], [ORANGE, MAGENTA, BLUE], [GREEN, ORANGE, MAGENTA])
    anims += [motion.ColorCycle(t, p, cycles=2) for t, p in zip(desk.cube.tiles, palettes)]
    for i, h in enumerate(desk.hands):
        anims.append(Rotate(h, angle=0.06 if i == 0 else -0.06, about_point=h.shoulder,
                            rate_func=motion.looped(rate_functions.there_and_back, 14 + 3 * i)))
    return anims


def eraser(height: float = 1.2) -> VGroup:
    body = RoundedRectangle(corner_radius=0.12, width=height * 0.55, height=height)
    body.set_stroke(INK, MID).set_fill(DIM, 0.35)
    felt = Rectangle(width=height * 0.55, height=height * 0.22).set_stroke(width=0).set_fill(ORANGE, 0.8)
    felt.align_to(body, DOWN)
    return VGroup(body, felt)
