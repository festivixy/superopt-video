# Whiteboard Scenes: Foundation + Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the v3 scene foundation (style kit, board replay, script-driven
timing, render tooling, checks) and the pilot: the 17 beats of the Intro, Part 1
and Part 2, rendered into a preview for the author to review.

**Architecture:** A `kit/` package holds the palette, fonts, layout zones, board
diagrams and monoline illustrations. Each Part's persistent board content is an
ordered list of `Write` / `Erase` / `Keep` records in `boards/`. A `BeatScene`
replays earlier records instantly, animates its own, and refuses to finish if the
screen and the records disagree or the beat runs over its time. Durations come
from `script/script.md` through a generated `timing.py`.

**Tech Stack:** Python 3.12 (uv-managed venv), Manim Community ≥ 0.19 (Cairo
renderer, PyAV encoding), MiKTeX for `MathTex`, pytest, imageio-ffmpeg (joining
clips).

**Spec:** `docs/superpowers/specs/2026-09-28-whiteboard-scenes-design.md`

**Scope:** spec phases A and B only. Parts 3–10 (phases C–E) get their own plans
after the pilot review, because the spec makes the pilot the gate that sets the
look.

## Global Constraints

- Everything lives in the `superopt-video` repo, on branch `v3-whiteboard`. Nothing is committed to the superopt repo.
- Commit messages follow `<type>: <description>` and must not mention Claude anywhere.
- Palette (exact): BG `#0E1116`, INK `#ECECEC`, DIM `#6E7681`, BLUE `#58A6FF`, ORANGE `#FFB86B`, GREEN `#7EE787`, MAGENTA `#FF7EE3`.
- Fonts: serif "STIX Two Text", mono "JetBrains Mono", from `assets/fonts/`, registered with `manimpango.register_font`; math through `MathTex`.
- Monoline illustrations: one stroke width (`STROKE = 3`), round caps and joins where supported, accent fill opacity ≤ 0.15 (text glyphs excepted).
- One scene per beat, class name `B_` + the beat id with `.` replaced by `_` (`I.4` → `B_I_4`, `2.3` → `B_2_3`).
- `timing.py` is generated from `script/script.md` at 2.1 spoken words per second plus each beat's hold; `BeatScene` spends at most 70% (`ANIM_SHARE = 0.7`) of the beat on animation and holds the finished board for the rest.
- Clip length equals the beat's timing to within ±0.5 s.
- The v2 `scenes/` directory is left untouched.
- The book is drawn as our own cover design titled "Hacker's Delight", never a copy of the real cover art.

## Review Focus

- **Voiceover shorter than the animations.** A re-recorded beat that's shorter than its animations must fail loudly with `TimingOverrun`, naming the beat and the overrun, not render a clip that drifts out of sync. Pinned in Task 7.
- **A script beat renamed or added with no scene.** The coverage checks must fail and name the missing beat. Pinned in Tasks 2, 9, 10 and 11.
- **Fonts missing or registered under a different family name.** Pango silently substitutes a fallback font, so import must raise `FontError` instead. Pinned in Task 1.
- **Something left on screen that the board doesn't know about**, or a board item missing from the screen. The next clip would visibly jump, so the scene must raise `BoardMismatch`. Pinned in Task 7.
- **A board record the scene never performs.** The board file and the scene have drifted apart, so the scene must raise `BoardMismatch` listing the pending records. Pinned in Task 7.

---

## File structure

```
superopt-video/
  pyproject.toml              deps + pytest config
  script/script.md            narration (already moved here)
  timing.py                   GENERATED: {beat_id: seconds}
  facts.py                    every number/text drawn on the board, with sources
  render.py                   CLI: preview/final renders, joining clips
  kit/__init__.py
  kit/style.py                palette, font registration, text helpers
  kit/zones.py                board zones, fit(), kept slots
  kit/board.py                board diagrams (registers, column ops, cards, bars, timeline…)
  kit/draw.py                 monoline illustrations (desk scene, book, chess board, devices…)
  kit/beat.py                 Write/Erase/Keep records, Board, replay, BeatScene
  boards/__init__.py
  boards/intro.py             Intro board records (I.1–I.9)
  boards/part1.py             Part 1 board records (1.1–1.4)
  boards/part2.py             Part 2 board records (2.1–2.4)
  beats/__init__.py           registry of BeatScene classes
  beats/intro.py              B_I_1 … B_I_9
  beats/part1.py              B_1_1 … B_1_4
  beats/part2.py              B_2_1 … B_2_4
  tools/__init__.py
  tools/script_timing.py      script.md → timing.py
  tests/conftest.py           dry-run helper
  tests/test_style.py  tests/test_script_timing.py  tests/test_facts.py
  tests/test_zones.py  tests/test_board.py  tests/test_draw.py
  tests/test_beat.py  tests/test_render.py
  tests/test_beats_intro.py  tests/test_beats_part1.py  tests/test_beats_part2.py
  assets/fonts/               STIX Two Text + JetBrains Mono (.ttf, OFL.txt)
```

All commands run from `superopt-video/` in Git Bash. `PY` means
`venv/Scripts/python.exe`.

---

### Task 1: Environment, fonts, and the style module

**Files:**
- Create: `pyproject.toml`, `kit/__init__.py`, `kit/style.py`, `tests/conftest.py`, `tests/test_style.py`
- Create: `assets/fonts/STIXTwoText[wght].ttf`, `assets/fonts/STIXTwoText-OFL.txt`, `assets/fonts/JetBrainsMono[wght].ttf`, `assets/fonts/JetBrainsMono-OFL.txt`

**Interfaces:**
- Produces: `kit.style` constants `BG, INK, DIM, BLUE, ORANGE, GREEN, MAGENTA, SERIF, MONO, STROKE, FONT_DIR`; `FontError`; `register_fonts() -> None`; `serif(text: str, size: float = 32, color: str = INK, **kw) -> Text`; `mono(text: str, size: float = 28, color: str = INK, **kw) -> Text`; `math(tex: str, size: float = 40, color: str = INK) -> MathTex`. `tests/conftest.py` provides `render_dry(scene_cls) -> Scene`.

- [ ] **Step 1: Create the venv and project file**

```toml
# pyproject.toml
[project]
name = "superopt-video"
version = "0.3.0"
requires-python = ">=3.12,<3.13"
dependencies = ["manim>=0.19", "imageio-ffmpeg>=0.5"]

[project.optional-dependencies]
dev = ["pytest>=8"]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

Run:
```bash
uv venv --python 3.12 venv
uv pip install --python venv/Scripts/python.exe -r pyproject.toml --extra dev
venv/Scripts/python.exe -c "import manim, manimpango; print(manim.__version__)"
```
Expected: prints a version ≥ 0.19. If MiKTeX later pops up asking to install packages, allow it.

- [ ] **Step 2: Download the fonts (OFL, from the google/fonts repo)**

```bash
mkdir -p assets/fonts
curl -fL -o "assets/fonts/STIXTwoText[wght].ttf" "https://github.com/google/fonts/raw/main/ofl/stixtwotext/STIXTwoText%5Bwght%5D.ttf"
curl -fL -o assets/fonts/STIXTwoText-OFL.txt https://github.com/google/fonts/raw/main/ofl/stixtwotext/OFL.txt
curl -fL -o "assets/fonts/JetBrainsMono[wght].ttf" "https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
curl -fL -o assets/fonts/JetBrainsMono-OFL.txt https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/OFL.txt
ls -la assets/fonts
```
Expected: four files, both `.ttf` over 100 KB. (`-f` makes curl fail on a 404 instead of saving an HTML error page.)

- [ ] **Step 3: Write the failing tests**

```python
# tests/conftest.py
from __future__ import annotations

from manim import tempconfig


def render_dry(scene_cls):
    """Run a scene's construct without writing video; return the finished scene."""
    with tempconfig({"dry_run": True, "quality": "low_quality", "disable_caching": True}):
        scene = scene_cls()
        scene.render()
    return scene
```

```python
# tests/test_style.py
from __future__ import annotations

import manimpango
import pytest

from kit import style


def test_palette_is_exact():
    assert (style.BG, style.INK, style.DIM) == ("#0E1116", "#ECECEC", "#6E7681")
    assert (style.BLUE, style.ORANGE, style.GREEN, style.MAGENTA) == (
        "#58A6FF", "#FFB86B", "#7EE787", "#FF7EE3",
    )


def test_bundled_families_are_registered():
    families = set(manimpango.list_fonts())
    assert style.SERIF in families
    assert style.MONO in families


def test_missing_font_dir_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(style, "FONT_DIR", tmp_path)
    with pytest.raises(style.FontError, match="no .ttf"):
        style.register_fonts()


def test_wrong_family_raises(monkeypatch):
    monkeypatch.setattr(style, "REQUIRED_FAMILIES", ("No Such Family 123",))
    with pytest.raises(style.FontError, match="No Such Family 123"):
        style.register_fonts()


def test_text_helpers_build_visible_mobjects():
    assert style.serif("Hacker's Delight").width > 0
    assert style.mono("0110 1100").width > 0
    assert style.math(r"x \mathbin{\&} (x-1)").width > 0
```

- [ ] **Step 4: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_style.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'kit'`.

- [ ] **Step 5: Implement**

```python
# kit/__init__.py
```

```python
# kit/style.py
from __future__ import annotations

from pathlib import Path

import manimpango
from manim import MathTex, Text, config

BG = "#0E1116"
INK = "#ECECEC"
DIM = "#6E7681"
BLUE = "#58A6FF"
ORANGE = "#FFB86B"
GREEN = "#7EE787"
MAGENTA = "#FF7EE3"

SERIF = "STIX Two Text"
MONO = "JetBrains Mono"
REQUIRED_FAMILIES = (SERIF, MONO)
STROKE = 3

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"


class FontError(RuntimeError):
    pass


def register_fonts() -> None:
    files = sorted(FONT_DIR.glob("*.ttf"))
    if not files:
        raise FontError(f"no .ttf files in {FONT_DIR}")
    for path in files:
        manimpango.register_font(str(path))
    available = set(manimpango.list_fonts())
    missing = [family for family in REQUIRED_FAMILIES if family not in available]
    if missing:
        raise FontError(f"font families not available after registration: {missing}")


register_fonts()
config.background_color = BG


def serif(text: str, size: float = 32, color: str = INK, **kwargs) -> Text:
    return Text(text, font=SERIF, font_size=size, color=color, **kwargs)


def mono(text: str, size: float = 28, color: str = INK, **kwargs) -> Text:
    return Text(text, font=MONO, font_size=size, color=color, **kwargs)


def math(tex: str, size: float = 40, color: str = INK) -> MathTex:
    return MathTex(tex, font_size=size, color=color)
```

- [ ] **Step 6: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_style.py -v`
Expected: 5 passed. If `test_bundled_families_are_registered` fails, print `manimpango.list_fonts()` and look at the family name the file actually registers under. Fix `SERIF`/`MONO` to match, not the test.

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml kit/__init__.py kit/style.py tests/conftest.py tests/test_style.py assets/fonts
git commit -m "feat: style kit with bundled fonts and palette"
```

---

### Task 2: Script-driven timing

**Files:**
- Create: `tools/__init__.py`, `tools/script_timing.py`, `tests/test_script_timing.py`
- Generate: `timing.py`

**Interfaces:**
- Produces: `tools.script_timing.Beat(id: str, words: int, hold: float)`; `parse(text: str) -> list[Beat]`; `durations(beats: list[Beat], rate: float = RATE) -> dict[str, float]`; `module_source(d: dict[str, float]) -> str`; `main(argv: list[str] | None = None) -> int`. `timing.TIMING: dict[str, float]`, in script order.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_script_timing.py
from __future__ import annotations

import pytest

from tools import script_timing as st

SAMPLE = """# title

### I.1 · Hi
*~0:00 · 23s · 45 words*
**Scene:** face cam · hold 2s

> Hi, I'm Curtis. I like coding
> and games.

### 1.1 · The loop
**Scene:** `a0s1` · hold 4s

> Here's the loop.

## Sources for the numbers

### not.a.beat · ignored
**Scene:** x · hold 9s

> should not count
"""


def test_parse_reads_ids_words_and_holds_in_order():
    beats = st.parse(SAMPLE)
    assert [b.id for b in beats] == ["I.1", "1.1"]
    assert beats[0] == st.Beat("I.1", 8, 2.0)
    assert beats[1] == st.Beat("1.1", 3, 4.0)


def test_durations_use_rate_plus_hold():
    d = st.durations([st.Beat("I.1", 21, 2.0)], rate=2.1)
    assert d == {"I.1": 12.0}


