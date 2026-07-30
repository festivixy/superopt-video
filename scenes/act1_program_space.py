import math
import random

from manim import UP, AnimationGroup, Create, Dot, FadeIn, Indicate, Succession, VGroup

from theme import DIM, INK, PROOF, VideoScene, mono, proof_check

CENTER = [0, -0.4, 0]


def ring(
    n: int, radius: float, opacity: float, dot_radius: float, gap_deg: float = 0, gap_center_deg: float = 90
) -> VGroup:
    dots = VGroup()
    gap_rad = math.radians(gap_deg)
    span = 2 * math.pi - gap_rad
    start = math.radians(gap_center_deg) + gap_rad / 2
    for i in range(n):
        angle = start + span * i / n
        pos = [CENTER[0] + radius * math.cos(angle), CENTER[1] + radius * math.sin(angle), 0]
        dots.add(Dot(point=pos, radius=dot_radius, color=DIM, fill_opacity=opacity))
    return dots


def scatter_cloud(n: int, r_min: float, r_max: float, seed: int) -> VGroup:
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(n):
        angle = rng.uniform(0, 2 * math.pi)
        radius = rng.uniform(r_min, r_max)
        t = (radius - r_min) / (r_max - r_min)
        opacity = max(0.02, 0.22 * (1 - t))
        pos = [CENTER[0] + radius * math.cos(angle), CENTER[1] + radius * math.sin(angle), 0]
        dots.add(Dot(point=pos, radius=0.025, color=DIM, fill_opacity=opacity))
    return dots


class TheSpaceOfPrograms(VideoScene):
    def construct(self) -> None:
        ring1 = ring(10, 1.0, opacity=0.9, dot_radius=0.06)
        ring2 = ring(40, 1.9, opacity=0.7, dot_radius=0.045)
        ring3 = ring(90, 2.9, opacity=0.35, dot_radius=0.03, gap_deg=100, gap_center_deg=90)
        cloud = scatter_cloud(28, 3.1, 3.9, seed=7)

        self.play(FadeIn(ring1, lag_ratio=0.05), run_time=1.0)
        self.play(FadeIn(ring2, lag_ratio=0.02), run_time=1.2)
        self.play(FadeIn(ring3, lag_ratio=0.01), run_time=1.4)
        self.play(FadeIn(cloud, lag_ratio=0.02), run_time=1.0)
        self.wait(1.4)

        self.play(
            Succession(*[Indicate(d, color=INK, scale_factor=1.8, run_time=0.18) for d in ring1]),
            run_time=1.8,
        )
        self.wait(0.6)
        self.play(
            AnimationGroup(*[Indicate(d, color=INK, scale_factor=1.5) for d in ring2], lag_ratio=0.05),
            run_time=2.2,
        )
        self.wait(1.6)

        winner = ring2[0]
        self.play(winner.animate.set_color(PROOF).scale(1.8), run_time=0.8)
        check = proof_check(size=0.35, color=PROOF)
        check.next_to(winner, UP, buff=0.25)
        self.play(Create(check), run_time=0.6)
        self.wait(16.0)
