# Whiteboard scenes: design (v3)

A complete redraw of the superopt explainer's Manim scenes for the v3 narration
script (67 beats, about 32 minutes). This replaces the v2 caption-free scenes.

## Goal

Every beat of the v3 script gets an animated scene that works like a good
teacher's whiteboard. The board holds the framework: definitions, worked
examples, the math, rules and results. It doesn't repeat the narration. Where
the story needs them, scenes also include diagrams and illustrations: me at a
desk coding, the book, a chess board, devices, the compiler, the solver.

The narration script is the source of truth for content and timing. Right now
it lives at `../video/script.md` in the superopt checkout, which is untracked;
see "Open item" at the end.

## Decisions

| Decision | Choice |
|---|---|
| Board style | Dark technical: near-black board, typeset math, clean diagrams |
| Illustration style | Monoline: same thin stroke as the diagrams, round caps, faint accent fills at most, drawn on with `Create` |
| Board behavior | Fills up within a Part, wiped at the start of the next Part |
| Scene structure | One Manim scene per beat, with board replay |
| Where it lives | `superopt-video` repo only, branch `v3-whiteboard` |

This supersedes `shots/visual-language.md` (v2, "no sentence on screen that the
voiceover can say"). The v3 rule: **the board shows the framework; the voice
tells the story.** Text on the board is allowed when it's durable content, like
a definition, a rule, a worked line, a label or a result. Text that restates a
narration sentence is still out.

## 1. Style kit (`kit/`)

### Palette

| Token | Hex | Meaning |
|---|---|---|
| `BG` | `#0E1116` | board |
| `INK` | `#ECECEC` | primary strokes and text |
| `DIM` | `#6E7681` | notes, place values, secondary labels |
| `BLUE` | `#58A6FF` | values and data (inputs, bit values) |
| `ORANGE` | `#FFB86B` | attention, questions, the thing being examined |
| `GREEN` | `#7EE787` | proven, passes, correct |
| `MAGENTA` | `#FF7EE3` | found by the solver (constants, counterexamples, wirings) |

Each color keeps its meaning across the whole video.

### Type

- **Serif** for board headings and notes: STIX Two Text.
- **Math** through `MathTex` (LaTeX via the installed MiKTeX), for example
  `2^{32}`, `\exists P\,\forall x`, `x \mathbin{\&} (x-1)`.
- **Monospace** for binary, code and assembly: JetBrains Mono.

Both font families are OFL-licensed. They ship in `assets/fonts/` and are
registered at import with `manimpango.register_font`, so renders don't depend on
system fonts.

### Board zones (1920×1080 frame)

| Zone | Where | Holds |
|---|---|---|
| `HEADLINE` | top-left strip | the Part's headline, written at the Part's first beat |
| `WORK` | left ~60% | the main worked example or diagram |
| `RULE` | top-right box | the definition or law being used |
| `NOTES` | bottom-right | asides, analogies, side facts |
| `KEPT` | bottom-left corner | results carried forward within the Part |

Zones are layout helpers (`zone(name)` returns an anchor point and a max size).
Scenes can span zones when a diagram needs the room.

### Monoline illustration kit (`kit/draw.py`)

One stroke width (3 px at 1080p), round caps and joins, `INK` strokes, accent
fill opacity ≤ 0.15. Each function returns a `VGroup` built from primitives or
hand-authored SVG paths.

- `person_seated()`, `person_standing()`, `person_pointing()`: me. Built as
  a rigged group (head, torso, arms, legs as separate paths) so arms can move
  to type or point.
- `desk()`, `chair()`, `laptop(callout_lines=None)`.
- `book(title="Hacker's Delight")`: our own cover design with a bit-pattern
  motif. It doesn't copy the real cover art. Can open to a spread.
- `chess_board(highlight=None)`: 8×8, pieces as dots, with an optional bitboard
  overlay.
- `phone()`, `browser_window()`, `chip()`.
- `compiler_machine()`: a machine that takes a program card and outputs one.
- `solver_box(label="Z3")`, `gate(label)`, `stopwatch()`.

### Board diagrams (`kit/board.py`)

- `register(n_bits, value, place_values=False)`: cells with optional
  128…1 labels above.
- `column_op(rows, op, carries=None, borrows=None)`: column-aligned binary
  or decimal arithmetic, with small borrow and carry arrows.
- `truth_table(op)`, `rule_box(lines)`, `bracket(target, label, side)`,
  `note(text)`.
- `program_card(lines)`: IR or assembly lines in a rounded card.
- `ladder(rows)`, `count_bars(values, log=True)`, `cegis_loop()`,
  `wiring_slots(n_lines, components)`, `scoreboard(rows)`, `timeline(ticks)`.

## 2. Scene architecture

### One scene per beat

`beats/part_N.py` holds one `BeatScene` subclass per script beat, named after
the beat id (`B_2_3`, `B_I_4`). Each renders to `renders/beats/<id>.mp4`.

### Board replay

`boards/part_N.py` defines the Part's board as an ordered list of `Write`
records: `(beat_id, key, builder, zone)`, plus `Move` (to `KEPT`) and `Erase`
records. `BeatScene.setup()` replays every record from earlier beats of the same
Part with no animation, so the frame starts exactly where the previous clip
ended. `construct()` then animates only this beat's own records. The first beat
of each Part starts blank and writes the headline.

### Timing

`tools/build_script.py`, ported from the scratch builder, parses `script.md` and
writes `timing.py` (`{beat_id: seconds}`). `BeatScene` spends about 70% of the
beat's time on its animations, scaled to fit, and holds the finished board for
the rest. After the voiceover is recorded, a real `timing.py` replaces the
estimate and only the beats whose length changed get re-rendered.

## 3. Render setup and checks

- Environment: `uv venv --python 3.12` in the repo (`venv/` is already
  ignored), then `uv pip install manim pytest`. Manim encodes through PyAV, so
  it doesn't need a system ffmpeg.
- `render.py preview <part|beat>` renders at low quality in parallel and joins
  the Part into `renders/part_N_preview.mp4`.
- `render.py final` renders every beat at 1080p60, plus the full joined cut.
- Checks (`tests/`, pytest):
  1. **Coverage:** every beat id in `script.md` has a scene, and every scene
     has a beat.
  2. **Duration:** each rendered clip is within ±0.5 s of `timing.py`.
  3. **Continuity:** for each Part, the board replayed up to beat *k* equals
     the board state at the end of beat *k−1* (same keys, same positions).
  4. **Facts:** numbers drawn on the board match the script's Sources list,
     asserted from one `facts.py` module that the scenes import.
- Visual review: after each Part renders, I pull stills and check overlap,
  cropping and readability, then hand over the joined preview.
- Commits go on `v3-whiteboard`, with no mention of Claude in any message. The
  v2 `scenes/` stay untouched until the new ones are approved.

## 4. Build order

| Phase | Scope | Gate |
|---|---|---|
| A · Foundation | env, fonts, kit, zones, board replay, timing, `render.py`, checks | smoke render |
| B · Pilot | Intro (I.1–I.9), Parts 1–2 | **review; the look is set here** |
| C | Parts 3–6 | preview review |
| D | Parts 7–8 | preview review |
| E | Parts 9–10 | preview review |
| F · Final | 1080p60, full cut, voiceover timing pass | full watch |

## 5. Board plan, beat by beat

Each entry lists what the board **adds**. Carried items say **kept**. Every
number comes from `facts.py`.

### Intro: "The summer of superopt"

- **I.1 Hi.** WORK: me at the desk draws on (person, chair, desk, laptop).
  RULE: a name card, "Curtis · high school", with two icons, `</>` and a game
  controller. Bottom: a `timeline` strip, May → Aug 2026, empty ticks.
- **I.2 Compilers.** A code card (`return x & (x-1);`) → `compiler_machine`
  → an instruction card (`lea`, `and`). An arrow is labeled "translate", and a
  second arrow under it "make fast". RULE: compiler = translator + optimizer.
- **I.3 Bit tricks.** The book draws on and opens. One page shows
  `0110 1100` as a register. NOTES: "bit tricks: shortcuts on the 1s and 0s".
- **I.4 One trick.** Two cards side by side: a loop card (check bit 0, 1, 2 …,
  "≤ 32 checks") and `x & (x − 1)` ("2 instructions"). NOTES: "why it works →
  Part 2".
- **I.5 The question.** The loop card goes into `compiler_machine`. The output
  slot shows an orange "2 instructions?". NOTES: "measured later →".
- **I.6 Games.** `chess_board` with pieces. The overlay lights the occupied
  squares as 1s in a 64-bit row. `b &= b − 1` steps: the lowest 1 disappears,
  and the matching piece pulses, three times. NOTES: "millions of times a
  second".
- **I.7 Scale.** `compiler_machine` labeled "clang" fans out to `phone`,
  `browser_window` and `laptop`. A multiplier line reads "× calls per second ×
  devices".
- **I.8 The bigger question.** WORK, the problem as math:
  `min |P|  such that  ∀x: P(x) = f(x)`. Two numbered lines: 1) find the
  shortest P, 2) prove nothing shorter.