def test_duplicate_beat_id_is_rejected():
    with pytest.raises(ValueError, match="duplicate beat id I.1"):
        st.parse(SAMPLE.replace("### 1.1 ·", "### I.1 ·"))


def test_beat_without_hold_is_rejected():
    with pytest.raises(ValueError, match="1.1.*hold"):
        st.parse(SAMPLE.replace("hold 4s", "no hold here"))


def test_beat_without_narration_is_rejected():
    with pytest.raises(ValueError, match="1.1.*narration"):
        st.parse(SAMPLE.replace("> Here's the loop.", ""))


def test_module_source_round_trips():
    namespace: dict = {}
    exec(st.module_source({"I.1": 12.0, "1.1": 5.4}), namespace)
    assert namespace["TIMING"] == {"I.1": 12.0, "1.1": 5.4}
    assert list(namespace["TIMING"]) == ["I.1", "1.1"]


def test_generated_timing_matches_the_script():
    import timing
    from pathlib import Path

    script = Path("script/script.md").read_text(encoding="utf-8")
    assert timing.TIMING == st.durations(st.parse(script))
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_script_timing.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'tools'`.

- [ ] **Step 3: Implement**

```python
# tools/__init__.py
```

```python
# tools/script_timing.py
"""Turn script/script.md into timing.py: {beat_id: seconds}, in script order."""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

RATE = 2.1  # spoken words per second, relaxed
HEAD = re.compile(r"^### (\S+) · .*$", re.M)
HOLD = re.compile(r"hold (\d+(?:\.\d+)?)s")
WORD = re.compile(r"[A-Za-z0-9'-]+")
END_OF_BEATS = "## Sources for the numbers"


@dataclass(frozen=True)
class Beat:
    id: str
    words: int
    hold: float


def parse(text: str) -> list[Beat]:
    body = text.split(END_OF_BEATS, 1)[0]
    pieces = HEAD.split(body)
    beats: list[Beat] = []
    seen: set[str] = set()
    for beat_id, block in zip(pieces[1::2], pieces[2::2]):
        if beat_id in seen:
            raise ValueError(f"duplicate beat id {beat_id}")
        seen.add(beat_id)
        hold = HOLD.search(block)
        if hold is None:
            raise ValueError(f"beat {beat_id} has no 'hold Ns' on its Scene line")
        narration = " ".join(
            line[1:].strip() for line in block.splitlines() if line.startswith(">")
        )
        if not narration:
            raise ValueError(f"beat {beat_id} has no narration lines")
        beats.append(Beat(beat_id, len(WORD.findall(narration)), float(hold.group(1))))
    return beats


def durations(beats: list[Beat], rate: float = RATE) -> dict[str, float]:
    return {b.id: round(b.words / rate + b.hold, 1) for b in beats}


