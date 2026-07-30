from manim import (
    DOWN,
    RIGHT,
    UP,
    AnimationGroup,
    FadeIn,
    FadeOut,
    Indicate,
    Rectangle,
    RoundedRectangle,
    TransformFromCopy,
    ValueTracker,
    VGroup,
    always_redraw,
    linear,
)

from theme import BLUE, DIM, INK, PROOF, VideoScene, mono

CARD_TEXTS = ["x + x", "x << 1"]
CARD_XS = [-3.4, 3.4]
CARD_Y = 1.1
INPUT_Y = 3.2
OUTPUT_Y = -0.6
VALUES = [(7, 14), (3, 6), (255, 510), (12, 24)]
SPEEDS = [1.0, 0.85, 0.7, 0.6]
TOTAL_INPUTS = 4_294_967_296
BAR_WIDTH = 8.0
BAR_Y = -2.6


def make_card(text: str, x: float) -> VGroup:
    box = RoundedRectangle(corner_radius=0.25, width=3.0, height=1.3, stroke_color=INK, stroke_width=2, fill_opacity=0)
    box.move_to([x, CARD_Y, 0])
    label = mono(text, size=32, color=INK).move_to(box.get_center())
    return VGroup(box, label)


def feed_value(scene: VideoScene, in_val: int, out_val: int, speed: float) -> None:
    seed = mono(str(in_val), size=40, color=BLUE).move_to([0, INPUT_Y, 0])
    scene.play(FadeIn(seed, shift=DOWN * 0.2), run_time=0.3 * speed)

    copies = VGroup(*[mono(str(in_val), size=32, color=BLUE).move_to([x, INPUT_Y - 0.05, 0]) for x in CARD_XS])
    scene.play(*[TransformFromCopy(seed, c) for c in copies], FadeOut(seed), run_time=0.35 * speed)

    scene.play(*[c.animate.move_to([c.get_center()[0], CARD_Y, 0]).set_opacity(0) for c in copies], run_time=0.3 * speed)
    scene.remove(*copies)

    outputs = VGroup(*[mono(str(out_val), size=34, color=BLUE).move_to([x, OUTPUT_Y, 0]) for x in CARD_XS])
    scene.play(*[FadeIn(o, shift=UP * 0.15) for o in outputs], run_time=0.3 * speed)
    scene.play(
        AnimationGroup(*[Indicate(o, color=PROOF, scale_factor=1.3) for o in outputs], lag_ratio=0.15),
        run_time=0.5 * speed,
    )
    scene.play(FadeOut(outputs), run_time=0.25 * speed)


class TwoProgramsOneInput(VideoScene):
    def construct(self) -> None:
        cards = VGroup(*[make_card(t, x) for t, x in zip(CARD_TEXTS, CARD_XS)])
        self.play(FadeIn(cards, lag_ratio=0.2), run_time=0.9)
        self.wait(1.4)

        for (in_val, out_val), speed in zip(VALUES, SPEEDS):
            feed_value(self, in_val, out_val, speed)
            self.wait(0.4)

        self.wait(0.8)

        bar_outline = RoundedRectangle(
            corner_radius=0.08, width=BAR_WIDTH, height=0.35, stroke_color=INK, stroke_width=2, fill_opacity=0
        )
        bar_outline.move_to([0, BAR_Y, 0])
        target_label = mono(f"{TOTAL_INPUTS:,}", size=18, color=DIM)
        target_label.next_to(bar_outline, DOWN, buff=0.2)
        target_label.align_to(bar_outline, RIGHT)

        tracker = ValueTracker(0)
        counter = always_redraw(
            lambda: mono(f"{int(tracker.get_value()):,}", size=30, color=BLUE).next_to(bar_outline, UP, buff=0.35)
        )

        def make_fill() -> Rectangle:
            frac = min(1.0, tracker.get_value() / TOTAL_INPUTS)
            width = max(0.01, BAR_WIDTH * frac)
            fill_rect = Rectangle(width=width, height=0.35, stroke_width=0, fill_color=BLUE, fill_opacity=1)
            fill_rect.move_to([bar_outline.get_left()[0] + width / 2, BAR_Y, 0])
            return fill_rect

        fill = always_redraw(make_fill)

        self.play(FadeIn(bar_outline), FadeIn(target_label), run_time=0.5)
        self.play(FadeIn(counter), FadeIn(fill), run_time=0.3)
        self.play(tracker.animate.set_value(3_000_000), run_time=4.0, rate_func=linear)
        self.wait(1.5)
        self.play(tracker.animate.set_value(60_000_000), run_time=3.0, rate_func=linear)
        self.wait(4.7)
