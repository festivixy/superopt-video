from __future__ import annotations

from collections.abc import Callable, Sequence

from manim import Animation, ManimColor, Mobject, rate_functions

SPRING = rate_functions.ease_out_back
ELASTIC = rate_functions.ease_out_elastic
ANTICIPATE = rate_functions.ease_in_back
DROP = rate_functions.ease_in_quad


def looped(rate: Callable[[float], float], cycles: int) -> Callable[[float], float]:
    def f(t: float) -> float:
        return rate((t * cycles) % 1.0) if t < 1.0 else rate(0.0)
    return f


class ColorCycle(Animation):
    def __init__(self, mobject: Mobject, colors: Sequence[str], cycles: int = 1,
                 parts: tuple[str, ...] = ("fill",), **kwargs) -> None:
        start = (mobject.get_fill_color() if "fill" in parts else mobject.get_stroke_color()).to_hex().upper()
        if start != ManimColor(colors[0]).to_hex().upper():
            raise ValueError(f"colour cycle must start from the current colour {start}, got {colors[0]}")
        self.colors = [ManimColor(c) for c in colors] + [ManimColor(colors[0])]
        self.cycles = cycles
        self.parts = parts
        self._original = (mobject.get_fill_color(), mobject.get_stroke_color())
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        if alpha >= 1.0:
            fill, stroke = self._original
            if "fill" in self.parts:
                self.mobject.set_fill(fill)
            if "stroke" in self.parts:
                self.mobject.set_stroke(stroke)
            return
        phase = (alpha * self.cycles) % 1.0
        span = len(self.colors) - 1
        i = min(int(phase * span), span - 1)
        colour = self.colors[i].interpolate(self.colors[i + 1], phase * span - i)
        if "fill" in self.parts:
            self.mobject.set_fill(colour)
        if "stroke" in self.parts:
            self.mobject.set_stroke(colour)