def module_source(timing: dict[str, float]) -> str:
    lines = "".join(f"    {beat_id!r}: {seconds},\n" for beat_id, seconds in timing.items())
    return (
        "# Generated by tools/script_timing.py from script/script.md. Do not edit.\n"
        "TIMING: dict[str, float] = {\n" + lines + "}\n"
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    script = Path(args[0] if args else "script/script.md")
    out = Path(args[1] if len(args) > 1 else "timing.py")
    timing = durations(parse(script.read_text(encoding="utf-8")))
    out.write_text(module_source(timing), encoding="utf-8")
    print(f"wrote {len(timing)} beats to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Generate timing.py and run the tests**

Run:
```bash
venv/Scripts/python.exe -m tools.script_timing script/script.md timing.py
venv/Scripts/python.exe -m pytest tests/test_script_timing.py -v
```
Expected: `wrote 67 beats to timing.py`, then 7 passed.

- [ ] **Step 5: Commit**

```bash
git add tools timing.py tests/test_script_timing.py script/script.md
git commit -m "feat: generate beat timing from the narration script"
```

---

### Task 3: Facts module

**Files:**
- Create: `facts.py`, `tests/test_facts.py`

**Interfaces:**
- Produces: `facts.EXAMPLE = 108`, `EXAMPLE_MINUS_ONE = 107`, `EXAMPLE_AND = 104`, `CLANG_CLEAR_LOWEST_BIT = 98`, `TRICK_INSTRUCTIONS = 2`, `INPUT_BITS = 32`, `OPS: tuple[str, ...]` (11 names), `TIMELINE: tuple[tuple[str, str], ...]`, `C_SOURCE: str`, `CLANG_ASM_LINES: tuple[str, ...]` (the function body, stripped), `count_instructions(lines) -> int`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_facts.py
from __future__ import annotations

from pathlib import Path

import pytest

import facts


def test_example_arithmetic():
    assert facts.EXAMPLE == 64 + 32 + 8 + 4 == 0b01101100
    assert facts.EXAMPLE_MINUS_ONE == facts.EXAMPLE - 1 == 0b01101011
    assert facts.EXAMPLE_AND == facts.EXAMPLE & (facts.EXAMPLE - 1) == 0b01101000


def test_clang_count_follows_the_counting_rule():
    # every body instruction except ret, as in the superopt compiler-gap script
    assert facts.count_instructions(facts.CLANG_ASM_LINES) == facts.CLANG_CLEAR_LOWEST_BIT == 98
    assert 32 * 3 + 2 == facts.CLANG_CLEAR_LOWEST_BIT


def test_asm_lines_start_at_the_function_label():
    assert facts.CLANG_ASM_LINES[0] == "clear_lowest_bit:"
    assert facts.CLANG_ASM_LINES[1:4] == ("mov     eax, 1", "test    dil, 1", "jne     .LBB0_33")


def test_c_source_is_the_naive_loop():
    assert "for (int i = 0; i < 32; i++)" in facts.C_SOURCE
    assert "return x ^ (1u << i);" in facts.C_SOURCE


def test_eleven_ops():
    assert facts.OPS == ("add", "sub", "mul", "and", "or", "xor", "not", "neg", "shl", "lshr", "ashr")


def test_ops_match_superopt_ir_when_checked_out():
    ir = Path("../superopt/ir.py")
    if not ir.exists():
        pytest.skip("superopt checkout not next to superopt-video")
    text = ir.read_text(encoding="utf-8")
    for name in facts.OPS:
        assert f'= "{name}"' in text


def test_timeline_is_in_order():
    assert [d for d, _ in facts.TIMELINE] == ["May 29", "Jun 9", "Jun 17", "Jul 28", "Jul 29", "Aug 12"]
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_facts.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'facts'`.

- [ ] **Step 3: Implement**

```python
# facts.py
"""Every number and quoted text drawn on the board. Sources are in script/script.md."""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

EXAMPLE = 108
EXAMPLE_MINUS_ONE = 107
EXAMPLE_AND = 104
CLANG_CLEAR_LOWEST_BIT = 98  # results/asm/clang-clear_lowest_bit-base.s, clang 22.1.0 -O3
TRICK_INSTRUCTIONS = 2
INPUT_BITS = 32

OPS = ("add", "sub", "mul", "and", "or", "xor", "not", "neg", "shl", "lshr", "ashr")

TIMELINE = (
    ("May 29", "start"),
    ("Jun 9", "first search"),
    ("Jun 17", "synthesis"),
    ("Jul 28", "bug fixed"),
    ("Jul 29", "compiler survey"),
    ("Aug 12", "done"),
)

C_SOURCE = (ASSETS / "clear_lowest_bit.c").read_text(encoding="utf-8").strip("\n")


def _asm_body(path: Path) -> tuple[str, ...]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    start = lines.index("clear_lowest_bit:")
    return tuple(line for line in lines[start:] if line and not line.startswith("#"))


CLANG_ASM_LINES = _asm_body(ASSETS / "clang_clear_lowest_bit.s")


def count_instructions(lines: Iterable[str]) -> int:
    """Every body instruction except ret: skip labels and directives."""
    count = 0
    for line in lines:
        if line.endswith(":") or line.startswith("."):
            continue
        if line.split()[0] == "ret":
            continue
        count += 1
    return count
```

- [ ] **Step 4: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_facts.py -v`
Expected: 7 passed (or 6 passed, 1 skipped, if `../superopt` is missing).

- [ ] **Step 5: Commit**

```bash
git add facts.py tests/test_facts.py
git commit -m "feat: facts module with checked board numbers"
```

---

### Task 4: Board zones

**Files:**
- Create: `kit/zones.py`, `tests/test_zones.py`

**Interfaces:**
- Consumes: `kit.style`.
- Produces: `Zone(x, y, width, height)` with `.center`, `.left`, `.right`, `.top`, `.bottom`; `ZONES: dict[str, Zone]` with keys `HEADLINE, WORK, RULE, NOTES, KEPT, ART, SIDE, STRIP, CENTER`; `fit(m, zone: str, align: str = "center") -> Mobject` (align ∈ center, left, right, top, bottom, top_left); `KEPT_SLOTS = 3`; `kept_slot(i: int) -> Zone`; `to_kept(m, slot: int) -> Mobject`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_zones.py
from __future__ import annotations

import pytest
from manim import Rectangle

from kit import zones

EPS = 1e-6


def box(w, h):
    return Rectangle(width=w, height=h)


def inside(m, z):
    return (
        m.get_left()[0] >= z.left - EPS and m.get_right()[0] <= z.right + EPS
        and m.get_bottom()[1] >= z.bottom - EPS and m.get_top()[1] <= z.top + EPS
    )


@pytest.mark.parametrize("name", sorted(zones.ZONES))
def test_fit_puts_large_things_inside(name):
    m = zones.fit(box(40, 30), name)
    assert inside(m, zones.ZONES[name])


def test_fit_never_scales_up():
    m = zones.fit(box(0.5, 0.25), "WORK")
    assert m.width == pytest.approx(0.5)


@pytest.mark.parametrize("align", ["left", "right", "top", "bottom", "top_left"])
def test_alignments_touch_the_edge(align):
    z = zones.ZONES["SIDE"]
    m = zones.fit(box(1, 1), "SIDE", align=align)
    if "left" in align:
        assert m.get_left()[0] == pytest.approx(z.left)
    if align == "right":
        assert m.get_right()[0] == pytest.approx(z.right)
    if "top" in align:
        assert m.get_top()[1] == pytest.approx(z.top)
    if align == "bottom":
        assert m.get_bottom()[1] == pytest.approx(z.bottom)


def test_unknown_align_is_rejected():
    with pytest.raises(ValueError, match="align"):
        zones.fit(box(1, 1), "WORK", align="diagonal")


def test_kept_slots_are_disjoint_and_inside_kept():
    slots = [zones.kept_slot(i) for i in range(zones.KEPT_SLOTS)]
    for a, b in zip(slots, slots[1:]):
        assert a.right <= b.left + EPS
    k = zones.ZONES["KEPT"]
    assert slots[0].left >= k.left - EPS and slots[-1].right <= k.right + EPS


def test_to_kept_fits_the_slot_and_rejects_bad_slots():
    m = zones.to_kept(box(6, 2), 1)
    assert inside(m, zones.kept_slot(1))
    with pytest.raises(ValueError, match="slot"):
        zones.to_kept(box(1, 1), zones.KEPT_SLOTS)


def test_main_zones_do_not_overlap():
    names = ["HEADLINE", "WORK", "RULE", "NOTES", "KEPT"]
    zs = [zones.ZONES[n] for n in names]
    for i, a in enumerate(zs):
        for b in zs[i + 1:]:
            overlap_x = min(a.right, b.right) - max(a.left, b.left)
            overlap_y = min(a.top, b.top) - max(a.bottom, b.bottom)
            assert overlap_x <= EPS or overlap_y <= EPS
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_zones.py -v`
Expected: FAIL, `ImportError: cannot import name 'zones'`.

- [ ] **Step 3: Implement**

```python
# kit/zones.py
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Mobject


@dataclass(frozen=True)
class Zone:
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> np.ndarray:
        return np.array([self.x, self.y, 0.0])

    @property
    def left(self) -> float:
        return self.x - self.width / 2

    @property
    def right(self) -> float:
        return self.x + self.width / 2

    @property
    def top(self) -> float:
        return self.y + self.height / 2

    @property
    def bottom(self) -> float:
        return self.y - self.height / 2


# Frame is 14.22 x 8 units. Main zones do not overlap; ART/SIDE/STRIP/CENTER are
# alternative layouts used by illustration-heavy beats.
ZONES: dict[str, Zone] = {
    "HEADLINE": Zone(-2.5, 3.55, 8.6, 0.7),
    "WORK": Zone(-2.5, 0.2, 8.6, 5.6),
    "RULE": Zone(4.55, 2.05, 4.5, 3.0),
    "NOTES": Zone(4.55, -1.6, 4.5, 3.9),
    "KEPT": Zone(-2.5, -3.35, 8.6, 0.8),
    "ART": Zone(-4.0, 0.0, 5.4, 5.8),
    "SIDE": Zone(2.9, 0.3, 7.4, 5.6),
    "STRIP": Zone(0.0, -3.45, 13.6, 0.7),
    "CENTER": Zone(0.0, 0.0, 12.0, 6.5),
}

ALIGNS = ("center", "left", "right", "top", "bottom", "top_left")
KEPT_SLOTS = 3


def _fit_into(m: Mobject, z: Zone, align: str) -> Mobject:
    if align not in ALIGNS:
        raise ValueError(f"unknown align {align!r}; expected one of {ALIGNS}")
    factors = [1.0]
    if m.width > 0:
        factors.append(z.width / m.width)
    if m.height > 0:
        factors.append(z.height / m.height)
    scale = min(factors)
    if scale < 1.0:
        m.scale(scale)
    m.move_to(z.center)
    if "left" in align:
        m.align_to(np.array([z.left, 0.0, 0.0]), LEFT)
    if align == "right":
        m.align_to(np.array([z.right, 0.0, 0.0]), RIGHT)
    if "top" in align:
        m.align_to(np.array([0.0, z.top, 0.0]), UP)
    if align == "bottom":
        m.align_to(np.array([0.0, z.bottom, 0.0]), DOWN)
    return m


def fit(m: Mobject, zone: str, align: str = "center") -> Mobject:
    return _fit_into(m, ZONES[zone], align)


def kept_slot(i: int) -> Zone:
    if not 0 <= i < KEPT_SLOTS:
        raise ValueError(f"kept slot {i} out of range 0..{KEPT_SLOTS - 1}")
    k = ZONES["KEPT"]
    w = k.width / KEPT_SLOTS
    return Zone(k.left + w * (i + 0.5), k.y, w - 0.2, k.height)


def to_kept(m: Mobject, slot: int) -> Mobject:
    return _fit_into(m, kept_slot(slot), "center")
```

- [ ] **Step 4: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_zones.py -v`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add kit/zones.py tests/test_zones.py
git commit -m "feat: board zones with fit and kept slots"
```

---

### Task 5: Board diagrams

**Files:**
- Create: `kit/board.py`, `tests/test_board.py`

**Interfaces:**
- Consumes: `kit.style`, `kit.zones`.
- Produces:
  - `char_row(text: str, size: float = 34, color: str = INK, colors: Mapping[int, str] | None = None) -> VGroup`, with `.columns: dict[int, Text]` (text index → glyph; spaces have no entry) and `.digits: list[Text]` (left to right).
  - `column_op(rows: Sequence[tuple[str, str]], size: float = 34, rule_before_last: bool = True, colors: Mapping[tuple[int, int], str] | None = None) -> VGroup`, with `.rows: list[VGroup]` (char rows), `.labels`, `.rule`, and `.digit(row: int, k: int) -> Text` (k-th digit from the right, 0-based).
  - `borrow_marks(op: VGroup, row: int, ks: Sequence[int], color: str = ORANGE) -> VGroup`: a small arrow into digit k from digit k+1, for each k.
  - `register(value: int, n_bits: int = 8, cell: float = 0.62, place_values: bool = False, one_color: str = BLUE) -> VGroup`, with `.cells`, `.digits` (MSB first), `.places` (a `VGroup`, empty if not requested), `.bit(i) -> VGroup` (cell + digit for bit i, 0 = LSB).
  - `truth_table(op: str = "&", size: float = 28) -> VGroup` (four lines).
  - `rule_box(content: Mobject, pad: float = 0.3, color: str = DIM) -> VGroup`, with `.frame`, `.content`.
  - `note(text: str, size: float = 26, color: str = DIM) -> Text`.
  - `stack(*mobs, buff: float = 0.25) -> VGroup`: arranged DOWN, left-aligned.
  - `program_card(lines: Sequence[str], size: float = 26, colors: Mapping[int, str] | None = None, footer: Mobject | None = None) -> VGroup`, with `.frame`, `.lines` (keeps indentation).
  - `code_card(source: str, size: float = 22) -> VGroup`, with `.frame`, `.lines` (one entry per source line, blanks included as spacers).
  - `asm_wall(lines: Sequence[str], columns: int = 5, size: float = 13) -> VGroup`, with `.lines` (flat, in order).
  - `count_bars(rows: Sequence[tuple[str, int, str]], width: float = 6.0, size: float = 28) -> VGroup`, with `.bars`, `.labels`, `.values`.
  - `timeline(ticks: Sequence[tuple[str, str]], width: float = 12.0, size: float = 20) -> VGroup`, with `.axis`, `.ticks`.
  - `headline(text: str, size: float = 40) -> VGroup`, placed in the HEADLINE zone.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_board.py
from __future__ import annotations

import pytest

from kit import board, style, zones


def glyphs(row):
    return "".join(t.text for t in row.digits)


def test_char_row_keeps_columns_for_spaces():
    row = board.char_row("01 1")
    assert sorted(row.columns) == [0, 1, 3]
    gap = row.columns[3].get_x() - row.columns[1].get_x()
    step = row.columns[1].get_x() - row.columns[0].get_x()
    assert gap == pytest.approx(2 * step, rel=1e-3)


def test_register_shows_108_msb_first_and_colors_ones():
    reg = board.register(108, 8, place_values=True)
    assert glyphs(reg) == "01101100"
    assert [p.text for p in reg.places] == ["128", "64", "32", "16", "8", "4", "2", "1"]
    assert reg.bit(2)[1].text == "1"
    assert reg.bit(2)[1].get_color().to_hex().upper() == style.BLUE.upper()
    assert reg.bit(0)[1].text == "0"


def test_register_rejects_values_that_do_not_fit():
    with pytest.raises(ValueError, match="does not fit"):
        board.register(256, 8)


def test_column_op_right_aligns_rows_and_counts_digits_from_the_right():
    op = board.column_op([("x", "0110 1100"), ("− 1", "1"), ("", "0110 1011")])
    assert op.digit(1, 0).get_x() == pytest.approx(op.digit(0, 0).get_x())
    assert op.digit(0, 2).text == "1"
    assert op.digit(2, 2).text == "0"
    assert op.rule.get_y() > op.rows[2].get_y()


def test_borrow_marks_one_per_k():
    op = board.column_op([("", "1000"), ("− 1", "1"), ("", "0999")])
    marks = board.borrow_marks(op, 0, (2, 1, 0))
    assert len(marks) == 3


def test_truth_table_and():
    lines = board.truth_table("&")
    assert ["".join(t.text for t in l.digits) for l in lines] == ["1&1=1", "1&0=0", "0&1=0", "0&0=0"]


def test_program_card_keeps_indentation():
    card = board.program_card(["for i:", "  body"])
    assert card.lines[1].get_left()[0] > card.lines[0].get_left()[0]


def test_code_card_one_entry_per_source_line():
    src = "a\n\n  b"
    card = board.code_card(src)
    assert len(card.lines) == 3
    assert card.lines[2].get_left()[0] > card.lines[0].get_left()[0]


def test_asm_wall_keeps_order_across_columns():
    lines = [f"l{i}" for i in range(10)]
    wall = board.asm_wall(lines, columns=2)
    assert [m.text for m in wall.lines] == lines
    assert wall.lines[5].get_x() > wall.lines[4].get_x()


def test_count_bars_are_proportional():
    bars = board.count_bars([("a", 98, style.ORANGE), ("b", 2, style.GREEN)], width=6.0)
    assert bars.bars[0].width == pytest.approx(6.0)
    assert bars.bars[1].width == pytest.approx(max(0.06, 6.0 * 2 / 98))


def test_timeline_one_tick_per_entry_left_to_right():
    t = board.timeline([("May 29", "start"), ("Aug 12", "done")])
    assert len(t.ticks) == 2
    assert t.ticks[0].get_x() < t.ticks[1].get_x()


def test_headline_sits_in_its_zone():
    h = board.headline("numbers are rows of switches")
    z = zones.ZONES["HEADLINE"]
    assert h.get_left()[0] == pytest.approx(z.left)
    assert z.bottom - 1e-6 <= h.get_bottom()[1] and h.get_top()[1] <= z.top + 1e-6
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_board.py -v`
Expected: FAIL, `ImportError: cannot import name 'board'`.

- [ ] **Step 3: Implement**

```python
# kit/board.py
from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, CurvedArrow, Line, Mobject, Rectangle, RoundedRectangle,
    Square, Text, VGroup,
)

from kit import style, zones
from kit.style import BLUE, DIM, INK, ORANGE, STROKE

ADVANCE = 1.55  # monospace column step, in widths of a "0" glyph


def _advance(size: float) -> float:
    return style.mono("0", size).width * ADVANCE


def char_row(text: str, size: float = 34, color: str = INK,
             colors: Mapping[int, str] | None = None) -> VGroup:
    colors = colors or {}
    adv = _advance(size)
    row = VGroup()
    row.columns = {}
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        glyph = style.mono(ch, size, colors.get(i, color))
        glyph.move_to(np.array([i * adv, 0.0, 0.0]))
        row.columns[i] = glyph
        row.add(glyph)
    row.digits = [row.columns[i] for i in sorted(row.columns)]
    row.adv = adv
    return row


def column_op(rows: Sequence[tuple[str, str]], size: float = 34, rule_before_last: bool = True,
              colors: Mapping[tuple[int, int], str] | None = None) -> VGroup:
    colors = colors or {}
    width = max(len(digits) for _, digits in rows)
    adv = _advance(size)
    line_h = style.mono("0", size).height * 2.4
    group = VGroup()
    group.rows = []
    group.labels = VGroup()
    for r, (label, digits) in enumerate(rows):
        padded = digits.rjust(width)
        row_colors = {i: c for (rr, i), c in colors.items() if rr == r}
        row = char_row(padded, size, colors=row_colors)
        row.shift(np.array([0.0, -r * line_h, 0.0]))
        group.rows.append(row)
        group.add(row)
        if label:
            lab = style.mono(label, size * 0.8, DIM)
            lab.move_to(np.array([-adv * 1.2, -r * line_h, 0.0]), aligned_edge=RIGHT)
            group.labels.add(lab)
            group.add(lab)
    if rule_before_last and len(rows) > 1:
        y = -(len(rows) - 1.5) * line_h
        group.rule = Line(np.array([-adv * 0.6, y, 0.0]), np.array([(width - 0.4) * adv, y, 0.0]),
                          color=INK, stroke_width=STROKE)
        group.add(group.rule)
    else:
        group.rule = None

    def digit(row: int, k: int) -> Text:
        return group.rows[row].digits[-1 - k]

    group.digit = digit
    return group


def borrow_marks(op: VGroup, row: int, ks: Sequence[int], color: str = ORANGE) -> VGroup:
    marks = VGroup()
    for k in ks:
        src = op.digit(row, k + 1).get_top() + UP * 0.08
        dst = op.digit(row, k).get_top() + UP * 0.08
        marks.add(CurvedArrow(src, dst, angle=-PI / 2, color=color, stroke_width=STROKE * 0.8, tip_length=0.12))
    return marks


def register(value: int, n_bits: int = 8, cell: float = 0.62, place_values: bool = False,
             one_color: str = BLUE) -> VGroup:
    if not 0 <= value < (1 << n_bits):
        raise ValueError(f"{value} does not fit in {n_bits} bits")
    bits = format(value, f"0{n_bits}b")
    cells = VGroup(*[Square(side_length=cell, stroke_color=INK, stroke_width=STROKE * 0.7)
                     for _ in range(n_bits)]).arrange(RIGHT, buff=0)
    digits = VGroup()
    for sq, b in zip(cells, bits):
        digits.add(style.mono(b, cell * 55, one_color if b == "1" else INK).move_to(sq))
    places = VGroup()
    if place_values:
        for sq, p in zip(cells, range(n_bits - 1, -1, -1)):
            places.add(style.mono(str(1 << p), cell * 26, DIM).next_to(sq, UP, buff=0.12))
    reg = VGroup(cells, digits, places)
    reg.cells, reg.digits, reg.places = cells, digits, places

    def bit(i: int) -> VGroup:
        j = n_bits - 1 - i
        return VGroup(cells[j], digits[j])

    reg.bit = bit
    return reg


_TRUTH = {"&": lambda a, b: a & b, "|": lambda a, b: a | b, "^": lambda a, b: a ^ b}


def truth_table(op: str = "&", size: float = 28) -> VGroup:
    lines = VGroup()
    for a in (1, 0):
        for b in (1, 0):
            r = _TRUTH[op](a, b)
            lines.add(char_row(f"{a}{op}{b}={r}", size, colors={4: style.GREEN if r else DIM}))
    return lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18)


def rule_box(content: Mobject, pad: float = 0.3, color: str = DIM) -> VGroup:
    frame = RoundedRectangle(corner_radius=0.12, width=content.width + 2 * pad,
                             height=content.height + 2 * pad, stroke_color=color,
                             stroke_width=STROKE * 0.7).move_to(content)
    g = VGroup(frame, content)
    g.frame, g.content = frame, content
    return g


def note(text: str, size: float = 26, color: str = DIM) -> Text:
    return style.serif(text, size, color)


def stack(*mobs: Mobject, buff: float = 0.25) -> VGroup:
    return VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def _indented_lines(lines: Sequence[str], size: float, colors: Mapping[int, str],
                    t2c: Mapping[str, str] | None = None) -> VGroup:
    adv = _advance(size)
    line_h = style.mono("0", size).height * 1.9
    out = VGroup()
    for i, line in enumerate(lines):
        text = line.lstrip(" ")
        indent = len(line) - len(text)
        y = -i * line_h
        if text:
            m = style.mono(text, size, colors.get(i, INK), t2c=dict(t2c or {}))
            m.move_to(np.array([indent * adv, y, 0.0]), aligned_edge=LEFT)
        else:
            m = Rectangle(width=0.01, height=0.01, stroke_width=0, fill_opacity=0).move_to(np.array([0.0, y, 0.0]))
        out.add(m)
    return out


def _card(body: VGroup, footer: Mobject | None) -> VGroup:
    content = VGroup(body) if footer is None else VGroup(body, footer.next_to(body, DOWN, buff=0.3, aligned_edge=LEFT))
    frame = RoundedRectangle(corner_radius=0.15, width=content.width + 0.6, height=content.height + 0.5,
                             stroke_color=INK, stroke_width=STROKE * 0.7).move_to(content)
    card = VGroup(frame, content)
    card.frame = frame
    card.lines = body
    return card


def program_card(lines: Sequence[str], size: float = 26, colors: Mapping[int, str] | None = None,
                 footer: Mobject | None = None) -> VGroup:
    return _card(_indented_lines(lines, size, colors or {}), footer)


C_KEYWORDS = {"#include": DIM, "uint32_t": BLUE, "for": BLUE, "if": BLUE, "return": BLUE}


def code_card(source: str, size: float = 22) -> VGroup:
    return _card(_indented_lines(source.split("\n"), size, {}, t2c=C_KEYWORDS), None)


def asm_wall(lines: Sequence[str], columns: int = 5, size: float = 13) -> VGroup:
    per_col = -(-len(lines) // columns)
    cols = VGroup()
    flat: list[Text] = []
    for c in range(columns):
        chunk = lines[c * per_col:(c + 1) * per_col]
        if not chunk:
            break
        col = VGroup(*[style.mono(l, size, DIM if l.endswith(":") else INK) for l in chunk])
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cols.add(col)
        flat.extend(col)
    cols.arrange(RIGHT, aligned_edge=UP, buff=0.45)
    cols.lines = flat
    return cols


def count_bars(rows: Sequence[tuple[str, int, str]], width: float = 6.0, size: float = 28) -> VGroup:
    top = max(v for _, v, _ in rows)
    group = VGroup()
    group.bars, group.labels, group.values = VGroup(), VGroup(), VGroup()
    for i, (label, value, color) in enumerate(rows):
        y = -i * 0.9
        lab = style.mono(label, size, INK).move_to(np.array([-0.3, y, 0.0]), aligned_edge=RIGHT)
        bar = Rectangle(width=max(0.06, width * value / top), height=0.36, stroke_width=0,
                        fill_color=color, fill_opacity=0.9).move_to(np.array([0.0, y, 0.0]), aligned_edge=LEFT)
        num = style.mono(f"{value:,}", size, color).next_to(bar, RIGHT, buff=0.25)
        group.labels.add(lab)
        group.bars.add(bar)
        group.values.add(num)
        group.add(lab, bar, num)
    return group


def timeline(ticks: Sequence[tuple[str, str]], width: float = 12.0, size: float = 20) -> VGroup:
    axis = Line(np.array([-width / 2, 0.0, 0.0]), np.array([width / 2, 0.0, 0.0]),
                color=DIM, stroke_width=STROKE * 0.7)
    marks = VGroup()
    for i, (date, label) in enumerate(ticks):
        x = -width / 2 + width * (i + 0.5) / len(ticks)
        mark = Line(np.array([x, -0.12, 0.0]), np.array([x, 0.12, 0.0]), color=INK, stroke_width=STROKE)
        d = style.mono(date, size, BLUE).next_to(mark, UP, buff=0.1)
        t = style.serif(label, size, DIM).next_to(mark, DOWN, buff=0.1)
        marks.add(VGroup(mark, d, t))
    g = VGroup(axis, marks)
    g.axis, g.ticks = axis, marks
    return g


def headline(text: str, size: float = 40) -> VGroup:
    words = style.serif(text, size)
    underline = Line(LEFT, RIGHT, color=DIM, stroke_width=STROKE * 0.6)
    underline.set_width(words.width).next_to(words, DOWN, buff=0.08)
    return zones.fit(VGroup(words, underline), "HEADLINE", align="left")
```

- [ ] **Step 4: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_board.py -v`
Expected: all pass. If `t2c` isn't accepted by your Manim version's `Text`, drop the keyword coloring in `_indented_lines` (keep the parameter), and note it in the commit message.

- [ ] **Step 5: Commit**

```bash
git add kit/board.py tests/test_board.py
git commit -m "feat: board diagrams for registers, column math, cards and bars"
```

---

### Task 6: Monoline illustrations

**Files:**
- Create: `kit/draw.py`, `tests/test_draw.py`

**Interfaces:**
- Consumes: `kit.style`, `kit.board.register`.
- Produces: `desk_scene() -> VGroup` (attributes `.person` with `.forearm`, `.laptop`, `.desk`, `.chair`, `.book`); `book(title: str = "Hacker's Delight") -> VGroup`; `open_book(page: Mobject | None = None) -> VGroup`; `chess_board(size: float = 3.2, occupied: Sequence[int] = OCCUPIED) -> VGroup` (attributes `.squares` indexed 0–63, rank 0 at the bottom; `.pieces` in ascending square order; `.occupied`); `compiler_machine(label: str = "compiler", width: float = 2.6) -> VGroup`; `phone()`, `browser_window()`, `laptop_icon()`, `code_icon()`, `game_controller() -> VGroup`; `MAX_FILL = 0.15`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_draw.py
from __future__ import annotations

import pytest
from manim import Text

from kit import draw, style

BUILDERS = [
    draw.desk_scene, draw.book, draw.open_book, draw.chess_board, draw.compiler_machine,
    draw.phone, draw.browser_window, draw.laptop_icon, draw.code_icon, draw.game_controller,
]


def non_text_parts(m):
    if isinstance(m, Text):
        return []
    out = [m]
    for sub in m.submobjects:
        out.extend(non_text_parts(sub))
    return out


@pytest.mark.parametrize("build", BUILDERS, ids=lambda b: b.__name__)
def test_builds_something_visible(build):
    m = build()
    assert m.width > 0 and m.height > 0


@pytest.mark.parametrize("build", BUILDERS, ids=lambda b: b.__name__)
def test_monoline_rules(build):
    for part in non_text_parts(build()):
        if not part.has_points():
            continue
        assert part.get_fill_opacity() <= draw.MAX_FILL + 1e-9
        if part.get_stroke_opacity() > 0 and part.get_stroke_width() > 0:
            assert part.get_stroke_width() in (style.STROKE, style.STROKE * 0.7)


def test_desk_scene_exposes_parts():
    s = draw.desk_scene()
    for name in ("person", "laptop", "desk", "chair", "book"):
        assert getattr(s, name) in s.submobjects
    assert s.person.forearm in s.person.submobjects


def test_chess_board_geometry():
    b = draw.chess_board()
    assert len(b.squares) == 64
    assert b.squares[0].get_y() < b.squares[63].get_y()
    assert b.squares[0].get_x() < b.squares[7].get_x()
    assert len(b.pieces) == len(b.occupied)
    assert list(b.occupied) == sorted(b.occupied)


def test_book_title_is_ours():
    titles = [t.text for t in draw.book().get_family() if isinstance(t, Text)]
    joined = " ".join(titles)
    assert "Hacker's" in joined and "Delight" in joined
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_draw.py -v`
Expected: FAIL, `ImportError: cannot import name 'draw'`.

- [ ] **Step 3: Implement**

```python
# kit/draw.py
"""Monoline illustrations. Coordinates for the desk scene follow the approved
mockup (160x90 viewBox, y down) and are mapped to Manim units by _p."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, Circle, Line, Mobject, Polygon, Rectangle,
    RoundedRectangle, Square, Triangle, VGroup, VMobject,
)

from kit import style
from kit.board import register
from kit.style import BLUE, DIM, INK, ORANGE, STROKE

MAX_FILL = 0.15
S = 0.1
THIN = STROKE * 0.7
OCCUPIED = (3, 12, 21, 30, 42, 45, 52, 61)


def _round(m: VMobject) -> VMobject:
    try:
        from manim.constants import CapStyleType, LineJointType

        m.set_cap_style(CapStyleType.ROUND)
        m.joint_type = LineJointType.ROUND
    except (ImportError, AttributeError):
        pass
    return m


def _p(x: float, y: float) -> np.ndarray:
    return np.array([x * S, -y * S, 0.0])


def _line(*pts: tuple[float, float], color: str = INK, width: float = STROKE) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    m.set_points_as_corners([_p(*p) for p in pts])
    return _round(m)


def _curve(*pts: tuple[float, float], color: str = INK) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=STROKE, fill_opacity=0)
    m.set_points_smoothly([_p(*p) for p in pts])
    return _round(m)


def _outline(m: VMobject, color: str = INK, width: float = STROKE) -> VMobject:
    m.set_stroke(color=color, width=width)
    m.set_fill(opacity=0)
    return _round(m)


def desk_scene() -> VGroup:
    desk = VGroup(_line((8, 62), (82, 62)), _line((13, 62), (13, 86)), _line((77, 62), (77, 86)))
    chair = VGroup(_line((17, 38), (19, 65), (33, 65), color=DIM, width=THIN),
                   _line((26, 65), (26, 86), color=DIM, width=THIN),
                   _line((19, 65), (17, 86), color=DIM, width=THIN))
    head = _outline(Circle(radius=5.2 * S)).move_to(_p(30, 33))
    hair = _curve((25.5, 31), (27, 27.6), (31, 27.2), (34.2, 28.4), (35.3, 31.5))
    torso = _curve((29, 38.5), (28.3, 50), (29, 63))
    upper_arm = _line((29.5, 43), (37, 53))
    forearm = _line((37, 53), (49, 58.5))
    leg = _line((29, 63), (42, 64), (43, 82), (47, 82))
    person = VGroup(head, hair, torso, upper_arm, forearm, leg)
    person.forearm = forearm
    glow = Polygon(_p(61, 43), _p(64, 61.5), _p(57, 50), stroke_width=0, fill_color=BLUE, fill_opacity=0.12)
    laptop = VGroup(_line((46, 61.5), (64, 61.5)), _line((64, 61.5), (61, 43)), glow)
    book_small = VGroup(_line((67, 61.5), (79, 61.5), (79, 58), (67, 58), (67, 61.5), color=ORANGE, width=THIN),
                        _line((67, 59.7), (79, 59.7), color=ORANGE, width=THIN))
    scene = VGroup(chair, desk, person, laptop, book_small).move_to(ORIGIN)
    scene.person, scene.laptop, scene.desk, scene.chair, scene.book = person, laptop, desk, chair, book_small
    return scene


def book(title: str = "Hacker's Delight") -> VGroup:
    cover = _outline(RoundedRectangle(corner_radius=0.08, width=2.4, height=3.2))
    spine = Line(cover.get_corner(UP + LEFT) + RIGHT * 0.25, cover.get_corner(DOWN + LEFT) + RIGHT * 0.25,
                 stroke_color=DIM, stroke_width=THIN)
    first, _, rest = title.partition(" ")
    words = VGroup(style.serif(first, 30), style.serif(rest, 30)).arrange(DOWN, buff=0.08)
    words.move_to(cover.get_center() + UP * 0.6)
    squares = VGroup()
    for bit in "01101100":
        sq = Square(side_length=0.18, stroke_color=DIM, stroke_width=THIN,
                    fill_color=ORANGE, fill_opacity=MAX_FILL if bit == "1" else 0)
        squares.add(sq)
    squares.arrange(RIGHT, buff=0.04).move_to(cover.get_center() + DOWN * 0.7)
    return VGroup(cover, spine, words, squares)


def open_book(page: Mobject | None = None) -> VGroup:
    left = _outline(RoundedRectangle(corner_radius=0.06, width=2.6, height=3.2), width=THIN)
    right = left.copy().next_to(left, RIGHT, buff=0)
    lines = VGroup(*[Line(LEFT * 0.95, RIGHT * 0.95, stroke_color=DIM, stroke_width=THIN) for _ in range(7)])
    lines.arrange(DOWN, buff=0.28).move_to(left)
    spread = VGroup(left, right, lines)
    if page is not None:
        if page.width > 2.2:
            page.scale(2.2 / page.width)
        spread.add(page.move_to(right))
    return spread


def chess_board(size: float = 3.2, occupied: Sequence[int] = OCCUPIED) -> VGroup:
    cell = size / 8
    squares = VGroup()
    for i in range(64):
        rank, file = divmod(i, 8)
        dark = (rank + file) % 2 == 0
        sq = Square(side_length=cell, stroke_color=DIM, stroke_width=THIN,
                    fill_color=DIM, fill_opacity=0.12 if dark else 0)
        sq.move_to(np.array([(file - 3.5) * cell, (rank - 3.5) * cell, 0.0]))
        squares.add(sq)
    occ = tuple(sorted(occupied))
    pieces = VGroup(*[_outline(Circle(radius=cell * 0.28)).move_to(squares[i]) for i in occ])
    frame = _outline(Square(side_length=size))
    g = VGroup(squares, frame, pieces)
    g.squares, g.pieces, g.occupied = squares, pieces, occ
    return g


def compiler_machine(label: str = "compiler", width: float = 2.6) -> VGroup:
    h = width * 0.55
    body = _outline(RoundedRectangle(corner_radius=0.18, width=width, height=h))
    inlet = _outline(Triangle().scale_to_fit_height(h * 0.3).rotate(-np.pi / 2), width=THIN).move_to(body.get_left())
    outlet = inlet.copy().move_to(body.get_right())
    gears = VGroup(_outline(Circle(radius=h * 0.16), DIM, THIN), _outline(Circle(radius=h * 0.11), DIM, THIN))
    gears.arrange(RIGHT, buff=0.1).move_to(body.get_center() + UP * h * 0.15)
    name = style.serif(label, 24).move_to(body.get_center() + DOWN * h * 0.25)
    return VGroup(body, inlet, outlet, gears, name)


def phone() -> VGroup:
    body = _outline(RoundedRectangle(corner_radius=0.12, width=0.8, height=1.5))
    speaker = Line(LEFT * 0.12, RIGHT * 0.12, stroke_color=DIM, stroke_width=THIN).move_to(body.get_top() + DOWN * 0.15)
    return VGroup(body, speaker)


def browser_window() -> VGroup:
    body = _outline(RoundedRectangle(corner_radius=0.08, width=1.8, height=1.2))
    bar = Line(body.get_corner(UP + LEFT) + DOWN * 0.25, body.get_corner(UP + RIGHT) + DOWN * 0.25,
               stroke_color=DIM, stroke_width=THIN)
    dots = VGroup(*[_outline(Circle(radius=0.04), DIM, THIN) for _ in range(3)]).arrange(RIGHT, buff=0.06)
    dots.move_to(body.get_corner(UP + LEFT) + np.array([0.25, -0.13, 0.0]))
    return VGroup(body, bar, dots)


def laptop_icon() -> VGroup:
    screen = _outline(RoundedRectangle(corner_radius=0.06, width=1.5, height=0.95))
    base = _outline(Polygon(np.array([-0.95, 0, 0]), np.array([0.95, 0, 0]),
                            np.array([0.8, 0.12, 0]), np.array([-0.8, 0.12, 0])), width=THIN)
    base.next_to(screen, DOWN, buff=0.03)
    return VGroup(screen, base)


def code_icon() -> VGroup:
    ring = _outline(Circle(radius=0.45), DIM, THIN)
    glyph = style.mono("</>", 26, BLUE).move_to(ring)
    return VGroup(ring, glyph)


def game_controller() -> VGroup:
    body = _outline(RoundedRectangle(corner_radius=0.3, width=1.3, height=0.72))
    dpad = VGroup(Line(LEFT * 0.12, RIGHT * 0.12, stroke_color=INK, stroke_width=THIN),
                  Line(DOWN * 0.12, UP * 0.12, stroke_color=INK, stroke_width=THIN))
    dpad.move_to(body.get_center() + LEFT * 0.33)
    buttons = VGroup(_outline(Circle(radius=0.06), ORANGE, THIN), _outline(Circle(radius=0.06), BLUE, THIN))
    buttons.arrange(RIGHT, buff=0.1).move_to(body.get_center() + RIGHT * 0.33)
    return VGroup(body, dpad, buttons)
```

- [ ] **Step 4: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_draw.py -v`
Expected: all pass. If `test_monoline_rules` flags a stroke width, fix the builder, not the test.

- [ ] **Step 5: Commit**

```bash
git add kit/draw.py tests/test_draw.py
git commit -m "feat: monoline illustration kit"
```

---

### Task 7: Board records, replay, and BeatScene

**Files:**
- Create: `kit/beat.py`, `tests/test_beat.py`

**Interfaces:**
- Consumes: `kit.style`, `kit.zones`, the `timing` module (lazily).
- Produces: `Write(beat, key, build)`, `Erase(beat, key)`, `Keep(beat, key, slot)`; `Board(name, beats, records, previous=None)` with `.index(beat)`, `.records_for(beat)`, `.records_before(beat)`, `.records_through(beat)`; `replay(records) -> dict[str, Mobject]`; `fingerprint(m) -> tuple[float, float, float, float]`; `leaf_ids(mobjects) -> set[int]` (ids of every drawn shape in the mobjects' families; used for the on-screen check, because Manim regroups top-level mobjects when you animate part of one); `BoardMismatch`, `TimingOverrun`; `ANIM_SHARE = 0.7`; `BeatScene` (class attrs `beat_id: str`, `board: Board`, optional `timing: Mapping[str, float]`; instance `.items`, `.target`, `.elapsed`, `.budget`; methods `step(n) -> float`, `write(key, anim=Create, run_time=1.0, **kw) -> Mobject`, `erase(*keys, run_time=0.5)`, `keep(key, run_time=0.8)`, abstract `animate_beat()`).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_beat.py
from __future__ import annotations

import pytest
from manim import Circle, Dot, FadeIn, FadeOut, Square

from kit.beat import (
    Board, BoardMismatch, BeatScene, Erase, Keep, TimingOverrun, Write, fingerprint, leaf_ids, replay,
)
from tests.conftest import render_dry

A = Board("A", ("a1", "a2"), (
    Write("a1", "dot", lambda: Dot()),
    Write("a1", "sq", lambda: Square().shift([2, 0, 0])),
    Keep("a2", "sq", 0),
    Erase("a2", "dot"),
    Write("a2", "circle", lambda: Circle().shift([-2, 0, 0])),
))
B = Board("B", ("b1",), (Write("b1", "dot", lambda: Dot().shift([0, 1, 0])),), previous=A)
TIMES = {"a1": 3.0, "a2": 4.0, "b1": 2.0}


class A1(BeatScene):
    beat_id, board, timing = "a1", A, TIMES

    def animate_beat(self):
        self.write("dot", anim=FadeIn, run_time=0.5)
        self.write("sq", run_time=0.5)


class A2(BeatScene):
    beat_id, board, timing = "a2", A, TIMES

    def animate_beat(self):
        self.keep("sq")
        self.erase("dot")
        self.write("circle", run_time=0.5)


class B1(BeatScene):
    beat_id, board, timing = "b1", B, TIMES

    def animate_beat(self):
        self.write("dot", run_time=0.5)


def test_records_must_name_known_beats_in_order():
    with pytest.raises(BoardMismatch, match="unknown beat"):
        Board("X", ("x1",), (Write("zz", "k", Dot),))
    with pytest.raises(BoardMismatch, match="order"):
        Board("X", ("x1", "x2"), (Write("x2", "k", Dot), Write("x1", "j", Dot)))


def test_replay_applies_write_keep_erase():
    items = replay(A.records_through("a2"))
    assert sorted(items) == ["circle", "sq"]
    assert items["sq"].height <= 0.8 + 1e-6


def test_replay_rejects_double_write_and_missing_erase():
    with pytest.raises(BoardMismatch, match="written twice"):
        replay((Write("a1", "k", Dot), Write("a1", "k", Dot)))
    with pytest.raises(BoardMismatch, match="not on the board"):
        replay((Erase("a1", "k"),))


@pytest.mark.parametrize("cls", [A1, A2, B1])
def test_scene_ends_on_the_replayed_board_and_on_time(cls):
    scene = render_dry(cls)
    expected = replay(cls.board.records_through(cls.beat_id))
    assert {k: fingerprint(m) for k, m in scene.items.items()} == {
        k: fingerprint(m) for k, m in expected.items()
    }
    assert scene.elapsed == pytest.approx(TIMES[cls.beat_id], abs=0.05)


def test_first_beat_of_a_part_wipes_the_previous_board():
    scene = render_dry(B1)
    assert set(scene.items) == {"dot"}
    assert leaf_ids(scene.mobjects) == leaf_ids(scene.items.values())


def test_indicating_part_of_an_item_does_not_count_as_stray():
    class Pointy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            from manim import Indicate, LaggedStart, VGroup
            self.write("dot", run_time=0.5)
            sq = self.write("sq", run_time=0.5)
            self.play(LaggedStart(Indicate(sq), Indicate(self.items["dot"])), run_time=0.5)

    render_dry(Pointy)


def test_unperformed_record_raises():
    class Lazy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.5)

    with pytest.raises(BoardMismatch, match="sq"):
        render_dry(Lazy)


def test_record_not_on_the_board_raises():
    class Rogue(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("nope")

    with pytest.raises(BoardMismatch, match="nope"):
        render_dry(Rogue)


def test_stray_mobject_raises():
    class Messy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.5)
            self.write("sq", run_time=0.5)
            self.play(FadeIn(Circle()), run_time=0.2)

    with pytest.raises(BoardMismatch, match="stray"):
        render_dry(Messy)


def test_transient_mobject_removed_in_time_is_fine():
    class Tidy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.5)
            self.write("sq", run_time=0.5)
            tmp = Circle()
            self.play(FadeIn(tmp), run_time=0.2)
            self.play(FadeOut(tmp), run_time=0.2)

    render_dry(Tidy)


def test_overrun_raises_with_beat_and_amount():
    class Slow(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=2.5)
            self.write("sq", run_time=2.5)

    with pytest.raises(TimingOverrun, match=r"a1.*2\.0"):
        render_dry(Slow)


def test_missing_timing_raises():
    class NoTime(BeatScene):
        beat_id, board, timing = "a1", A, {"a2": 1.0}

        def animate_beat(self):
            pass

    with pytest.raises(BoardMismatch, match="no timing"):
        render_dry(NoTime)
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_beat.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'kit.beat'`.

- [ ] **Step 3: Implement**

```python
# kit/beat.py
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from manim import Create, FadeOut, Mobject, Scene, Transform

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
        super().play(*args, **kwargs)
        self.elapsed += self.duration  # Scene.wait() routes through play()

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
        remaining = self.target - self.elapsed
        if remaining < -TIME_TOLERANCE:
            raise TimingOverrun(f"{self.beat_id}: animations run {-remaining:.1f}s past the {self.target}s beat")
        if remaining > 0:
            self.wait(remaining)
```

- [ ] **Step 4: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_beat.py -v`
Expected: all pass. If `self.duration` doesn't exist in your Manim version, replace the `play` override's increment with `self.elapsed += self.renderer.time - before`, capturing `before = self.renderer.time` ahead of `super().play(...)`, and re-run.

- [ ] **Step 5: Commit**

```bash
git add kit/beat.py tests/test_beat.py
git commit -m "feat: board records, replay and the beat scene"
```

---

### Task 8: Render tooling

**Files:**
- Create: `render.py`, `beats/__init__.py` (empty registry for now), `tests/test_render.py`

**Interfaces:**
- Consumes: `timing.TIMING`.
- Produces: `render.PARTS: dict[str, tuple[str, str]]` (part name → (scene file, beat prefix)); `class_name(beat_id) -> str`; `beats_in_part(part) -> list[str]`; `manim_command(file, cls, mode) -> list[str]`; `output_path(file, cls, mode) -> Path`; `concat_list_text(paths) -> str`; `render_part(part, mode, workers=8) -> list[Path]`; `concat(paths, out) -> None`; `main(argv) -> int`. `beats.all_beats() -> dict[str, type[BeatScene]]`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_render.py
from __future__ import annotations

from pathlib import Path

import pytest

import render


def test_class_names():
    assert render.class_name("I.4") == "B_I_4"
    assert render.class_name("2.3") == "B_2_3"


def test_beats_in_part_follow_script_order():
    assert render.beats_in_part("intro") == [f"I.{i}" for i in range(1, 10)]
    assert render.beats_in_part("1") == ["1.1", "1.2", "1.3", "1.4"]


def test_unknown_part_is_rejected():
    with pytest.raises(ValueError, match="unknown part"):
        render.beats_in_part("99")


def test_manim_command_and_output_path():
    cmd = render.manim_command("beats/part2.py", "B_2_3", "preview")
    assert cmd[-2:] == ["beats/part2.py", "B_2_3"] and "-ql" in cmd
    assert render.output_path("beats/part2.py", "B_2_3", "preview").as_posix().endswith(
        "renders/media/videos/part2/480p15/B_2_3.mp4"
    )
    assert "1080p60" in render.output_path("beats/part2.py", "B_2_3", "final").as_posix()


def test_concat_list_escapes_quotes():
    text = render.concat_list_text([Path("a/b's.mp4")])
    assert text.strip() == "file '" + Path("a/b's.mp4").resolve().as_posix().replace("'", "'\\''") + "'"
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_render.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'render'`.

- [ ] **Step 3: Implement**

```python
# beats/__init__.py
from __future__ import annotations

import importlib

from kit.beat import BeatScene

MODULES = ("beats.intro", "beats.part1", "beats.part2")


def all_beats() -> dict[str, type[BeatScene]]:
    found: dict[str, type[BeatScene]] = {}
    for name in MODULES:
        module = importlib.import_module(name)
        for obj in vars(module).values():
            if isinstance(obj, type) and issubclass(obj, BeatScene) and obj is not BeatScene and obj.beat_id:
                if obj.beat_id in found:
                    raise ValueError(f"two scenes for beat {obj.beat_id}")
                found[obj.beat_id] = obj
    return found
```

```python
# render.py
"""Render beats. Usage:
    python render.py preview intro|1|2      low quality, joined into renders/<part>_preview.mp4
    python render.py final intro|1|2|all    1080p60, joined per part
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from timing import TIMING

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT / "renders" / "media"
PARTS: dict[str, tuple[str, str]] = {
    "intro": ("beats/intro.py", "I"),
    "1": ("beats/part1.py", "1"),
    "2": ("beats/part2.py", "2"),
}
MODES = {"preview": ("-ql", "480p15"), "final": ("-qh", "1080p60")}


def class_name(beat_id: str) -> str:
    return "B_" + beat_id.replace(".", "_")


def beats_in_part(part: str) -> list[str]:
    if part not in PARTS:
        raise ValueError(f"unknown part {part!r}; expected one of {sorted(PARTS)}")
    prefix = PARTS[part][1]
    return [b for b in TIMING if b.split(".")[0] == prefix]


def manim_command(file: str, cls: str, mode: str) -> list[str]:
    flag = MODES[mode][0]
    return [sys.executable, "-m", "manim", "render", flag, "--disable_caching",
            "--media_dir", str(MEDIA), file, cls]


def output_path(file: str, cls: str, mode: str) -> Path:
    return MEDIA / "videos" / Path(file).stem / MODES[mode][1] / f"{cls}.mp4"


def _render_one(file: str, cls: str, mode: str) -> Path:
    env = dict(os.environ, PYTHONPATH=str(ROOT))
    result = subprocess.run(manim_command(file, cls, mode), cwd=ROOT, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{cls} failed:\n{result.stderr[-3000:]}")
    out = output_path(file, cls, mode)
    if not out.exists():
        raise RuntimeError(f"{cls} rendered but {out} is missing")
    return out


def render_part(part: str, mode: str, workers: int = 8) -> list[Path]:
    file = PARTS[part][0]
    classes = [class_name(b) for b in beats_in_part(part)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda c: _render_one(file, c, mode), classes))


def concat_list_text(paths: list[Path]) -> str:
    return "".join("file '" + p.resolve().as_posix().replace("'", "'\\''") + "'\n" for p in paths)


def concat(paths: list[Path], out: Path) -> None:
    import imageio_ffmpeg

    out.parent.mkdir(parents=True, exist_ok=True)
    listing = out.with_suffix(".txt")
    listing.write_text(concat_list_text(paths), encoding="utf-8")
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
           "-i", str(listing), "-c", "copy", str(out)]
    subprocess.run(cmd, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=sorted(MODES))
    parser.add_argument("part", choices=sorted(PARTS) + ["all"])
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv)
    parts = list(PARTS) if args.part == "all" else [args.part]
    for part in parts:
        clips = render_part(part, args.mode, args.workers)
        out = ROOT / "renders" / f"{part}_{args.mode}.mp4"
        concat(clips, out)
        print(f"{part}: {len(clips)} beats -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run to verify pass**

Run: `venv/Scripts/python.exe -m pytest tests/test_render.py -v`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add render.py beats/__init__.py tests/test_render.py
git commit -m "feat: render tooling for per-beat clips and part previews"
```

---

### Task 9: Intro board and scenes (I.1–I.9)

**Files:**
- Create: `boards/__init__.py`, `boards/intro.py`, `beats/intro.py`, `tests/test_beats_intro.py`

**Interfaces:**
- Consumes: `kit.board`, `kit.draw`, `kit.style`, `kit.zones`, `kit.beat`, `facts`, `timing`.
- Produces: `boards.intro.BOARD: Board` (beats `I.1`–`I.9`); classes `B_I_1` … `B_I_9`. The final board through I.9 holds the keys `desk`, `timeline_axis`, `problem`, `headline`, `timeline_ticks`.

- [ ] **Step 1: Write the failing tests** (this file pattern repeats for Parts 1 and 2)

```python
# tests/test_beats_intro.py
from __future__ import annotations

from pathlib import Path

import pytest

import timing
from beats import all_beats
from kit.beat import fingerprint, replay
from tests.conftest import render_dry
from tools.script_timing import parse

PREFIX = "I"
SCRIPT_BEATS = [b.id for b in parse(Path("script/script.md").read_text(encoding="utf-8"))
                if b.id.split(".")[0] == PREFIX]


def test_every_script_beat_has_a_scene_and_board_slot():
    from boards.intro import BOARD

    assert list(BOARD.beats) == SCRIPT_BEATS
    registered = [b for b in all_beats() if b.split(".")[0] == PREFIX]
    assert sorted(registered) == sorted(SCRIPT_BEATS)


@pytest.mark.parametrize("beat_id", SCRIPT_BEATS)
def test_beat_ends_on_its_board_and_on_time(beat_id):
    cls = all_beats()[beat_id]
    scene = render_dry(cls)
    expected = replay(cls.board.records_through(beat_id))
    assert {k: fingerprint(m) for k, m in scene.items.items()} == {k: fingerprint(m) for k, m in expected.items()}
    assert scene.elapsed == pytest.approx(timing.TIMING[beat_id], abs=0.5)
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_beats_intro.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'boards'`.

- [ ] **Step 3: Implement the board**

```python
# boards/__init__.py
```

```python
# boards/intro.py
from __future__ import annotations

from manim import DOWN, RIGHT, Arrow, VGroup

import facts
from kit import board, draw, style, zones
from kit.beat import Board, Erase, Write
from kit.style import DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7", "I.8", "I.9")


def _arrow(a, b):
    return Arrow(a, b, buff=0.12, color=DIM, stroke_width=STROKE, max_tip_length_to_length_ratio=0.2)


def desk():
    return zones.fit(draw.desk_scene(), "ART")


def namecard():
    name = style.serif("Curtis", 60)
    role = style.serif("high school", 30, DIM)
    likes = VGroup(
        board.stack(draw.code_icon(), board.note("coding")),
        board.stack(draw.game_controller(), board.note("games")),
    ).arrange(RIGHT, buff=1.0)
    return zones.fit(VGroup(name, role, likes).arrange(DOWN, buff=0.4), "SIDE")


def _timeline():
    return zones.fit(board.timeline(facts.TIMELINE), "STRIP")


def timeline_axis():
    return _timeline().axis


def timeline_ticks():
    return _timeline().ticks


def compile_flow():
    src = board.program_card(["return x & (x - 1);"], size=24)
    machine = draw.compiler_machine()
    out = board.program_card(["lea eax, [rdi - 1]", "and eax, edi"], size=24)
    column = VGroup(src, machine, out).arrange(DOWN, buff=0.7)
    a1, a2 = _arrow(src.get_bottom(), machine.get_top()), _arrow(machine.get_bottom(), out.get_top())
    t1 = board.note("translate", color=INK).next_to(a1, RIGHT, buff=0.2)
    t2 = board.note("+ make it fast", color=ORANGE).next_to(a2, RIGHT, buff=0.2)
    rule = board.rule_box(board.stack(style.serif("compiler =", 28), style.serif("translator", 28),
                                      style.serif("+ optimizer", 28, ORANGE)))
    return zones.fit(VGroup(VGroup(column, a1, a2, t1, t2), rule).arrange(RIGHT, buff=0.9), "SIDE")


def book():
    return zones.fit(draw.open_book(board.register(facts.EXAMPLE, 8, cell=0.3)), "SIDE", align="top")


def bits_note():
    return zones.fit(board.note("bit tricks: shortcuts that work\ndirectly on the 1s and 0s"), "SIDE", align="bottom")


def loop_vs_trick():
    loop = board.program_card(["for i in 0..31:", "  if bit i of x is 1:", "    turn it off, return", "return 0"],
                              size=22, footer=board.note("≤ 32 checks"))
    trick = board.program_card(["x & (x - 1)"], size=30, footer=board.note("2 instructions", color=GREEN))
    return zones.fit(VGroup(loop, trick).arrange(RIGHT, buff=0.6, aligned_edge=DOWN), "SIDE", align="top")


def why_note():
    return zones.fit(board.note("why it works: Part 2"), "SIDE", align="bottom")


def question():
    loop = board.program_card(["for i in 0..31:", "  ..."], size=20)
    machine = draw.compiler_machine()
    ask = style.serif("2 instructions?", 34, ORANGE)
    row = VGroup(loop, machine, ask).arrange(RIGHT, buff=0.9)
    arrows = VGroup(_arrow(loop.get_right(), machine.get_left()), _arrow(machine.get_right(), ask.get_left()))
    return zones.fit(VGroup(row, arrows), "SIDE")


def later_note():
    return zones.fit(board.note("measured later in the summer"), "SIDE", align="bottom")


def chess():
    b = draw.chess_board()
    code = board.program_card(["b &= b - 1"], size=26)
    side = board.stack(code, board.note("millions of times\na second"), buff=0.5)
    return zones.fit(VGroup(b, side).arrange(RIGHT, buff=0.7), "SIDE")


def scale():
    clang = draw.compiler_machine(label="clang")
    devices = VGroup(draw.phone(), draw.browser_window(), draw.laptop_icon()).arrange(DOWN, buff=0.5)
    row = VGroup(clang, devices).arrange(RIGHT, buff=1.6)
    arrows = VGroup(*[_arrow(clang.get_right(), d.get_left()) for d in devices])
    mult = style.serif("× calls per second  × devices", 30, ORANGE).next_to(row, DOWN, buff=0.6)
    return zones.fit(VGroup(row, arrows, mult), "SIDE")


def problem():
    eq = style.math(r"\min\ |P| \quad \text{such that} \quad \forall x:\ P(x) = f(x)", 40)
    goals = board.stack(style.serif("1.  find the shortest P", 30), style.serif("2.  prove nothing shorter exists", 30))
    return zones.fit(board.stack(eq, goals, buff=0.7), "SIDE")


def headline():
    return board.headline("superoptimization  (1987 →)")


BOARD = Board("intro", BEATS, (
    Write("I.1", "desk", desk),
    Write("I.1", "namecard", namecard),
    Write("I.1", "timeline_axis", timeline_axis),
    Erase("I.2", "namecard"),
    Write("I.2", "compile_flow", compile_flow),
    Erase("I.3", "compile_flow"),
    Write("I.3", "book", book),
    Write("I.3", "bits_note", bits_note),
    Erase("I.4", "book"),
    Erase("I.4", "bits_note"),
    Write("I.4", "loop_vs_trick", loop_vs_trick),
    Write("I.4", "why_note", why_note),
    Erase("I.5", "loop_vs_trick"),
    Erase("I.5", "why_note"),
    Write("I.5", "question", question),
    Write("I.5", "later_note", later_note),
    Erase("I.6", "question"),
    Erase("I.6", "later_note"),
    Write("I.6", "chess", chess),
    Erase("I.7", "chess"),
    Write("I.7", "scale", scale),
    Erase("I.8", "scale"),
    Write("I.8", "problem", problem),
    Write("I.9", "headline", headline),
    Write("I.9", "timeline_ticks", timeline_ticks),
))
```

- [ ] **Step 4: Implement the scenes**

```python
# beats/intro.py
from __future__ import annotations

from manim import (
    DOWN, UP, Create, FadeIn, FadeOut, Indicate, LaggedStart, ReplacementTransform, Rotate, Write,
    there_and_back,
)

from boards.intro import BOARD
from kit import board, draw, style, zones
from kit.beat import BeatScene
from kit.style import ORANGE


class IntroBeat(BeatScene):
    board = BOARD

    def type_a_bit(self, run_time: float = 1.0) -> None:
        arm = self.items["desk"].person.forearm
        self.play(Rotate(arm, angle=0.12, about_point=arm.get_start(), rate_func=there_and_back), run_time=run_time)


class B_I_1(IntroBeat):
    beat_id = "I.1"

    def animate_beat(self):
        s = self.step(4)
        self.write("desk", run_time=2 * s)
        self.write("namecard", anim=FadeIn, run_time=s, shift=UP * 0.2)
        self.write("timeline_axis", run_time=s)


class B_I_2(IntroBeat):
    beat_id = "I.2"

    def animate_beat(self):
        s = self.step(5)
        self.erase("namecard")
        self.type_a_bit(run_time=s)
        self.write("compile_flow", run_time=3 * s)
        self.type_a_bit(run_time=s)


class B_I_3(IntroBeat):
    beat_id = "I.3"

    def animate_beat(self):
        s = self.step(5)
        self.erase("compile_flow")
        closed = zones.fit(draw.book(), "SIDE", align="top")
        self.play(Create(closed), run_time=2 * s)
        self.write("book", anim=lambda m: ReplacementTransform(closed, m), run_time=1.5 * s)
        self.write("bits_note", anim=FadeIn, run_time=s)


class B_I_4(IntroBeat):
    beat_id = "I.4"

    def animate_beat(self):
        s = self.step(6)
        self.erase("book", "bits_note")
        cards = self.write("loop_vs_trick", run_time=3 * s)
        self.play(Indicate(cards[1], color=ORANGE), run_time=s)
        self.write("why_note", anim=FadeIn, run_time=s)


class B_I_5(IntroBeat):
    beat_id = "I.5"

    def animate_beat(self):
        s = self.step(5)
        self.erase("loop_vs_trick", "why_note")
        q = self.write("question", run_time=3 * s)
        self.play(Indicate(q[0][2], color=ORANGE), run_time=s)
        self.write("later_note", anim=FadeIn, run_time=0.5 * s)


class B_I_6(IntroBeat):
    beat_id = "I.6"

    def animate_beat(self):
        s = self.step(8)
        self.erase("question", "later_note")
        item = self.write("chess", run_time=2 * s)
        grid = item[0]
        ones = [style.mono("1", 20, style.BLUE).move_to(grid.squares[i]) for i in grid.occupied]
        self.play(FadeIn(*ones), run_time=s)
        for k in range(3):
            self.play(Indicate(grid.pieces[k], color=ORANGE), ones[k].animate.set_color(ORANGE), run_time=0.6 * s)
            self.play(FadeOut(ones[k]), run_time=0.4 * s)
        self.play(FadeOut(*ones[3:]), run_time=0.5 * s)


class B_I_7(IntroBeat):
    beat_id = "I.7"

    def animate_beat(self):
        s = self.step(4)
        self.erase("chess")
        g = self.write("scale", run_time=2 * s)
        self.play(LaggedStart(*[Indicate(d) for d in g[0][1]], lag_ratio=0.3), run_time=s)


class B_I_8(IntroBeat):
    beat_id = "I.8"

    def animate_beat(self):
        s = self.step(4)
        self.erase("scale")
        self.write("problem", anim=Write, run_time=3 * s)


class B_I_9(IntroBeat):
    beat_id = "I.9"

    def animate_beat(self):
        s = self.step(4)
        self.write("headline", anim=Write, run_time=s)
        self.write("timeline_ticks", anim=lambda m: LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in m], lag_ratio=0.4),
                   run_time=2.5 * s)
```

- [ ] **Step 5: Run the tests**

Run: `venv/Scripts/python.exe -m pytest tests/test_beats_intro.py -v`
Expected: 10 passed. A `TimingOverrun` means that beat's `step(n)` split is too tight: raise `n`, don't change the timing. A `BoardMismatch` about stray mobjects means a transient wasn't faded out.

- [ ] **Step 6: Render the preview and look at it**

```bash
venv/Scripts/python.exe render.py preview intro
venv/Scripts/python.exe -c "
import imageio_ffmpeg, subprocess
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, '-y', '-loglevel', 'error', '-i', 'renders/intro_preview.mp4', '-vf', 'fps=1/4,scale=480:-1,tile=4x4', 'renders/intro_sheet_%02d.png'], check=True)"
```
Open each `renders/intro_sheet_*.png` and check: nothing overlaps or runs off the frame, text is readable, and the desk illustration reads as a person at a desk. Fix layout in `boards/intro.py` (sizes, `buff`, zone choice) and re-run Steps 5–6 until it's clean.

- [ ] **Step 7: Commit**

```bash
git add boards/__init__.py boards/intro.py beats/intro.py tests/test_beats_intro.py
git commit -m "feat: intro beats I.1 to I.9 on the whiteboard"
```

---

### Task 10: Part 1 board and scenes (1.1–1.4)

**Files:**
- Create: `boards/part1.py`, `beats/part1.py`, `tests/test_beats_part1.py`

**Interfaces:**
- Consumes: as Task 9, plus `boards.intro.BOARD` (as `previous`).
- Produces: `boards.part1.BOARD` (beats `1.1`–`1.4`, `previous=intro BOARD`); classes `B_1_1` … `B_1_4`. The final board holds only `title`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_beats_part1.py
from __future__ import annotations

from pathlib import Path

import pytest

import timing
from beats import all_beats
from kit.beat import fingerprint, replay
from tests.conftest import render_dry
from tools.script_timing import parse

PREFIX = "1"
SCRIPT_BEATS = [b.id for b in parse(Path("script/script.md").read_text(encoding="utf-8"))
                if b.id.split(".")[0] == PREFIX]


def test_every_script_beat_has_a_scene_and_board_slot():
    from boards.part1 import BOARD

    assert list(BOARD.beats) == SCRIPT_BEATS
    registered = [b for b in all_beats() if b.split(".")[0] == PREFIX]
    assert sorted(registered) == sorted(SCRIPT_BEATS)


@pytest.mark.parametrize("beat_id", SCRIPT_BEATS)
def test_beat_ends_on_its_board_and_on_time(beat_id):
    cls = all_beats()[beat_id]
    scene = render_dry(cls)
    expected = replay(cls.board.records_through(beat_id))
    assert {k: fingerprint(m) for k, m in scene.items.items()} == {k: fingerprint(m) for k, m in expected.items()}
    assert scene.elapsed == pytest.approx(timing.TIMING[beat_id], abs=0.5)
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_beats_part1.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'boards.part1'`.

- [ ] **Step 3: Implement the board**

```python
# boards/part1.py
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, Arrow, Line, SurroundingRectangle, VGroup

import facts
from boards.intro import BOARD as INTRO
from kit import board, style, zones
from kit.beat import Board, Erase, Keep, Write
from kit.style import BLUE, DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("1.1", "1.2", "1.3", "1.4")
C_NOTES = ((4, "check bit i"), (5, "switch it off"), (8, "x = 0  →  0"))


def headline():
    return board.headline("98 vs 2")


def c_code():
    return zones.fit(board.code_card(facts.C_SOURCE, size=24), "WORK", align="left")


def c_notes():
    card = c_code()
    notes = VGroup()
    for line_no, text in C_NOTES:
        line = card.lines[line_no]
        label = board.note(text, color=ORANGE).move_to([3.0, line.get_y(), 0], aligned_edge=LEFT)
        arrow = Arrow(label.get_left(), line.get_right() + RIGHT * 0.1, buff=0.1, color=ORANGE,
                      stroke_width=STROKE * 0.8, max_tip_length_to_length_ratio=0.12)
        notes.add(VGroup(arrow, label))
    return notes


def asm_wall():
    return zones.fit(board.asm_wall(facts.CLANG_ASM_LINES, columns=5, size=13), "WORK")


def asm_box():
    wall = asm_wall()
    return SurroundingRectangle(VGroup(*wall.lines[1:4]), color=ORANGE, buff=0.05, stroke_width=STROKE)


def asm_math():
    content = board.stack(board.note("boxed group of 3, once per bit", color=ORANGE),
                          style.math(r"32 \times 3 + 2 = 98", 44))
    return zones.fit(board.rule_box(content), "RULE")


def bars():
    rows = [("clang -O3", facts.CLANG_CLEAR_LOWEST_BIT, ORANGE), ("the trick", facts.TRICK_INSTRUCTIONS, GREEN)]
    return zones.fit(board.count_bars(rows, width=6.0), "WORK")


def two_asm():
    return zones.fit(board.program_card(["lea eax, [rdi - 1]", "and eax, edi"], size=26), "NOTES", align="top")


def same_note():
    g = board.stack(board.note("same result for every input"), style.math(r"x \in [0,\ 2^{32})", 34, BLUE))
    return zones.fit(g, "NOTES", align="bottom")


def title():
    name = style.serif("superopt", 110)
    underline = Line(LEFT, RIGHT, color=BLUE, stroke_width=STROKE)
    underline.set_width(name.width).next_to(name, DOWN, buff=0.1)
    sub = style.serif("the shortest program, proven", 34, DIM)
    return zones.fit(VGroup(name, underline, sub).arrange(DOWN, buff=0.3), "CENTER")


BOARD = Board("part1", BEATS, (
    Write("1.1", "headline", headline),
    Write("1.1", "c_code", c_code),
    Write("1.1", "c_notes", c_notes),
    Erase("1.2", "c_notes"),
    Keep("1.2", "c_code", 0),
    Write("1.2", "asm_wall", asm_wall),
    Write("1.2", "asm_box", asm_box),
    Write("1.2", "asm_math", asm_math),
    Erase("1.3", "asm_box"),
    Erase("1.3", "asm_wall"),
    Write("1.3", "bars", bars),
    Write("1.3", "two_asm", two_asm),
    Write("1.3", "same_note", same_note),
    Erase("1.4", "headline"),
    Erase("1.4", "c_code"),
    Erase("1.4", "asm_math"),
    Erase("1.4", "bars"),
    Erase("1.4", "two_asm"),
    Erase("1.4", "same_note"),
    Write("1.4", "title", title),
), previous=INTRO)
```

- [ ] **Step 4: Implement the scenes**

```python
# beats/part1.py
from __future__ import annotations

from manim import UP, Create, FadeIn, GrowFromEdge, Indicate, LaggedStart, Write, LEFT

from boards.part1 import BOARD
from kit.beat import BeatScene
from kit.style import ORANGE


class Part1Beat(BeatScene):
    board = BOARD


class B_1_1(Part1Beat):
    beat_id = "1.1"

    def animate_beat(self):
        s = self.step(6)
        self.write("headline", anim=Write, run_time=s)
        self.write("c_code", anim=FadeIn, run_time=2 * s, shift=UP * 0.2)
        self.write("c_notes", anim=lambda m: LaggedStart(*[Create(n) for n in m], lag_ratio=0.6), run_time=3 * s)


class B_1_2(Part1Beat):
    beat_id = "1.2"

    def animate_beat(self):
        s = self.step(7)
        self.erase("c_notes")
        self.keep("c_code")
        self.write("asm_wall", anim=lambda m: LaggedStart(*[FadeIn(l) for l in m.lines], lag_ratio=0.03),
                   run_time=3 * s)
        self.write("asm_box", run_time=s)
        self.write("asm_math", anim=Write, run_time=2 * s)


class B_1_3(Part1Beat):
    beat_id = "1.3"

    def animate_beat(self):
        s = self.step(6)
        self.erase("asm_box", "asm_wall")
        self.write("bars", anim=lambda m: LaggedStart(
            *[GrowFromEdge(b, LEFT) for b in m.bars], *[FadeIn(t) for t in [*m.labels, *m.values]], lag_ratio=0.2),
            run_time=2 * s)
        self.write("two_asm", anim=FadeIn, run_time=s)
        self.play(Indicate(self.items["bars"].bars[1], color=ORANGE), run_time=s)
        self.write("same_note", anim=FadeIn, run_time=s)


class B_1_4(Part1Beat):
    beat_id = "1.4"

    def animate_beat(self):
        s = self.step(4)
        self.erase("headline", "c_code", "asm_math", "bars", "two_asm", "same_note", run_time=s)
        self.write("title", anim=Write, run_time=2 * s)
```

- [ ] **Step 5: Run the tests**

Run: `venv/Scripts/python.exe -m pytest tests/test_beats_part1.py -v`
Expected: 5 passed.

- [ ] **Step 6: Render the preview and look at it**

```bash
venv/Scripts/python.exe render.py preview 1
venv/Scripts/python.exe -c "
import imageio_ffmpeg, subprocess
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, '-y', '-loglevel', 'error', '-i', 'renders/1_preview.mp4', '-vf', 'fps=1/4,scale=480:-1,tile=4x4', 'renders/1_sheet_%02d.png'], check=True)"
```
Check that the 98-line wall reads as a wall, that the boxed `mov / test / jne` group is visible, that the C card is legible in the kept corner, and that nothing overlaps. Fix the board file and re-run Steps 5–6 until it's clean.

- [ ] **Step 7: Commit**

```bash
git add boards/part1.py beats/part1.py tests/test_beats_part1.py
git commit -m "feat: part 1 beats, 98 vs 2"
```

---

### Task 11: Part 2 board and scenes (2.1–2.4)

**Files:**
- Create: `boards/part2.py`, `beats/part2.py`, `tests/test_beats_part2.py`

**Interfaces:**
- Consumes: as Task 9, plus `boards.part1.BOARD` (as `previous`).
- Produces: `boards.part2.BOARD` (beats `2.1`–`2.4`); classes `B_2_1` … `B_2_4`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_beats_part2.py
from __future__ import annotations

from pathlib import Path

import pytest

import timing
from beats import all_beats
from kit.beat import fingerprint, replay
from tests.conftest import render_dry
from tools.script_timing import parse

PREFIX = "2"
SCRIPT_BEATS = [b.id for b in parse(Path("script/script.md").read_text(encoding="utf-8"))
                if b.id.split(".")[0] == PREFIX]


def test_every_script_beat_has_a_scene_and_board_slot():
    from boards.part2 import BOARD

    assert list(BOARD.beats) == SCRIPT_BEATS
    registered = [b for b in all_beats() if b.split(".")[0] == PREFIX]
    assert sorted(registered) == sorted(SCRIPT_BEATS)


@pytest.mark.parametrize("beat_id", SCRIPT_BEATS)
def test_beat_ends_on_its_board_and_on_time(beat_id):
    cls = all_beats()[beat_id]
    scene = render_dry(cls)
    expected = replay(cls.board.records_through(beat_id))
    assert {k: fingerprint(m) for k, m in scene.items.items()} == {k: fingerprint(m) for k, m in expected.items()}
    assert scene.elapsed == pytest.approx(timing.TIMING[beat_id], abs=0.5)
```

