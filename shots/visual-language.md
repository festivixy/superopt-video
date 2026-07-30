# Visual language v2 — the screen shows, the voice tells

Adopted 2026-08-01 (director's note: the video is narrated; on-screen
sentences compete with the voiceover instead of supporting it).

## The rule

No sentence on screen that the voiceover can say. Meaning lives in
motion, structure, and data. If a caption restates narration, delete it
and, where the scene would go visually slack, replace it with a visual
beat that embodies the same idea.

## Text that stays (content, not caption)

- Code, programs, assembly, IR lines — they are the subject.
- Data: numbers, counts, timings, test names, benchmark names,
  `loc_width = 2`, `failing input: x = 19`, `109 passed, 3 deselected`.
- Proper names and artifacts: paper titles, the issue card's title and
  repo line, attribution lines.
- Iconic stamps and one-word motifs: the UNSAT/SAT verdicts, `proven`,
  the recurring ORANGE one-word question (`shorter?`), `2.`
- Title card and end card keep their text (cards are text by nature).

## Text that dies

Every multi-word caption whose meaning the narration carries:
explanatory sentences, morals, transitions, second DIM lines. Roughly
55 strings across the v1 scenes.

## Where deletions need a visual replacement

- act1_tidy_editor: after the bag empties, a ghost of a genuinely
  shorter program shimmers faintly beneath the compiler's final answer,
  unnoticed by the compiler box — the irony the caption used to state.
- act2_two_programs: an input counter spins into the millions while a
  progress bar toward 4,294,967,296 barely leaves zero.
- act3_ladder: the exhausted rung gets a lock/X seal before the winner
  glows — order carries the proof logic.
- act3_one_bit: a small crosshair motif finds and holds the lowest set
  bit instead of the task caption.
- act3_loop: the example stack visibly grows by exactly one per failed
  round; rounds counter ticks — teaching-by-counterexample shown, not
  said.
- act3_two_gates / act3_saboteur: gate labels stay (component names);
  moral captions die; the saboteur's rejected chip falls past a faint
  count of random inputs that caught it.
- act5_alien_trick: a boundary ring around the machine's world; inside
  it the program card glows PROOF; a copy sliding outside the ring
  loses its glow and cracks ORANGE — portability without a lecture.
- act5_filed_issue: the card lifts upward off the top of frame after
  its hold — upstream, literally.
- act4_timer: the ORANGE size-growth of `0.02s` carries the suspicion;
  the two caption lines die.
- act2_even_reasoning: the paired-dots merge and the morph to bits do
  the work; all three captions die.

## Enforcement

New scenes: no caption strings at all without a listed exemption.
Existing scenes: v2 cleanup tracked per scene in git history.

## v2.1 addendum — words may not be the protagonist (2026-08-01)

Killing captions is not enough: a scene whose main character is a word
(a text morph, a concept-word reveal) is still text doubling the voice.
When the subject is a concept, build a visual object for it and let the
object act:

- "What is a program" is not the words — it is a little machine: an
  input chute, visible internal stations that light in sequence, an
  output chute. A number token drops in, the stations tick, the doubled
  token drops out. The machine is the protagonist.
- The machine becomes a recurring character: programs are machines with
  their code on the faceplate; the compiler is a machine that rewrites
  machines; the search is a hall of candidate machines.
- Still allowed as text: code on faceplates, data, names, the iconic
  stamps and the single ORANGE question word, title/end/thesis cards.
- Banned: concept-word morphs, standalone nouns introducing ideas the
  narration already introduces.