- **I.9 The plan.** HEADLINE: "superoptimization (1987 →)". The timeline fills
  in: May 29 start, Jun 9 first search, Jun 17 synthesis, Jul 28 bug fixed, Jul
  29 compiler survey, Aug 12 done. The ticks act as the video's roadmap.

### Part 1: "98 vs 2"

- **1.1** WORK: the naive C card (from `assets/clear_lowest_bit.c`). Arrows
  label "check bit i", "switch it off", "x = 0 → 0".
- **1.2** A tall assembly card scrolls (from `assets/clang_clear_lowest_bit.s`).
  A box goes around one `mov / test / jne` group. RULE: "boxed group of 3, once per bit" and
  `32 × 3 + 2 = 98`. **Kept:** 98.
- **1.3** Assembly card: `lea eax, [rdi − 1]` / `and eax, edi`. `count_bars`:
  98 against 2. NOTES: "same result for all 2³² inputs".
- **1.4** Title card: "superopt", subtitle "the shortest program, proven".

### Part 2: "Numbers are rows of switches"

- **2.1** `register(8, 108, place_values=True)`. Math:
  `108 = 64 + 32 + 8 + 4`. NOTES: "real registers: 32 or 64 bits". **Kept:**
  108 row.
- **2.2** `column_op`: decimal `1000 − 1 = 0999` beside binary
  `0110 1100 − 1 = 0110 1011`, with borrow arrows in both. RULE: "−1: trailing
  0s → 1, lowest 1 → 0, rest unchanged".
