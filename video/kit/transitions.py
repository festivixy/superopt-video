from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, Animation, AnimationGroup, FadeOut, Group, Mobject, Succession, Transform,
    config, rate_functions,
)

from kit import cartoon, motion


def _off(m: Mobject, target: Mobject, rate) -> Transform:
    return Transform(m, target, remover=True, rate_func=rate)


def fade(mobs: Sequence[Mobject], **_) -> Animation:
    return FadeOut(*mobs)


def pop(mobs: Sequence[Mobject], **_) -> Animation:
    return AnimationGroup(*[_off(m, m.copy().scale(0.01), motion.ANTICIPATE) for m in mobs])


def fall(mobs: Sequence[Mobject], **_) -> Animation:
    bottom = -config.frame_height / 2
    anims = []
    for i, m in enumerate(sorted(mobs, key=lambda m: m.get_center()[0])):
        drop = m.get_top()[1] - bottom + 0.5
        spin = 0.35 if i % 2 == 0 else -0.3
        anims.append(_off(m, m.copy().shift(DOWN * drop).rotate(spin), motion.DROP))
    return AnimationGroup(*anims, lag_ratio=0.12)


def swipe(mobs: Sequence[Mobject], **_) -> Animation:
    half = config.frame_width / 2
    rub = cartoon.eraser(height=config.frame_height * 0.9)
    start, end = LEFT * (half + rub.width), RIGHT * (half + rub.width)
    rub.move_to(start)
    anims = [_off(rub, rub.copy().move_to(end), rate_functions.linear)]
    span = end[0] - start[0]
    for m in mobs:
        at = float(np.clip((m.get_center()[0] - start[0]) / span, 0.0, 0.9))
        anims.append(FadeOut(m, rate_func=lambda t, a=at: float(np.clip((t - a) / 0.1, 0.0, 1.0))))
    return AnimationGroup(*anims)


def shove(mobs: Sequence[Mobject], **_) -> Animation:
    content = Group(*mobs)
    guy = cartoon.stick_guy().scale(1.7)
    guy.move_to([-config.frame_width / 2 - guy.width, content.get_center()[1], 0])
    at_edge = guy.copy().next_to(content, LEFT, buff=0.05)
    dist = config.frame_width / 2 - content.get_left()[0] + 0.5
    push = [_off(m, m.copy().shift(RIGHT * dist), motion.ANTICIPATE) for m in mobs]
    push.append(_off(guy, at_edge.copy().shift(RIGHT * (dist + guy.width)), motion.ANTICIPATE))
    return Succession(
        Transform(guy, at_edge, rate_func=motion.SPRING, run_time=0.4),
        AnimationGroup(*push, run_time=0.6),
    )


def dive(mobs: Sequence[Mobject], focus=ORIGIN, **_) -> Animation:
    focus = np.array(focus, dtype=float)
    return AnimationGroup(*[
        _off(m, m.copy().scale(9, about_point=focus).set_opacity(0), rate_functions.ease_in_cubic) for m in mobs
    ])


TRANSITIONS: dict[str, Callable[..., Animation]] = {
    "fade": fade, "pop": pop, "fall": fall, "swipe": swipe, "shove": shove, "dive": dive,
}


def get(style: str) -> Callable[..., Animation]:
    if style not in TRANSITIONS:
        raise ValueError(f"unknown transition {style!r}; expected one of {sorted(TRANSITIONS)}")
    return TRANSITIONS[style]
