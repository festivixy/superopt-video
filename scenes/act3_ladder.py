from manim import LEFT, RIGHT, Circle, FadeIn, FadeOut, Indicate, LaggedStart, Line, RoundedRectangle, Text, VGroup

from theme import DIM, INK, ORANGE, PROOF, VideoScene, mono

RUNGS = [("length 1", -1.6), ("length 2", 0.6), ("length 3", 2.8)]
TRACK_LEFT = -3.7
TRACK_RIGHT = 4.7
TRACK_X = (TRACK_LEFT + TRACK_RIGHT) / 2
TRACK_WIDTH = TRACK_RIGHT - TRACK_LEFT
CHIP_W = 0.5
CHIP_H = 0.3


def make_track(y: float) -> RoundedRectangle:
    track = RoundedRectangle(
        corner_radius=0.06, width=TRACK_WIDTH, height=0.14, stroke_width=0, fill_color=DIM, fill_opacity=1
    )
    track.move_to([TRACK_X, y, 0])
    return track


def make_chip(x: float, y: float) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.05, width=CHIP_W, height=CHIP_H, stroke_color=INK, stroke_width=1.5, fill_color=INK, fill_opacity=0.12
    ).move_to([x, y, 0])


def highlight(scene: VideoScene, track: RoundedRectangle, label: Text, color: str) -> None:
    scene.play(track.animate.set_fill(color), label.animate.set_color(color), run_time=0.5)


def make_seal(y: float) -> VGroup:
    ring = Circle(radius=0.22, stroke_color=DIM, stroke_width=3, fill_opacity=0)
    mark1 = Line([-0.13, -0.13, 0], [0.13, 0.13, 0], stroke_color=DIM, stroke_width=3)
    mark2 = Line([-0.13, 0.13, 0], [0.13, -0.13, 0], stroke_color=DIM, stroke_width=3)
    seal = VGroup(ring, mark1, mark2)
    seal.move_to([TRACK_X, y, 0])
    return seal


def stream_fail(scene: VideoScene, y: float, n: int) -> None:
    xs = [TRACK_LEFT + 0.6 + i * (TRACK_WIDTH - 1.2) / (n - 1) for i in range(n)]
    chips = VGroup(*[make_chip(x, y) for x in xs])
    scene.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in chips], lag_ratio=0.15), run_time=0.3 + 0.15 * n)
    scene.wait(0.5)

    marks = VGroup(*[mono("x", size=14, color=ORANGE).move_to(c.get_center()) for c in chips])
    scene.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.12), run_time=0.25 + 0.12 * n)
    scene.play(
        LaggedStart(*[FadeOut(VGroup(c, m)) for c, m in zip(chips, marks)], lag_ratio=0.12),
        run_time=0.25 + 0.12 * n,
    )


def stream_winner(scene: VideoScene, y: float, n: int, winner_index: int) -> RoundedRectangle:
    xs = [TRACK_LEFT + 0.6 + i * (TRACK_WIDTH - 1.2) / (n - 1) for i in range(n)]
    chips = VGroup(*[make_chip(x, y) for x in xs])
    scene.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in chips], lag_ratio=0.15), run_time=0.3 + 0.15 * n)
    scene.wait(0.5)

    winner = chips[winner_index]
    others = [c for i, c in enumerate(chips) if i != winner_index]
    marks = VGroup(*[mono("x", size=14, color=ORANGE).move_to(c.get_center()) for c in others])

    scene.play(
        Indicate(winner, color=PROOF, scale_factor=1.6),
        LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.12),
        run_time=0.9,
    )
    scene.play(
        winner.animate.scale(1.3).set_stroke(PROOF).set_fill(PROOF, opacity=0.3),
        LaggedStart(*[FadeOut(VGroup(c, m)) for c, m in zip(others, marks)], lag_ratio=0.1),
        run_time=0.9,
    )
    return winner


class TheLadder(VideoScene):
    def construct(self) -> None:
        tracks = VGroup(*[make_track(y) for _, y in RUNGS])
        labels = VGroup(
            *[mono(text, size=22, color=DIM).next_to(track, LEFT, buff=0.4) for (text, _), track in zip(RUNGS, tracks)]
        )
        rail_left = Line([TRACK_LEFT, RUNGS[0][1] - 0.4, 0], [TRACK_LEFT, RUNGS[-1][1] + 0.4, 0], stroke_color=DIM, stroke_width=2)
        rail_right = Line([TRACK_RIGHT, RUNGS[0][1] - 0.4, 0], [TRACK_RIGHT, RUNGS[-1][1] + 0.4, 0], stroke_color=DIM, stroke_width=2)

        self.play(FadeIn(rail_left), FadeIn(rail_right), FadeIn(tracks), FadeIn(labels), run_time=1.2)
        self.wait(2.0)

        track1, track2, _ = tracks
        label1, label2, _ = labels
        y1 = RUNGS[0][1]
        y2 = RUNGS[1][1]

        highlight(self, track1, label1, INK)
        self.wait(0.7)
        stream_fail(self, y1, 6)

        none_label = mono("none work", size=20, color=DIM).next_to(track1, RIGHT, buff=0.4)
        self.play(FadeIn(none_label), run_time=0.5)
        highlight(self, track1, label1, DIM)
        self.wait(1.3)

        self.play(VGroup(track1, label1, none_label).animate.set_opacity(0.4), run_time=0.6)
        self.wait(0.5)

        seal = make_seal(y1)
        self.play(FadeIn(seal, scale=1.6), run_time=0.5)
        self.wait(1.2)

        highlight(self, track2, label2, INK)
        self.wait(0.7)

        stream_winner(self, y2, 6, 3)
        self.wait(16.5)
