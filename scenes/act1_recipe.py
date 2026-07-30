from manim import DOWN, RIGHT, AnimationGroup, Circle, FadeIn, FadeOut, Indicate, VGroup

from theme import BLUE, INK, VideoScene, machine, mono

MACHINE_WIDTH = 3.6
MACHINE_CENTER = [-2.3, 0.3, 0]
RESULTS_ANCHOR = [4.6, 0.3, 0]

PASSES = [(6, 12, 1.5), (21, 42, 1.0), (3, 6, 0.55)]


def make_token(value: int, radius: float = 0.34) -> VGroup:
    chip = Circle(radius=radius, stroke_color=BLUE, stroke_width=2.5, fill_opacity=0)
    digit = mono(str(value), size=24, color=BLUE).move_to(chip.get_center())
    token = VGroup(chip, digit)
    token.chip = chip
    token.digit = digit
    return token


def run_pass(scene: VideoScene, mach: VGroup, results: VGroup, in_val: int, out_val: int, speed: float) -> None:
    inlet_x, y, _ = mach.inlet.get_center()
    outlet_x, _, _ = mach.outlet.get_center()

    token = make_token(in_val).move_to([inlet_x - 1.6, y, 0])
    scene.play(FadeIn(token, shift=RIGHT * 0.3), run_time=0.3 * speed)
    scene.play(token.animate.move_to([inlet_x, y, 0]), run_time=0.4 * speed)
    scene.play(FadeOut(token, scale=0.2), run_time=0.25 * speed)

    scene.play(
        AnimationGroup(*[Indicate(s, color=INK, scale_factor=1.3) for s in mach.stations], lag_ratio=0.45),
        run_time=0.9 * speed,
    )

    output = make_token(out_val).move_to([outlet_x, y, 0])
    scene.play(FadeIn(output, scale=0.4), run_time=0.25 * speed)

    result = mono(f"{in_val} → {out_val}", size=24, color=BLUE)
    result.move_to(output.get_center())
    scene.play(FadeOut(output), FadeIn(result), run_time=0.3 * speed)

    results.add(result)
    scene.play(results.animate.arrange(DOWN, buff=0.5).move_to(RESULTS_ANCHOR), run_time=0.5 * speed)
    scene.wait(0.7 * speed)


class WhatIsAProgram(VideoScene):
    def construct(self) -> None:
        mach = machine(n_stations=3, width=MACHINE_WIDTH)
        mach.move_to(MACHINE_CENTER)
        self.play(FadeIn(mach), run_time=0.9)
        self.wait(0.6)

        results = VGroup()
        for in_val, out_val, speed in PASSES:
            run_pass(self, mach, results, in_val, out_val, speed)

        self.wait(1.0)
        for _ in range(2):
            self.play(mach.body.animate.set_stroke(opacity=0.55), run_time=1.0)
            self.play(mach.body.animate.set_stroke(opacity=1.0), run_time=1.0)
        self.wait(12.5)
