# Production timeline

Minute-by-minute map from the draft script (temp/drafts/script.md). Each
row is one scene to build; BUILT rows are done and rendered at 1080p60.
Durations are targets; final timing follows the recorded VO. Script cue
line numbers refer to draft 1; they shift after the author's rewrite but
the beats stay.

Status: 38 built / 0 to build / 41 total (standard accessibility trim
applied 2026-07-31: a3s5, a4s2, a5s8, a5s9 cut; a5s7 simplified; language
rule everywhere: no acronym spoken before its plain-words version, UNSAT
stays as the stamp, CEGIS on screen once as attribution only).

## Act 0 — Cold open (0:00-1:00)

| id | cue | scene | dur | status |
|---|---|---|---|---|
| a0s1 | L12-28 | TheScroll (C fades up, 98-line scroll, hard cut, the 2) | 0:45 | BUILT |
| a0s2 | L32 | Title card | 0:15 | BUILT |

## Act 1 — What a program is (1:00-4:30)

| id | cue | scene | dur | status |
|---|---|---|---|---|
| a1s1 | L40 | WhatIsAProgram (recipe card, numbers through) | 0:30 | BUILT |
| a1s2 | L46 | ManyRecipes (three programs, same outputs, shorter?) | 0:30 | BUILT |
| a1s3 | L52 | Recipes sorted by length | 0:25 | BUILT |
| a1s4 | L60-66 | Compiler as tidy-up editor; rule bag empties | 0:45 | BUILT |
| a1s5 | L70 | Massalin 1987 title beat | 0:20 | BUILT |
| a1s6 | L78 | The space of all short programs, one dot lights | 0:30 | BUILT |

## Act 2 — The impossible question (4:30-7:00)

| id | cue | scene | dur | status |
|---|---|---|---|---|
| a2s1 | L88 | Two programs, one input feeding both | 0:25 | BUILT |
| a2s2 | L94-100 | TheInputWall (grid, flashlight, missed dot) | 0:35 | BUILT |
| a2s3 | L104 | Even + even, reasoning without numbers | 0:25 | BUILT |
| a2s4 | L110-124 | TheDare (Z3, the dare, unsat, sat witness) | 0:45 | BUILT |

## Act 3 — Building the machine (7:00-13:00)

| id | cue | scene | dur | status |
|---|---|---|---|---|
| a3s1 | L134-140 | Ladder of lengths; rungs fill and clear | 0:40 | BUILT |
| a3s2 | L146 | 32-bit register, one bit survives | 0:25 | BUILT |
| a3s3 | L150 | x & -x rediscovered at length 2 | 0:30 | BUILT |
| a3s4 | L154 | Rungs exploding in size (combinatorial wall) | 0:25 | BUILT |
| a3s5 | L158 | Paper trail | — | CUT (folded into a5s10 attribution) |
| a3s6 | L162 | CEGIS loop diagram (theme component debut) | 0:40 | BUILT |
| a3s7 | L170 | Candidate space, slice vanishing per counterexample | 0:30 | BUILT |
| a3s8 | L176 | A program with a hole in it | 0:25 | BUILT |
| a3s9 | L184 | The hole fills: 0xAAAAAAAA | 0:30 | BUILT |
| a3s10 | L190 | Two gates, both must open (SMT + fuzzer) | 0:30 | BUILT |
| a3s11 | L196 | Wrong opcode: proof sails through, fuzzer catches | 0:35 | BUILT |

## Act 4 — The twist (13:00-17:00)

| id | cue | scene | dur | status |
|---|---|---|---|---|
| a4s1 | L206 | Green suite ticking | 0:25 | BUILT |
| a4s2 | L210 | The two halves of an optimality claim | — | CUT (merged into narration) |
| a4s3 | L214 | The 0.02s timer | 0:25 | BUILT |
| a4s4 | L222-252 | TheBitWrap (2-bit register, the wrap, false unsat, 3-bit sat) | 0:50 | BUILT |
| a4s5 | L248 | The "does not work" comment beat | 0:20 | BUILT |
| a4s6 | L256 | The regression test, positive direction | 0:25 | BUILT |
| a4s7 | L260-264 | Suite re-runs slowly; the lesson line | 0:35 | BUILT |

## Act 5 — Scoreboard and outro (17:00-21:30)

| id | cue | scene | dur | status |
|---|---|---|---|---|
| a5s1 | L274 | Fourteen benchmark names assemble | 0:20 | BUILT |
| a5s2 | L278-286 | TheScoreboard (bars, three benchmarks) | 0:35 | BUILT |
| a5s3 | L290 | The naive loop walking bit positions | 0:25 | BUILT |
| a5s4 | L296 | The honesty rows (rotl5, bswap32) | 0:30 | BUILT |
| a5s5 | L302 | The alien trick: ashr(x, x), only valid in the machine's own world | 0:30 | BUILT |
| a5s6 | L306 | The filed issue, styled | 0:20 | BUILT |
| a5s7 | L310-316 | What it still can't do (popcount, one simple beat) | 0:20 | BUILT |
| a5s8 | L316 | Three sweeps, different clocks | — | CUT (accessibility trim) |
| a5s9 | L320 | times_nine cost-model tangent | — | CUT (accessibility trim) |
| a5s10 | L324 | Attribution: 1987, 2006, 2010 | 0:20 | BUILT |
| a5s11 | L328 | 109 passed, 3 deselected | 0:15 | BUILT |
| a5s12 | L332 | Repo link, end | 0:15 | BUILT |

## Session plan

| session | minutes | scenes | count |
|---|---|---|---|
| A | 0:00-4:30 | a0s2, a1s3-a1s6 | DONE |
| B+C | 4:30-10:00 | a2s1, a2s3, a3s1-a3s4 | DONE |
| D | 10:00-13:00 | a3s6-a3s11 | DONE |
| E | 13:00-17:00 | a4s1, a4s3, a4s5, a4s6, a4s7 | DONE |
| F | 17:00-20:30 | a5s1, a5s3-a5s7, a5s10-a5s12 | DONE |

Rule: sessions run in order unless the author redirects; a session is done
when every scene in its minute range is final-rendered at 1080p60 and the
act plays as a sequence. Scene timing gets a final pass against recorded
VO during assembly.
