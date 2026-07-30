from manim import DOWN, RIGHT, UP, UR, Circle, Dot, FadeIn, FadeOut, Indicate, Transform, VGroup

from theme import BLUE, DIM, INK, ORANGE, PROOF, VideoScene, mono

COLS = 60
ROWS = 34
X_MIN, X_MAX = -6.9, 6.9
Y_MIN, Y_MAX = -3.6, 3.6
DX = (X_MAX - X_MIN) / (COLS - 1)
DY = (Y_MAX - Y_MIN) / (ROWS - 1)

STOPS = [(12, 25), (16, 26), (14, 22), (18, 24)]
LIGHT_OFFSETS = [(0, 0), (1, 0), (0, 1)]
TARGET = (52, 6)


def point_at(c: int, r: int) -> list:
    return [X_MIN + c * DX, Y_MIN + r * DY, 0]


def dot_index(c: int, r: int) -> int:
    return r * COLS + c


class TheInputWall(VideoScene):
    def construct(self) -> None:
        flat = [
            Dot(point=point_at(c, r), radius=0.035, color=DIM, fill_opacity=0.35, stroke_width=0)
            for r in range(ROWS)
            for c in range(COLS)
        ]
        grid = VGroup(*flat)
        self.play(FadeIn(grid), run_time=1.6)

        star_number = mono("4,294,967,296", size=30, color=INK).to_edge(UP, buff=0.5)
        self.play(FadeIn(star_number), run_time=0.8)
        self.wait(1.3)

        spotlight = Circle(radius=0.55, stroke_color=BLUE, stroke_width=3, fill_opacity=0)
        spotlight.move_to(point_at(*STOPS[0]))
        self.play(FadeIn(spotlight), run_time=0.4)

        counter = mono("tested: 0", size=22, color=DIM).to_corner(UR, buff=0.5)
        self.play(FadeIn(counter), run_time=0.4)
        self.wait(0.3)

        tested = 0
        for c0, r0 in STOPS:
            self.play(spotlight.animate.move_to(point_at(c0, r0)), run_time=0.5)
            lit = []
            for oc, orow in LIGHT_OFFSETS:
                c, r = c0 + oc, r0 + orow
                if 0 <= c < COLS and 0 <= r < ROWS:
                    lit.append(flat[dot_index(c, r)])
            tested += len(lit)
            new_counter = mono(f"tested: {tested}", size=22, color=DIM).move_to(counter, aligned_edge=RIGHT)
            self.play(
                *[d.animate.set_color(PROOF).scale(2.2) for d in lit],
                Transform(counter, new_counter),
                run_time=0.5,
            )

        self.wait(0.8)

        million_counter = mono("tested: 1,000,000", size=22, color=DIM).move_to(counter, aligned_edge=RIGHT)
        self.play(Transform(counter, million_counter), run_time=0.6)
        self.wait(1.4)

        self.play(grid.animate.scale(1.18), run_time=1.8)
        self.wait(1.2)

        target = flat[dot_index(*TARGET)]
        self.play(target.animate.set_color(ORANGE).scale(10), run_time=0.6)
        self.play(Indicate(target, color=ORANGE, scale_factor=1.5), run_time=0.9)
        self.wait(0.4)

        self.play(FadeOut(star_number), FadeOut(counter), FadeOut(spotlight), run_time=0.6)
        self.wait(3.7)