- [ ] **Step 2: Run to verify failure**

Run: `venv/Scripts/python.exe -m pytest tests/test_beats_part2.py -v`
Expected: FAIL, `ModuleNotFoundError: No module named 'boards.part2'`.

- [ ] **Step 3: Implement the board**

```python
# boards/part2.py
from __future__ import annotations

from manim import DOWN, RIGHT, Brace, VGroup

import facts
from boards.part1 import BOARD as PART1
from kit import board, style, zones
from kit.beat import Board, Erase, Keep, Write
from kit.style import BLUE, DIM, GREEN, INK, ORANGE

BEATS = ("2.1", "2.2", "2.3", "2.4")


def headline():
    return board.headline("numbers are rows of switches")


def reg108():
    return zones.fit(board.register(facts.EXAMPLE, 8, cell=0.8, place_values=True), "WORK", align="top")


def sum108():
    return style.math(r"108 = 64 + 32 + 8 + 4", 44).next_to(reg108(), DOWN, buff=0.8)


def note_regs():
    return zones.fit(board.note("real registers hold\n32 or 64 bits"), "NOTES")


def sub_bin():
    op = board.column_op([("x", "0110 1100"), ("− 1", "1"), ("", "0110 1011")])
    return op.next_to(reg108(), DOWN, buff=0.9)


def borrow_bin():
    return board.borrow_marks(sub_bin(), 0, (1, 0))


def sub_dec():
    op = board.column_op([("", "1000"), ("− 1", "1"), ("", "0999")], size=28)
    marks = board.borrow_marks(op, 0, (2, 1, 0))
    label = board.note("decimal: borrow from the left")
    return zones.fit(board.stack(label, VGroup(op, marks), buff=0.4), "NOTES", align="top")


def minus_rule():
    content = board.stack(style.serif("x − 1:", 28), style.serif("trailing 0s → 1", 26),
                          style.serif("lowest 1 → 0", 26, ORANGE), style.serif("everything above: same", 26))
    return zones.fit(board.rule_box(content), "RULE")


def and_op():
    op = board.column_op([("x", "0110 1100"), ("x − 1", "0110 1011"), ("&", "0110 1000")])
    return op.next_to(reg108(), DOWN, buff=0.9)


def and_marks():
    op = and_op()
    above = VGroup(*[op.digit(2, k) for k in range(3, 8)])
    below = VGroup(*[op.digit(2, k) for k in range(0, 3)])
    b1, b2 = Brace(above, DOWN, color=BLUE), Brace(below, DOWN, color=ORANGE)
    t1 = board.note("same → kept", color=BLUE)
    t2 = board.note("a 0 → cleared", color=ORANGE)
    b1.put_at_tip(t1)
    b2.put_at_tip(t2)
    value = style.math(r"= 104", 40).next_to(op.rows[2], RIGHT, buff=0.5)
    return VGroup(b1, t1, b2, t2, value)


def and_table():
    return zones.fit(board.rule_box(board.stack(style.serif("AND: 1 only if both are 1", 26),
                                                board.truth_table("&"))), "RULE")


def isa():
    names = VGroup(*[style.mono(n, 24) for n in facts.OPS]).arrange_in_grid(rows=4, cols=3, buff=(0.5, 0.2))
    names.by_name = dict(zip(facts.OPS, names))
    box = board.rule_box(board.stack(style.serif("the 11 instructions I allow", 26), names))
    box.names = names.by_name
    return zones.fit(box, "RULE")


def length_def():
    return zones.fit(style.math(r"\text{length}(P) = \#\ \text{instructions in } P", 34), "NOTES", align="top")


def tally():
    card = board.program_card(["x - 1  →  sub", "x & …  →  and", "total  =  2"], size=24, colors={2: GREEN})
    return zones.fit(card, "NOTES", align="bottom")


BOARD = Board("part2", BEATS, (
    Write("2.1", "headline", headline),
    Write("2.1", "reg108", reg108),
    Write("2.1", "sum108", sum108),
    Write("2.1", "note_regs", note_regs),
    Erase("2.2", "note_regs"),
    Keep("2.2", "sum108", 0),
    Write("2.2", "sub_bin", sub_bin),
    Write("2.2", "borrow_bin", borrow_bin),
    Write("2.2", "sub_dec", sub_dec),
    Write("2.2", "minus_rule", minus_rule),
    Erase("2.3", "sub_dec"),
    Erase("2.3", "minus_rule"),
    Erase("2.3", "borrow_bin"),
    Erase("2.3", "sub_bin"),
    Write("2.3", "and_table", and_table),
    Write("2.3", "and_op", and_op),
    Write("2.3", "and_marks", and_marks),
    Erase("2.4", "and_marks"),
    Erase("2.4", "and_table"),
    Write("2.4", "isa", isa),
    Write("2.4", "length_def", length_def),
    Write("2.4", "tally", tally),
), previous=PART1)
```

