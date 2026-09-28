from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

import numpy as np
from manim import Create, FadeOut, Mobject, Scene, Transform, Wait, config

from kit import style, zones

ANIM_SHARE = 0.7
TIME_TOLERANCE = 0.05


class BoardMismatch(RuntimeError):
    pass


class TimingOverrun(RuntimeError):
    pass


@dataclass(frozen=True)
class Write:
    beat: str
    key: str
    build: Callable[[], Mobject]


@dataclass(frozen=True)
class Erase:
    beat: str
    key: str


@dataclass(frozen=True)
class Keep:
    beat: str
    key: str
    slot: int


Record = Write | Erase | Keep


@dataclass(frozen=True)
class Board:
    name: str
    beats: tuple[str, ...]
    records: tuple[Record, ...]
    previous: Board | None = None

    def __post_init__(self) -> None:
        for r in self.records:
            if r.beat not in self.beats:
                raise BoardMismatch(f"board {self.name}: record for unknown beat {r.beat!r}")
        order = [self.beats.index(r.beat) for r in self.records]
        if order != sorted(order):
            raise BoardMismatch(f"board {self.name}: records are not in beat order")

    def index(self, beat: str) -> int:
        if beat not in self.beats:
            raise BoardMismatch(f"board {self.name}: unknown beat {beat!r}")
        return self.beats.index(beat)

    def records_for(self, beat: str) -> tuple[Record, ...]:
        self.index(beat)
        return tuple(r for r in self.records if r.beat == beat)

    def records_before(self, beat: str) -> tuple[Record, ...]:
        i = self.index(beat)
        return tuple(r for r in self.records if self.beats.index(r.beat) < i)

    def records_through(self, beat: str) -> tuple[Record, ...]:
        i = self.index(beat)
        return tuple(r for r in self.records if self.beats.index(r.beat) <= i)


def _apply(record: Record, items: dict[str, Mobject]) -> None:
    if isinstance(record, Write):
        if record.key in items:
            raise BoardMismatch(f"{record.key!r} written twice")
        items[record.key] = record.build()
        return
    if record.key not in items:
        raise BoardMismatch(f"{record.key!r} is not on the board ({type(record).__name__} in {record.beat})")
    if isinstance(record, Erase):
        del items[record.key]
    else:
        items[record.key] = zones.to_kept(items[record.key], record.slot)


def replay(records: tuple[Record, ...]) -> dict[str, Mobject]:
    items: dict[str, Mobject] = {}
    for r in records:
        _apply(r, items)
    return items


def fingerprint(m: Mobject) -> tuple[float, float, float, float]:
    c = m.get_center()
    return (round(float(c[0]), 3), round(float(c[1]), 3), round(float(m.width), 3), round(float(m.height), 3))


def leaf_ids(mobjects) -> set[int]:
    return {id(x) for m in mobjects for x in m.get_family() if x.has_points()}


def signature(m: Mobject) -> tuple:
    """Geometry and style of every drawn leaf: what the next clip must reproduce exactly."""
    leaves = []
    for x in m.get_family():
        if not x.has_points():
            continue
        c = x.get_center()
        leaves.append((
            round(float(c[0]), 3), round(float(c[1]), 3), round(float(x.width), 3), round(float(x.height), 3),
            x.get_stroke_color().to_hex(), round(float(x.get_stroke_opacity()), 2),
            x.get_fill_color().to_hex(), round(float(x.get_fill_opacity()), 2),
        ))
    return tuple(leaves)


def _default_timing() -> Mapping[str, float]:
    import timing

    return timing.TIMING


