from manim import DOWN, RIGHT, AddTextLetterByLetter, Dot, FadeIn, FadeOut, Indicate, LaggedStart, RoundedRectangle, VGroup

from theme import BLUE, DIM, INK, MAGENTA, ORANGE, PROOF, VideoScene, mono, verdict

CHALLENGE_TEXT = "find one input where these differ"


def feed_challenge(scene: VideoScene, box: RoundedRectangle, type_it: bool, pulses: int) -> None:
    challenge = mono(CHALLENGE_TEXT, size=26, color=MAGENTA).move_to([0, 1.2, 0])
    if type_it:
        scene.play(AddTextLetterByLetter(challenge), run_time=1.6)
    else:
        scene.play(FadeIn(challenge), run_time=0.4)
    scene.wait(0.3)

    scene.play(challenge.animate.move_to(box.get_center()).scale(0.15).set_opacity(0), run_time=0.7)
    scene.remove(challenge)

    dots = VGroup(*[Dot(radius=0.08, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.35)
    dots.move_to([box.get_center()[0], box.get_center()[1] - 0.45, 0])
    scene.play(FadeIn(dots), run_time=0.3)
    for _ in range(pulses):
        scene.play(
            LaggedStart(*[Indicate(d, scale_factor=1.8, color=INK) for d in dots], lag_ratio=0.3),
            run_time=0.9,
        )
    scene.play(FadeOut(dots), run_time=0.3)


class TheDare(VideoScene):
    def construct(self) -> None:
        left_prog = mono("x + x", size=36, color=INK).move_to([-4, 2.3, 0])
        right_prog = mono("x << 1", size=36, color=INK).move_to([4, 2.3, 0])
        self.play(FadeIn(left_prog), FadeIn(right_prog), run_time=0.7)
        self.wait(0.6)

        box = RoundedRectangle(corner_radius=0.3, width=3.2, height=1.6, stroke_color=INK, stroke_width=2, fill_opacity=0)
        box.move_to([0, -0.7, 0])
        label = mono("Z3", size=34, color=INK).move_to(box.get_center())
        self.play(FadeIn(box), FadeIn(label), run_time=0.6)
        self.wait(0.5)

        feed_challenge(self, box, type_it=True, pulses=2)

        self.play(FadeOut(left_prog), FadeOut(right_prog), FadeOut(box), FadeOut(label), run_time=0.6)

        unsat = verdict("UNSAT", PROOF, size=90)
        self.play(FadeIn(unsat, scale=1.25), run_time=0.8)
        self.wait(4.1)

        self.play(FadeOut(unsat), run_time=0.6)

        right_prog2 = mono("x << 2", size=36, color=INK).move_to([4, 2.3, 0])
        self.play(FadeIn(left_prog), FadeIn(right_prog2), FadeIn(box), FadeIn(label), run_time=0.7)
        self.wait(0.5)

        feed_challenge(self, box, type_it=False, pulses=1)

        self.play(FadeOut(left_prog), FadeOut(right_prog2), FadeOut(box), FadeOut(label), run_time=0.6)

        sat = verdict("SAT", ORANGE, size=90).move_to([0, 0.6, 0])
        self.play(FadeIn(sat, scale=1.25), run_time=0.8)
        self.wait(0.5)

        witness = mono("x = 1   ->   2 vs 4", size=28, color=BLUE).next_to(sat, DOWN, buff=0.5)
        self.play(FadeIn(witness), run_time=0.5)
        self.wait(3.2)

        self.play(FadeOut(sat), FadeOut(witness), run_time=0.6)

        small_unsat = mono("UNSAT = proof", size=26, color=PROOF)
        small_sat = mono("SAT = witness", size=26, color=ORANGE)
        recap = VGroup(small_unsat, small_sat).arrange(RIGHT, buff=1.8)
        recap.move_to([0, 0, 0])
        drift = small_unsat[5].get_center()[1] - small_sat[3].get_center()[1]
        small_sat.shift([0, drift, 0])
        self.play(FadeIn(small_unsat), FadeIn(small_sat), run_time=0.7)
        self.wait(3.2)
