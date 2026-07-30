from manim import DOWN, RIGHT, UL, FadeIn, Rectangle, Transform, ValueTracker, always_redraw

from theme import BLUE, DIM, INK, ORANGE, PROOF, VideoScene, mono

BENCHMARKS = [
    ("clear_lowest_bit", 18, 98, 2),
    ("smear_lowest_bit", 19, 97, 2),
    ("isolate_rmb", 14, 97, 2),
]

BAR_START_X = -4.3
MAX_BAR_WIDTH = 9.6
MAX_VALUE = 98
SCALE = MAX_BAR_WIDTH / MAX_VALUE
MIN_BAR_WIDTH = 0.35
BAR_HEIGHT = 0.5

ROW_Y = {"gcc": 1.6, "clang": 0.3, "superopt": -1.0}


def bar_width(value: float) -> float:
    return max(value * SCALE, MIN_BAR_WIDTH)


def make_bar(value: float, y: float, color: str) -> Rectangle:
    w = bar_width(value)
    bar = Rectangle(width=w, height=BAR_HEIGHT, fill_color=color, fill_opacity=1, stroke_width=0)
    bar.move_to([BAR_START_X + w / 2, y, 0])
    return bar


def zero_bar(y: float, color: str) -> Rectangle:
    bar = Rectangle(width=0.001, height=BAR_HEIGHT, fill_color=color, fill_opacity=1, stroke_width=0)
    bar.move_to([BAR_START_X, y, 0])
    return bar


class TheScoreboard(VideoScene):
    def construct(self):
        name, gcc_v, clang_v, superopt_v = BENCHMARKS[0]

        title = mono(name, size=40, color=INK).to_corner(UL, buff=0.7)
        self.play(FadeIn(title), run_time=0.8)

        gcc_label = mono("gcc -O3", size=24, color=DIM)
        gcc_label.move_to([BAR_START_X - 0.3, ROW_Y["gcc"], 0], aligned_edge=RIGHT)
        clang_label = mono("clang -O3", size=24, color=DIM)
        clang_label.move_to([BAR_START_X - 0.3, ROW_Y["clang"], 0], aligned_edge=RIGHT)
        superopt_label = mono("superopt", size=24, color=DIM)
        superopt_label.move_to([BAR_START_X - 0.3, ROW_Y["superopt"], 0], aligned_edge=RIGHT)

        self.play(FadeIn(gcc_label), FadeIn(clang_label), FadeIn(superopt_label), run_time=0.8)
        self.wait(0.3)

        gcc_tracker = ValueTracker(0)
        clang_tracker = ValueTracker(0)
        superopt_tracker = ValueTracker(0)

        gcc_bar = zero_bar(ROW_Y["gcc"], DIM)
        clang_bar = zero_bar(ROW_Y["clang"], ORANGE)
        superopt_bar = zero_bar(ROW_Y["superopt"], BLUE)
        self.add(gcc_bar, clang_bar, superopt_bar)

        gcc_number = always_redraw(
            lambda: mono(f"{round(gcc_tracker.get_value())}", size=26, color=DIM).next_to(
                gcc_bar, RIGHT, buff=0.25
            )
        )
        clang_number = always_redraw(
            lambda: mono(f"{round(clang_tracker.get_value())}", size=26, color=ORANGE).next_to(
                clang_bar, RIGHT, buff=0.25
            )
        )
        superopt_number = always_redraw(
            lambda: mono(f"{round(superopt_tracker.get_value())}", size=26, color=BLUE).next_to(
                superopt_bar, RIGHT, buff=0.25
            )
        )
        self.add(gcc_number, clang_number, superopt_number)

        self.play(
            Transform(gcc_bar, make_bar(gcc_v, ROW_Y["gcc"], DIM)),
            gcc_tracker.animate.set_value(gcc_v),
            run_time=1.6,
        )
        self.wait(0.3)
        self.play(
            Transform(clang_bar, make_bar(clang_v, ROW_Y["clang"], ORANGE)),
            clang_tracker.animate.set_value(clang_v),
            run_time=2.6,
        )
        self.wait(0.3)
        self.play(
            Transform(superopt_bar, make_bar(superopt_v, ROW_Y["superopt"], BLUE)),
            superopt_tracker.animate.set_value(superopt_v),
            run_time=1.0,
        )
        proven = mono("proven", size=18, color=PROOF).next_to(superopt_number, RIGHT, buff=0.3)
        self.play(FadeIn(proven), run_time=0.5)
        self.wait(5.0)

        for name2, gcc_v2, clang_v2, superopt_v2 in BENCHMARKS[1:]:
            new_title = mono(name2, size=40, color=INK).to_corner(UL, buff=0.7)
            self.play(
                Transform(title, new_title),
                Transform(gcc_bar, make_bar(gcc_v2, ROW_Y["gcc"], DIM)),
                gcc_tracker.animate.set_value(gcc_v2),
                Transform(clang_bar, make_bar(clang_v2, ROW_Y["clang"], ORANGE)),
                clang_tracker.animate.set_value(clang_v2),
                run_time=2.2,
            )
            self.wait(5.0)

        self.wait(1.0)
        summary = mono("2   2   2", size=36, color=INK)
        summary.move_to(DOWN * 2.6)

        self.play(FadeIn(summary), run_time=0.6)
        self.play(summary.animate.scale(1.15), run_time=0.5)
        self.wait(3.9)