- [ ] **Step 4: Implement the scenes**

```python
# beats/part2.py
from __future__ import annotations

from manim import UP, Create, FadeIn, Indicate, LaggedStart, Write

from boards.part2 import BOARD
from kit.beat import BeatScene
from kit.style import BLUE, ORANGE


class Part2Beat(BeatScene):
    board = BOARD


class B_2_1(Part2Beat):
    beat_id = "2.1"

    def animate_beat(self):
        s = self.step(7)
        self.write("headline", anim=Write, run_time=s)
        reg = self.write("reg108", anim=lambda m: LaggedStart(Create(m.cells), FadeIn(m.places), FadeIn(m.digits),
                                                               lag_ratio=0.5), run_time=2 * s)
        ones = [reg.bit(i)[1] for i in (6, 5, 3, 2)]
        self.play(LaggedStart(*[Indicate(d, color=BLUE) for d in ones], lag_ratio=0.3), run_time=s)
        self.write("sum108", anim=Write, run_time=2 * s)
        self.write("note_regs", anim=FadeIn, run_time=s)


class B_2_2(Part2Beat):
    beat_id = "2.2"

    def animate_beat(self):
        s = self.step(8)
        self.erase("note_regs")
        self.keep("sum108")
        self.write("sub_dec", anim=FadeIn, run_time=2 * s)
        self.write("sub_bin", anim=Write, run_time=2 * s)
        self.write("borrow_bin", run_time=s)
        self.write("minus_rule", anim=FadeIn, run_time=s, shift=UP * 0.2)


class B_2_3(Part2Beat):
    beat_id = "2.3"

    def animate_beat(self):
        s = self.step(7)
        self.erase("sub_dec", "minus_rule", "borrow_bin", "sub_bin")
        self.write("and_table", anim=FadeIn, run_time=s)
        op = self.write("and_op", anim=Write, run_time=2 * s)
        self.play(LaggedStart(*[Indicate(op.digit(2, k), color=ORANGE) for k in range(8)], lag_ratio=0.15),
                  run_time=s)
        self.write("and_marks", run_time=2 * s)


class B_2_4(Part2Beat):
    beat_id = "2.4"

    def animate_beat(self):
        s = self.step(6)
        self.erase("and_marks", "and_table")
        box = self.write("isa", anim=FadeIn, run_time=2 * s)
        self.write("length_def", anim=Write, run_time=s)
        self.write("tally", anim=FadeIn, run_time=s)
        self.play(Indicate(box.names["sub"], color=ORANGE), Indicate(box.names["and"], color=ORANGE), run_time=s)
```

