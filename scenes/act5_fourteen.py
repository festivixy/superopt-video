from manim import LEFT, AnimationGroup, FadeIn, Indicate, VGroup

from theme import DIM, INK, VideoScene, mono

NAMES = [
    "absval",
    "avg_ceil",
    "avg_floor",
    "bswap32",
    "clear_lowest_bit",
    "flp2",
    "isolate_lowest_zero",
    "isolate_rmb",
    "popcount",
    "rotl5",
    "sign",
    "smear_lowest_bit",
    "times_nine",
    "turn_off_trailing_ones",
]

PULSE_NAMES = {"clear_lowest_bit", "smear_lowest_bit", "isolate_rmb"}

COL1_X = -3.8
COL2_X = 1.6
TOP_Y = 2.3
ROW_BUFF = 0.62

SCATTER = [
    [-6.4, 3.2, 0],
    [6.4, 3.4, 0],
    [-6.8, -2.8, 0],
    [6.6, -3.0, 0],
    [-5.4, 1.0, 0],
    [5.6, 0.6, 0],
    [-6.2, -0.8, 0],
    [6.3, -1.4, 0],
    [-5.6, 2.6, 0],
    [6.0, 2.0, 0],
    [-6.6, 0.1, 0],
    [6.5, -0.2, 0],
    [-5.3, -2.4, 0],
    [5.8, -2.6, 0],
]


def column_positions() -> list:
    positions = []
    for i in range(7):
        positions.append([COL1_X, TOP_Y - i * ROW_BUFF, 0])
    for i in range(7):
        positions.append([COL2_X, TOP_Y - i * ROW_BUFF, 0])
    return positions


class FourteenJobs(VideoScene):
    def construct(self) -> None:
        labels = [mono(name, size=20, color=DIM).move_to(pos) for name, pos in zip(NAMES, SCATTER)]
        targets = column_positions()

        self.play(
            AnimationGroup(*[FadeIn(label, scale=0.7) for label in labels], lag_ratio=0.05),
            run_time=1.0,
        )
        self.wait(0.3)

        self.play(
            AnimationGroup(
                *[label.animate.move_to(pos, aligned_edge=LEFT) for label, pos in zip(labels, targets)],
                lag_ratio=0.06,
            ),
            run_time=1.8,
        )
        self.wait(0.3)

        pulses = [label for name, label in zip(NAMES, labels) if name in PULSE_NAMES]
        self.play(
            AnimationGroup(*[Indicate(p, color=INK, scale_factor=1.25) for p in pulses], lag_ratio=0.25),
            run_time=1.2,
        )
        self.wait(0.6)
        self.play(
            AnimationGroup(*[Indicate(label, color=DIM, scale_factor=1.15) for label in labels], lag_ratio=0.03),
            run_time=1.4,
        )
        self.wait(14.3)