class BeatScene(Scene):
    beat_id: str = ""
    board: Board | None = None
    timing: Mapping[str, float] | None = None

    def setup(self) -> None:
        if not self.beat_id or self.board is None:
            raise BoardMismatch(f"{type(self).__name__} needs beat_id and board")
        self.camera.background_color = style.BG
        timings = self.timing if self.timing is not None else _default_timing()
        if self.beat_id not in timings:
            raise BoardMismatch(f"no timing for beat {self.beat_id}")
        self.target = float(timings[self.beat_id])
        self.elapsed = 0.0
        self.frames = 0
        self._wipe: dict[str, Mobject] = {}
        if self.board.index(self.beat_id) == 0 and self.board.previous is not None:
            prev = self.board.previous
            self._wipe = replay(prev.records_through(prev.beats[-1]))
            self.add(*self._wipe.values())
        self.items = replay(self.board.records_before(self.beat_id))
        self.add(*self.items.values())
        self._pending = list(self.board.records_for(self.beat_id))

    @property
    def budget(self) -> float:
        return ANIM_SHARE * self.target

    def step(self, n: int) -> float:
        return self.budget / n

    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)  # Scene.wait() routes through play() too
        # Count frames the way Manim 0.21 writes them: a static wait writes int(d * fps)
        # frames, anything else writes len(arange(0, d, 1/fps)), i.e. rounds up.
        fps = config.frame_rate
        anims = self.animations or []
        frozen = len(anims) == 1 and isinstance(anims[0], Wait) and not self.should_update_mobjects()
        self.frames += int(self.duration * fps) if frozen else len(np.arange(0, self.duration, 1 / fps))
        self.elapsed = self.frames / fps

    def construct(self) -> None:
        if self._wipe:
            self.play(FadeOut(*self._wipe.values()), run_time=0.6)
            self._wipe = {}
        self.animate_beat()
        self._finish()

    def animate_beat(self) -> None:
        raise NotImplementedError

    def _take(self, kind: type, key: str) -> Record:
        for i, r in enumerate(self._pending):
            if isinstance(r, kind) and r.key == key:
                return self._pending.pop(i)
        raise BoardMismatch(f"{self.beat_id}: no pending {kind.__name__} record for {key!r}")

    def write(self, key: str, anim=Create, run_time: float = 1.0, **anim_kwargs) -> Mobject:
        record = self._take(Write, key)
        if key in self.items:
            raise BoardMismatch(f"{self.beat_id}: {key!r} written twice")
        m = record.build()
        self.play(anim(m, **anim_kwargs), run_time=run_time)
        self.add(m)  # animating sub-parts leaves a temporary group on screen; make m itself the top-level item
        self.items[key] = m
        return m

    def erase(self, *keys: str, run_time: float = 0.5) -> None:
        gone = []
        for key in keys:
            self._take(Erase, key)
            if key not in self.items:
                raise BoardMismatch(f"{self.beat_id}: {key!r} is not on the board")
            gone.append(self.items.pop(key))
        self.play(FadeOut(*gone), run_time=run_time)

    def keep(self, key: str, run_time: float = 0.8) -> None:
        record = self._take(Keep, key)
        m = self.items[key]
        target = zones.to_kept(m.copy(), record.slot)
        self.play(Transform(m, target), run_time=run_time)

    def _finish(self) -> None:
        if self._pending:
            left = ", ".join(f"{type(r).__name__}({r.key})" for r in self._pending)
            raise BoardMismatch(f"{self.beat_id}: records not performed: {left}")
        on_screen = leaf_ids(self.mobjects)
        expected = leaf_ids(self.items.values())
        if on_screen - expected:
            raise BoardMismatch(f"{self.beat_id}: stray mobjects on screen: {len(on_screen - expected)}")
        if expected - on_screen:
            raise BoardMismatch(f"{self.beat_id}: board items missing from screen")
        replayed = replay(self.board.records_through(self.beat_id))
        for key, m in self.items.items():
            if signature(m) != signature(replayed[key]):
                raise BoardMismatch(
                    f"{self.beat_id}: {key!r} changed in place (position, size, colour or opacity); "
                    "the next clip would replay the original. Make the change a board record."
                )
        remaining = self.target - self.elapsed
        if remaining < -TIME_TOLERANCE:
            raise TimingOverrun(f"{self.beat_id}: animations run {-remaining:.1f}s past the {self.target}s beat")
        fps = config.frame_rate
        pad = round(self.target * fps) - self.frames
        if pad > 0:
            self.wait((pad + 0.5) / fps)  # static wait writes int((pad + 0.5)) == pad frames
