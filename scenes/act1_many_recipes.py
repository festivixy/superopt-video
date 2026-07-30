from manim import DOWN, RIGHT, AnimationGroup, FadeIn, FadeOut, Indicate, TransformFromCopy, VGroup

from theme import BLUE, INK, ORANGE, PROOF, VideoScene, machine, mono

PROGRAM_TEXTS = ["x + x", "x * 2", "x << 1"]
ROW_Y = 1.9
TOP_Y = 3.3
BOTTOM_Y = 0.4
MACHINE_WIDTH = 1.9


def make_machines() -> VGroup:
    machines = VGroup(*[machine(code_lines=[t], width=MACHINE_WIDTH) for t in PROGRAM_TEXTS])
    machines.arrange(RIGHT, buff=0.9)
    machines.move_to([0, ROW_Y, 0])
    return machines


def feed(scene: VideoScene, machines: VGroup, in_val: int, out_val: int, pulse: bool, speed: float = 1.0) -> None:
    seed = mono(str(in_val), size=40, color=BLUE).move_to([0, TOP_Y, 0])
    scene.play(FadeIn(seed, shift=DOWN * 0.2), run_time=0.3 * speed)

    copies = VGroup(
        *[mono(str(in_val), size=34, color=BLUE).move_to([m.inlet.get_center()[0], TOP_Y, 0]) for m in machines]
    )
    scene.play(
        *[TransformFromCopy(seed, c) for c in copies],
        FadeOut(seed),
        run_time=0.4 * speed,
    )
    scene.play(*[FadeOut(c, shift=DOWN * 0.3) for c in copies], run_time=0.3 * speed)

    outputs = VGroup(
        *[mono(str(out_val), size=34, color=BLUE).move_to([m.outlet.get_center()[0], BOTTOM_Y, 0]) for m in machines]
    )
    scene.play(*[FadeIn(o, shift=DOWN * 0.2) for o in outputs], run_time=0.35 * speed)

    if pulse:
        scene.play(
            AnimationGroup(*[Indicate(o, color=PROOF) for o in outputs], lag_ratio=0.2),
            run_time=0.6 * speed,
        )

    scene.play(*[FadeOut(o) for o in outputs], run_time=0.3 * speed)


class ManyRecipes(VideoScene):
    def construct(self) -> None:
        machines = make_machines()
        self.play(FadeIn(machines, lag_ratio=0.2), run_time=0.9)
        self.wait(1.3)

        feed(self, machines, 7, 14, pulse=True, speed=1.4)
        self.wait(1.0)

        for in_val, out_val in ((3, 6), (10, 20), (255, 510)):
            feed(self, machines, in_val, out_val, pulse=True, speed=0.75)
            self.wait(0.4)

        self.wait(0.8)

        eq_left = mono("=", size=34, color=INK)
        eq_right = mono("=", size=34, color=INK)
        eq_left.move_to([(machines[0].get_center()[0] + machines[1].get_center()[0]) / 2, ROW_Y, 0])
        eq_right.move_to([(machines[1].get_center()[0] + machines[2].get_center()[0]) / 2, ROW_Y, 0])
        self.play(FadeIn(eq_left), FadeIn(eq_right), run_time=0.5)
        self.wait(0.5)

        chain = VGroup(machines[0], eq_left, machines[1], eq_right, machines[2])
        self.play(chain.animate.arrange(RIGHT, buff=0.45).move_to([0, 0.6, 0]), run_time=1.1)
        self.wait(3.2)

        shorter = mono("shorter?", size=30, color=ORANGE)
        shorter.move_to([5.0, -1.4, 0])
        self.play(FadeIn(shorter, scale=0.7), run_time=0.6)
        self.wait(4.0)
