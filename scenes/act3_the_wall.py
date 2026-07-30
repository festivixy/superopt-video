import random

from manim import RIGHT, UP, Dot, FadeIn, Line, RoundedRectangle, VGroup

from theme import DIM, ORANGE, VideoScene, mono

RUNGS = [
    ("length 1 — dozens", -2.3, 6, 20, DIM, False),
    ("length 2 — thousands", -0.6, 12, 26, DIM, False),
    ("length 3 — millions", 1.1, 20, 32, ORANGE, False),
    ("length 4 — billions", 2.8, 28, 38, ORANGE, True),
]
TRACK_LEFT = -6.0
TRACK_RIGHT = -2.4
TRACK_WIDTH = TRACK_RIGHT - TRACK_LEFT
TRACK_X = (TRACK_LEFT + TRACK_RIGHT) / 2


def make_track(y: float) -> RoundedRectangle:
    track = RoundedRectangle(
        corner_radius=0.05, width=TRACK_WIDTH, height=0.1, stroke_width=0, fill_color=DIM, fill_opacity=1
    )
    track.move_to([TRACK_X, y, 0])
    return track


def make_pile(y: float, n: int, seed: int) -> VGroup:
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(n):
        x = rng.uniform(TRACK_LEFT + 0.2, TRACK_RIGHT - 0.2)
        yy = y + rng.uniform(-0.12, 0.12)
        dots.add(Dot(point=[x, yy, 0], radius=0.045, color=DIM, fill_opacity=0.85))
    return dots


def make_spill(y: float, n: int, seed: int) -> VGroup:
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(n):
        x = rng.uniform(TRACK_LEFT + 0.2, TRACK_RIGHT - 0.2)
        dots.add(Dot(point=[x, y + 0.2, 0], radius=0.045, color=ORANGE, fill_opacity=0.85))
    return dots


class TheWall(VideoScene):
    def construct(self) -> None:
        tracks = VGroup(*[make_track(y) for _, y, *_ in RUNGS])
        rail_left = Line([TRACK_LEFT, RUNGS[0][1] - 0.3, 0], [TRACK_LEFT, RUNGS[-1][1] + 0.3, 0], stroke_color=DIM, stroke_width=2)
        rail_right = Line([TRACK_RIGHT, RUNGS[0][1] - 0.3, 0], [TRACK_RIGHT, RUNGS[-1][1] + 0.3, 0], stroke_color=DIM, stroke_width=2)
        self.play(FadeIn(rail_left), FadeIn(rail_right), FadeIn(tracks), run_time=0.9)
        self.wait(1.0)

        for i, (text, y, n, size, color, spill) in enumerate(RUNGS):
            pile = make_pile(y, n, seed=i)
            self.play(FadeIn(pile, lag_ratio=0.05), run_time=0.5 + 0.03 * n)

            label = mono(text, size=size, color=color)
            label.next_to(tracks[i], RIGHT, buff=0.4)
            self.play(FadeIn(label, scale=0.7), run_time=0.5)

            if spill:
                spill_dots = make_spill(y, 8, seed=99)
                self.play(FadeIn(spill_dots), run_time=0.3)
                self.play(*[d.animate.shift(UP * 1.5).set_opacity(0) for d in spill_dots], run_time=1.0)

            self.wait(0.7)

        self.wait(1.0)

        how_word = mono("how?", size=44, color=ORANGE)
        how_word.set_opacity(0.0)
        how_word.move_to([0, -3.0, 0])
        self.add(how_word)
        self.play(how_word.animate.set_opacity(0.7), run_time=0.8)
        self.wait(10.0)