- **2.3** `column_op` AND of 108 and 107. RULE: `truth_table(AND)`. Brackets:
  "above: same → kept", "at and below: a 0 → cleared". Result `0110 1000 = 104`.
- **2.4** The instruction-set card: the 11 ops in a grid. Definition:
  `length(P) = number of instructions`. Tick marks: `x − 1` → sub, `&` → and,
  giving 2.

### Part 3: "Programs, recipes, compilers"

- **3.1** A monoline machine with 3 stations; 6 → 12, 21 → 42. Label:
  "station = instruction", and a question mark over the station count.
- **3.2** Three machines (`x + x`, `x · 2`, `x ≪ 1`) on 7, 3, 10. Aside:
  `0000 0111 ≪ 1 = 0000 1110` next to decimal `42 → 420 (× 10)`. RULE:
  `x ≪ 1 = 2x`.
- **3.3** Recipes sorted by length: three 1-instruction recipes and one
  3-instruction recipe (`a = x·4, b = a − x, c = b − x`). An orange
  "shortest?".
- **3.4** A pass pipeline with rewrite rules (`x·2 → x≪1`, `y + 0 → y`, copy
  elimination). A fixed-point note: "no rule matches → stop". The loop card
  goes in, 98 comes out: "no rule for this loop".

### Part 4: "Search instead of rules"

- **4.1** Paper card: Massalin, 1987, "Superoptimizer: A Look at the Smallest
  Program". Strategy line: enumerate by length → test on inputs.