- [ ] **Step 5: Run the tests**

Run: `venv/Scripts/python.exe -m pytest tests/test_beats_part2.py -v`
Expected: 5 passed.

- [ ] **Step 6: Render the preview and look at it**

```bash
venv/Scripts/python.exe render.py preview 2
venv/Scripts/python.exe -c "
import imageio_ffmpeg, subprocess
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, '-y', '-loglevel', 'error', '-i', 'renders/2_preview.mp4', '-vf', 'fps=1/4,scale=480:-1,tile=4x4', 'renders/2_sheet_%02d.png'], check=True)"
```
Check that the register's place values sit over the right cells, that the column math stays aligned with the register above it, that the braces point at the right digits (bits 0–2 against 3–7), and that the kept `108 = …` is readable. Fix the board file and re-run Steps 5–6 until it's clean.

- [ ] **Step 7: Commit**

```bash
git add boards/part2.py beats/part2.py tests/test_beats_part2.py
git commit -m "feat: part 2 beats, numbers as rows of switches"
```

---

### Task 12: Pilot cut and handoff for review

**Files:**
- Create: `renders/pilot_preview.mp4` (not committed; `renders/` is ignored)

- [ ] **Step 1: Run the whole suite**

Run: `venv/Scripts/python.exe -m pytest -v`
Expected: every test passes, with no skips except `test_ops_match_superopt_ir_when_checked_out` if the superopt checkout is missing.

- [ ] **Step 2: Join the three part previews into one pilot cut**

```bash
venv/Scripts/python.exe -c "
from pathlib import Path
import render
render.concat([Path('renders/intro_preview.mp4'), Path('renders/1_preview.mp4'), Path('renders/2_preview.mp4')],
              Path('renders/pilot_preview.mp4'))
print('ok')"
```
Expected: `ok`, and `renders/pilot_preview.mp4` plays through the Intro and Parts 1–2 (about 8½ minutes).

- [ ] **Step 3: Hand off**

Give the author the path to `renders/pilot_preview.mp4`, plus a short list of anything that still looks off. The pilot review decides the look for Parts 3–10, which get their own plans.
