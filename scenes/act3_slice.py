import math
import random

from manim import UP, Dot, FadeIn, FadeOut, Indicate, Transform, VGroup

from theme import DIM, INK, ORANGE, VideoScene, mono

CENTER = [0, -0.3, 0]
N_DOTS = 200
R_MAX = 3.3
WEDGE1_END = 2 * math.pi / 3
SURVIVOR_START = math.radians(340)


def scatter_cloud(n: int, r_max: float, seed: int) -> VGroup:
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(n):
        angle = rng.uniform(0, 2 * math.pi)
        radius = rng.uniform(0.25, r_max)
        pos = [CENTER[0] + radius * math.cos(angle), CENTER[1] + radius * math.sin(angle), 0]
        dot = Dot(point=pos, radius=0.035, color=DIM, fill_opacity=0.55)
        dot.wedge_angle = angle
        dots.add(dot)
    return dots


class TheVanishingSlice(VideoScene):
    def construct(self) -> None:
        cloud = scatter_cloud(N_DOTS, R_MAX, seed=11)
        self.play(FadeIn(cloud, lag_ratio=0.01), run_time=1.4)
        self.wait(1.0)

        input1 = mono("failing input: x = 19", size=24, color=ORANGE)
        input1.to_edge(UP, buff=0.6)
        self.play(FadeIn(input1), run_time=0.6)
        self.wait(1.0)

        wedge1 = VGroup(*[d for d in cloud if d.wedge_angle < WEDGE1_END])
        rest1 = VGroup(*[d for d in cloud if d.wedge_angle >= WEDGE1_END])
        self.play(FadeOut(wedge1), run_time=0.8)
        self.wait(1.2)

        input2 = mono("failing input: x = 37", size=24, color=ORANGE)
        input2.to_edge(UP, buff=0.6)
        self.play(Transform(input1, input2), run_time=0.6)
        self.wait(1.0)

        wedge2 = VGroup(*[d for d in rest1 if d.wedge_angle < SURVIVOR_START])
        survivors = [d for d in rest1 if d.wedge_angle >= SURVIVOR_START]
        self.play(FadeOut(wedge2), run_time=0.9)
        self.wait(1.3)

        winner = survivors[0]
        self.play(Indicate(winner, color=INK, scale_factor=2.2), run_time=1.0)
        self.wait(1.2)
        self.play(Indicate(winner, color=INK, scale_factor=1.8), run_time=0.9)
        self.wait(17.2)