- **4.2** `ladder`: length 1 = 11 programs, length 2 = 385. RULE: "first match
  ⇒ shortest, since everything shorter was tried".
- **4.3** A stamp: "test ⇏ proof".

### Part 5: "Proof instead of testing"

- **5.1** Two machines, `x + x` and `x ≪ 1`; 7 → 14, 12 → 24.
- **5.2** Input grid with `2³² = 4,294,967,296`, `10⁶ / 2³² ≈ 0.023%`, two
  inputs `2⁶⁴ ≈ 1.8 × 10¹⁹`. A corner case in orange: `−(−2³¹) = −2³¹`.
- **5.3** Math: `2a + 2b = 2(a + b)`, so the sum is even, for every a and b.
- **5.4** RULE: "SAT: is there an assignment that makes the formula true?" A
  tiny example formula with an assignment. "SMT = SAT + arithmetic". Diagram:
  one 8-bit value fans into 8 wires, and an AND instruction becomes 8 AND
  gates.
- **5.5** Query card: `P₁(x) = x + x`, `P₂(x) = x ≪ 1`, assert
  `P₁(x) ≠ P₂(x)` → `solver_box` → green UNSAT ⇒ `∀x: P₁(x) = P₂(x)`.
- **5.6** Search tree: a contradiction produces a learned rule, and a whole
  subtree greys out, repeated. "Every region ruled out ⇒ UNSAT = proof".
- **5.7** `x + x` against `x ≪ 2` → orange SAT, witness `x = 1: 2 ≠ 4`.
  Summary box: UNSAT = proof, SAT = counterexample. **Kept:** summary box.

### Part 6: "The first result, then a wall"

- **6.1** `ladder` plus a checker. "8-bit: 256 inputs → run them all".
- **6.2** `0110 1100` → `0000 0100` ("keep only the lowest 1").
- **6.3** Program card: `t = −x`, `r = x & t`. "length 1: 11 tried, 0 work".
- **6.4** RULE: `−x = ~x + 1`. `column_op`: `0110 1100` flips to `1001 0011`,
  then +1 with the carry running to give `1001 0100`.
- **6.5** `column_op` AND of x and −x. Brackets: above → 0 (flipped), at → 1,
  below → 0. Result `0000 0100`. Green "minimum = 2".
- **6.6** `count_bars` on a log scale: 11, 385, 27,720, 3,381,840. NOTES: "each
  constant × 2³²".

### Part 7: "The smarter loop"

- **7.1** Math: `∃P ∀x: P(x) = f(x)`. NOTES: "asked directly: unknown (60 s
  limit)".
- **7.2** Split into two boxes: `∃P` over examples E, and a `∀x` check →
  counterexample → `E ∪ {x}`. The `cegis_loop` diagram. **Kept:** loop.
- **7.3** Run table, row 1: input `0xD82C07CD`, guess `0x88280288`, check ✗
  `0x0282A822`. Note: "only bits where x = 1 constrain C".
- **7.4** Rows 2–3: `0x8AAAAAAA` ✗ `0x20000000`, then `0xAAAAAAAA` ✓ UNSAT.
  Binary comparison of `0x8AAAAAAA` and `0xAAAAAAAA` with bit 29 circled.
- **7.5** The candidate space of 2³² constants, shrinking with each
  counterexample: 3 examples leave 1.
- **7.6** `x & □`. Math: `∃c ∀x: x & c = f(x)`. "c is an unknown".
- **7.7** `wiring_slots(3, [NEG, AND])`: line 0 = x. Unknowns: out(NEG),
  in(NEG), out(AND), in₁(AND), in₂(AND).
- **7.8** RULE: in < out, outs distinct, last line = answer, `in = ℓ ⇒
  value(in) = value(ℓ)`. Solved in magenta: NEG@1 reads 0, AND@2 reads 0 and 1
  → `x & −x`, 0.03 s.

### Part 8: "Can I trust my own proofs?"

- **8.1** Two gates: proof (encoder → Z3) and fuzzer (interpreter, 100,000
  random inputs), with "no shared code" between them. "count only if both
  pass". **Kept:** gates.
- **8.2** On `1001 0110`: LShR gives `0100 1011`, AShR gives `1100 1011`. A
  code note: in Z3 Python `>>` = arithmetic, `LShR()` = logical. "both sides
  wrong the same way → proof passes; fuzzer uses the interpreter → catches".
- **8.3** `y + ((x−y) & ((x−y) ≫ 31))`, with `x = INT_MIN, y = 1 → 1` (should
  be INT_MIN). The fuzzer gate lights up; the proof gate reads "n/a (needs a
  comparison)".
- **8.4** Floor proof for absval: 11 one-op bags + 66 two-op bags → all UNSAT ⇒
  minimum 3. A small green suite.
- **8.5** `stopwatch` reads 0.02 s. Orange: "hardest question → fastest?".
- **8.6** `n_lines = 4 = 100₂` goes into a 2-bit box, the top bit falls off,
  giving `00₂ = 0`. `ULT(var, 4)` becomes `ULT(var, 0)`.
- **8.7** "∀v: v <ᵤ 0 is false ⇒ always UNSAT". Fix: `loc_width = bits(n_lines)
  = 3`.
- **8.8** "1 input + 1 constant + 2 instructions = 4 lines". Affected floors:
  absval, isolate_rmb, times_nine. The "does not work" workaround gives
  `n_constants = 2` → 5 lines, which hid the bug.
- **8.9** Test card: `test_synthesizes_when_line_count_is_a_power_of_two` →
  expects a program → `x & (x − 1)` ✓.
- **8.10** Suite rerun with real timings, all floors still UNSAT. RULE: "a fast
  'no' gets checked".

### Part 9: "Back to the original question"

- **9.1** The 14 job names. Pipeline: naive spec → Python (superopt) and C
  (gcc, clang).
- **9.2** Assembly listing with every line except `ret` ticked. Tier ladder:
  proven 7, best found 4, upper bound 2, none 1.
- **9.3** `scoreboard`: clear_lowest_bit 18 / 98 / 2, smear_lowest_bit
  19 / 97 / 2, isolate_rmb 14 / 97 / 2, with a green "proven" on each 2.
- **9.4** GCC's loop structure against clang's 32 copies.
  `BLSR = x & (x − 1)` in one instruction; the v3 columns show gcc 16, clang 98,
  so it's unused.
- **9.5** Rotate: x86 `rol` 1–2 against superopt 3 (shl, lshr, or), proven.
  Byte swap: 2 against 9, upper bound.
- **9.6** `m = x ≫ₐ x`. Negative x: the shift is huge, so all 1s. Positive x:
  `x < 2ˣ`, so 0. Then `(x ⊕ m) − m = |x|`. 8-bit example: x = −5 =
  `1111 1011` → m = `1111 1111` → `0000 0100` → 5.
- **9.7** "x86: count mod 32". x = 32 → count 0 → m = 32 → −32. A boundary
  ring: proven inside the IR, broken on hardware.
- **9.8** The LLVM issue card, #212908, lifts off the top of the frame.

### Part 10: "Limits, credit, outro"

- **10.1** Popcount's SWAR masks (`0x55…`, `0x33…`, `0x0F…`). Round-time bars:
  0.06, 0.1, 3.9, 11, 27 s, then ∞.
- **10.2** Credits timeline: 1987 Massalin, CEGIS (Solar-Lezama), 2010 Jha,
  Gulwani, Seshia, Tiwari.
- **10.3** "What I built" list. Next: ML-guided search.
- **10.4** End card: `github.com/festivixy/superopt`, and me at the desk again.

## Out of scope

- Voiceover recording and final editing.
- Music and sound effects.
- Face-cam footage. It can still cut in on top; no scene depends on it.
- Changes to the superopt code itself.

## Open item

- Where the script lives. It's at `../video/script.md`, untracked in the
  superopt checkout. The plan is to move it to `script/script.md` in this repo
  so the scenes, `timing.py` and the checks all read one tracked copy. That
  needs the author's go-ahead, since it moves a file out of the superopt
  checkout.
