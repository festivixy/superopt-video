# superopt: video script (v3, script-first)

An explainer told as the story of one summer, spoken by me. About 25 minutes.

This version goes deeper. Every idea gets a worked example, and the animation
gets re-timed to the narration instead of the other way round
(`superopt-video/shots/timeline.md` already says "final timing follows the
recorded VO").

**How to read it.** Each beat names the scene it plays over, using the ids from
`timeline.md`, and marks whether that scene exists, needs extending, or is new.
Start times are estimates from the word count at about 2.1 words a second, plus
the listed hold. Read slowly. The holds are where the animation carries the
idea.

**Every number is real.** Each one comes from the superopt repo or from running
its code; see **Sources** at the bottom.

**Pronunciation.** Z3 = "zee three". CEGIS = "SEE-giss". Massalin =
"MASS-a-lin". Solar-Lezama = "SO-lar le-ZAH-ma". Hex digits are read one at a
time ("hex A-A-A-A-A-A-A-A"). BLSR = "B-L-S-R".

---

## Animation work this script needs

**New scenes** (in the style of `shots/visual-language.md`: the screen shows,
the voice tells):

- **N1 Binary register** (2.1–2.3). An 8-switch register with place values 128
  … 1. 108 lights up as `01101100`. Subtract one: the borrow ripples to give
  `01101011`. Then the AND lines up both rows, column by column, into
  `01101000`. The register component in `theme.py` can probably do this.
- **N2 Bits into gates** (5.4). One 8-bit value splits into eight true/false
  wires. An AND instruction becomes a row of eight AND gates.
- **N3 Two's complement** (6.4–6.5). Extends `act3_x_and_negx.py`. Flip every
  bit, add one, and animate the carry running through the trailing 1s. Then the
  column-by-column AND.
- **N4 Wiring** (7.7–7.8). Lines 0, 1, 2 as slots. A NEG block and an AND block,
  each with unknown "writes to" and "reads from" numbers, snap into place.
- **N5 How I counted** (9.2), optional. Assembly listing with every line except
  `ret` ticked by a counter. Four tier labels: proven, best found, upper bound,
  no result.

**Scenes to change to real values:**

- `act3_loop.py` / `act3_fill.py` (7.3–7.4). Show the real run instead of the
  examples 3, 7, 12:
  - round 1: input `0xD82C07CD`, guess `0x88280288`, counterexample
    `0x0282A822`
  - round 2: guess `0x8AAAAAAA`, counterexample `0x20000000`
  - round 3: guess `0xAAAAAAAA`, unsat
- `act3_slice.py` (7.5). The failing inputs `x = 19` / `x = 37` are
  illustrative. Use `0x0282A822` and `0x20000000` to match.
- `act2_two_programs.py` (5.1). Inputs 7 and 12, as the narration says.

**Caption fixes still in the source** (`superopt-video/scenes/`):

1. `act5_honesty_rows.py:15`: `"best, not proven"` becomes `"upper bound"`.
2. `act5_honesty_rows.py:14`: rotate compiler count `"1"` is the v3 column; use
   `"2"` for baseline.
3. `act4_timer.py:10`: `"the hardest proof in the suite"` becomes `"the hardest
   kind of question"`.
4. `act5_suite.py:8`: rerun `pytest` and use the current count.

---

## Intro (new footage, I film this)

### I.1 · Hi
*~0:00 · 23s · 45 words*
**Scene:** face cam · hold 2s

> Hi, I'm Curtis. I'm a high schooler, and I like coding and games. This
> summer I built a project called superopt, and this video is the story of how
> it went, from the first idea to the mistakes to what I found at the end.

### I.2 · Compilers
*~0:23 · 26s · 49 words*
**Scene:** face cam, or film a short C file next to its assembly · hold 3s

> It started with reading about compilers. When you write code, the processor
> can't run it directly. A compiler translates it into the processor's own
> instructions, tiny steps like add, subtract and compare. A compiler also
> tries to make the result fast, and that part is what caught my attention.

### I.3 · Bit tricks
*~0:50 · 25s · 47 words*
**Scene:** film the *Hacker's Delight* cover or a page · hold 3s

> On the side, I was playing with bit tricks. Inside a computer, a number is
> stored as a row of 1s and 0s, and bit tricks are shortcuts that work
> directly on those 1s and 0s. The classic collection of them is a book called
> Hacker's Delight.

### I.4 · One trick
*~1:15 · 37s · 69 words*
**Scene:** film the loop version and the one-liner side by side · hold 4s

> Here's one of them. Say you want to take a number and switch off its lowest
> 1 bit. The obvious way is a loop: look at the bits one at a time until you
> find a 1, then switch it off. The book's version is x AND x minus one.
> There's no loop, and it takes two instructions. I'll show you exactly why it
> works in a few minutes.

### I.5 · The question
*~1:52 · 25s · 46 words*
**Scene:** face cam · hold 3s

> That's where the two things met. If a trick like that exists, does the
> compiler know it? If I write the slow loop, does the compiler swap in the
> two-instruction version on its own? Later in the summer I measured it, and
> the answer surprised me.

### I.6 · Why it matters: games
*~2:17 · 29s · 55 words*
**Scene:** film a chess board, then Stockfish's `pop_lsb` (`b &= b - 1`) · hold 3s

> This isn't only a puzzle, and games are a good example. Chess engines like
> Stockfish keep the board as 64-bit numbers, one bit for each square. To go
> through the pieces, they use this exact trick, x AND x minus one, over and
> over, millions of times a second while they search for a move.

### I.7 · Why it matters: scale
*~2:46 · 23s · 42 words*
**Scene:** film a phone, a laptop and a browser · hold 3s

> Compilers also work at a huge scale. Clang, one of the two big C compilers,
> builds iPhone apps, Android apps and Chrome. When a piece of code runs
> millions of times a second on billions of devices, one wasted instruction
> adds up.

### I.8 · The bigger question
*~3:09 · 21s · 38 words*
**Scene:** face cam · hold 3s

> So the question got bigger. Forget this one trick. For any small function,
> what's the shortest program that computes it? And could I prove that nothing
> shorter exists, for every possible input, including the ones I never tried?

### I.9 · The plan
*~3:30 · 24s · 44 words*
**Scene:** face cam, then cut to the animation · hold 3s

> That problem has a name, superoptimization, and people have been working on
> it since 1987. From the end of May to the middle of August, I built one.
> This video is how it works, what went wrong along the way, and what I found.

---

## Part 1: Ninety-eight versus two

### 1.1 · The obvious loop
*~3:54 · 30s · 55 words*
**Scene:** `a0s1` act0_cold_open.py (extend: hold on the C code) · hold 4s

> Let's start with that loop, written out in C. It checks bit zero, then bit
> one, and so on up to bit thirty-one. The first 1 it finds, it switches off
> and returns. If the number is zero, it returns zero. That's how most people
> would write it, and it's what I handed the compiler.

### 1.2 · What clang made
*~4:24 · 29s · 51 words*
**Scene:** `a0s1` act0_cold_open.py (the scroll) · hold 5s

> I gave this to clang with every optimization on, and this came out. Clang
> copied the check thirty-two times, once per bit. Each copy is three
> instructions: load the bit's value, test it, and jump out if it's set.
> Thirty-two times three is ninety-six, plus two at the end: ninety-eight
> instructions.

### 1.3 · The two
*~4:54 · 20s · 34 words*
**Scene:** `a0s1` act0_cold_open.py (the 2-instruction answer) · hold 4s

> And here's the trick from the book, as the processor sees it. Subtract one,
> then AND with the original. Two instructions, and the same answer for every
> one of the four billion possible inputs.

### 1.4 · Title
*~5:14 · 17s · 26 words*
**Scene:** `a0s2` act0_title.py · hold 5s

> That gap, ninety-eight against two, is what this project is about. Superopt
> finds answers like the two on its own, and then proves there's nothing
> shorter.

---

## Part 2: Numbers are rows of switches

### 2.1 · Binary
*~5:31 · 43s · 83 words*
**Scene:** N1 (new) · hold 3s

> To see why the trick works, you have to look at numbers the way the
> processor does: as a row of switches, each one on or off, 1 or 0. Each
> position is worth double the one to its right: one, two, four, eight, and so
> on. A hundred and eight is sixty-four plus thirty-two plus eight plus four,
> so it reads 0 1 1 0 1 1 0 0. Real registers have thirty-two or sixty-four
> switches. I'll use eight so it fits.

### 2.2 · Subtracting one
*~6:14 · 31s · 58 words*
**Scene:** N1 (new) · hold 3s

> Now subtract one. It works like subtracting one from a thousand in decimal:
> you borrow from the left. The 0s at the right end turn into 1s, the lowest 1
> turns into a 0, and everything above stays the same. So a hundred and eight
> becomes a hundred and seven, 0 1 1 0 1 0 1 1.

### 2.3 · The AND
*~6:44 · 41s · 78 words*
**Scene:** N1 (new) · hold 4s

> AND compares two numbers switch by switch and keeps a 1 only where both have
> a 1. Line up a hundred and eight with a hundred and seven. Above the lowest
> 1, the rows are identical, so those bits survive. At the lowest 1 and below
> it, one row always has a 0, so those bits become 0. The result is 0 1 1 0 1
> 0 0 0. The lowest 1 is gone, and nothing else changed.

### 2.4 · What counts as an instruction
*~7:25 · 22s · 43 words*
**Scene:** N1 (new), or reuse the 2-instruction answer from `a0s1` · hold 2s

> Subtract and AND are each one instruction, one of the basic operations built
> into the chip. I allow eleven: add, subtract, multiply, AND, OR, XOR, NOT,
> negate, and three kinds of shift. The shortest program means the one with
> the fewest of those.

---

## Part 3: Programs, recipes and compilers

### 3.1 · A program is a machine
*~7:48 · 30s · 57 words*
**Scene:** `a1s1` act1_recipe.py · hold 3s

> So think of a program as a little machine. A number goes in, passes through
> a few stations, one instruction each, and a number comes out. This one turns
> six into twelve and twenty-one into forty-two. It doubles things. From
> outside, you can't see how many stations it has, and that's the number I
> want to shrink.

### 3.2 · Three ways to double
*~8:18 · 39s · 75 words*
**Scene:** `a1s2` act1_many_recipes.py · hold 3s

> There's more than one way to double a number: add x to itself, multiply by
> two, or shift every bit one place left. The shift works for the same reason
> that adding a zero to the end of a decimal number multiplies it by ten. Each
> binary place is worth twice the one before, so sliding everything left
> doubles it. Put seven, three or ten through all three machines and you get
> the same answer.

### 3.3 · Longer recipes
*~8:57 · 25s · 47 words*
**Scene:** `a1s3` act1_sorted.py · hold 3s

> Those are one instruction each. You could also multiply by four and subtract
> x twice, which is three instructions for the same function. For doubling,
> the shortest version is easy to spot. For most functions it isn't. So how
> would you know you have the shortest one?

### 3.4 · How compilers do it
*~9:22 · 43s · 82 words*
**Scene:** `a1s4` act1_tidy_editor.py · hold 4s

> Compilers answer that with rules. A modern compiler sends your code through
> dozens of passes, and many of them are rewrite rules: a multiply by two
> becomes a shift, adding zero gets deleted, a pointless copy gets cut. Each
> rule is a small, safe improvement, and the compiler keeps applying them
> until nothing matches. Then it stops, with no way of knowing whether the
> result is the shortest program. That's how clang, with no rule for that
> loop, ended up at ninety-eight.

---

## Part 4: Search instead of rules

### 4.1 · Massalin, 1987
*~10:05 · 33s · 62 words*
**Scene:** `a1s5` act1_massalin.py · hold 3s

> In 1987, Alexia Massalin tried something different, in a paper called
> Superoptimizer: A Look at the Smallest Program. Instead of rules, search.
> List every possible program, shortest first, and try each one until one
> computes the function you want. Massalin's superoptimizer checked candidates
> against test inputs, and it found programs short and strange enough that
> nobody would have written them by hand.

### 4.2 · Shortest first
*~10:38 · 30s · 56 words*
**Scene:** `a1s6` act1_program_space.py · hold 3s

> The order matters. With one input and my eleven instructions, there are
> exactly eleven one-instruction programs. If none work, you move to two
> instructions, and there are three hundred and eighty-five of those. Go
> through the lengths in order, and the first program that works has to be the
> shortest, because you've already tried everything shorter.

### 4.3 · The catch
*~11:07 · 16s · 30 words*
**Scene:** `a1s6` act1_program_space.py (hold on the lit dot) · hold 2s

> The catch is the word "works." Massalin's machine tested candidates on
> sample inputs. Passing a test is a good sign, but it isn't a proof, and I
> wanted a proof.

---

## Part 5: Proof instead of testing

### 5.1 · Testing isn't enough
*~11:24 · 23s · 44 words*
**Scene:** `a2s1` act2_two_programs.py · hold 2s

> Take x plus x and x shifted left by one. Put in seven, and both give
> fourteen. Put in twelve, and both give twenty-four. They'll agree on
> anything you try, but agreeing on every input you tried doesn't mean they
> agree on every input.

### 5.2 · How many inputs there are
*~11:47 · 32s · 60 words*
**Scene:** `a2s2` act2_input_wall.py · hold 3s

> A 32-bit number can hold a little over four billion values, and a million
> tests covers about two hundredths of a percent of them. With two inputs,
> there are eighteen quintillion combinations. And the input that breaks a
> program is usually one you'd never think to try, like the most negative
> number, which comes back unchanged when you negate it.

### 5.3 · Reasoning
*~12:18 · 26s · 48 words*
**Scene:** `a2s3` act2_even_reasoning.py · hold 3s

> Math has a way around this. You know an even number plus an even number is
> always even, and you didn't check every even number to know it. You reasoned
> about it once, and that covers all of them. I needed something that reasons
> like that about bits.

### 5.4 · SAT and SMT solvers
*~12:44 · 36s · 70 words*
**Scene:** N2 (new) · hold 3s

> That's what a SAT solver does. You give it a logic formula made of true-or-
> false variables, and it answers one question: is there any way to set them
> that makes the formula true? An SMT solver adds arithmetic on top. I used
> Z3, from Microsoft Research. It turns each 32-bit value into thirty-two
> true-or-false variables, one per bit, and each instruction into the logic
> gates a chip would use.

### 5.5 · Asking it backwards
*~13:20 · 28s · 53 words*
**Scene:** `a2s4` act2_the_dare.py (up to UNSAT) · hold 3s

> Then I ask the question backwards. I translate both programs into formulas,
> add one condition, "the outputs are different," and ask Z3 whether any input
> satisfies it. For x plus x and a shift by one, it answers "unsat," short for
> unsatisfiable. Out of all four billion inputs, there's none where they
> differ.

### 5.6 · How it knows
*~13:49 · 33s · 64 words*
**Scene:** `a2s4` act2_the_dare.py (hold on UNSAT) · hold 3s

> Z3 doesn't get there by trying inputs one at a time. When it hits a
> contradiction, it works out why and writes that down as a new rule, and each
> rule rules out a huge region of possibilities at once. When every region has
> been ruled out, the answer is unsat, and that's a proof that covers every
> input without running any of them.

### 5.7 · A yes comes with evidence
*~14:22 · 32s · 60 words*
**Scene:** `a2s4` act2_the_dare.py (SAT and the witness) · hold 3s

> If the programs are different, the answer comes with evidence. Change the
> shift to a shift by two, and Z3 says "sat" and hands back an input that
> breaks it: one gives two on one side and four on the other. So a "no" is a
> proof, and a "yes" comes with a counterexample. Both turn out to be useful.

---

## Part 6: The first result, then a wall

### 6.1 · Search plus proof
*~14:54 · 28s · 53 words*
**Scene:** `a3s1` act3_ladder.py · hold 3s

> Now I had both halves of a superoptimizer: list programs shortest first, and
> check each one properly. My first version worked at eight bits, where there
> are only two hundred and fifty-six inputs, so it could run every candidate
> on every one of them. That's also a complete check, just a slower one.

### 6.2 · The job
*~15:22 · 25s · 46 words*
**Scene:** `a3s2` act3_one_bit.py · hold 3s

> The first real test, in early June, was a job from the book: keep only the
> lowest 1 bit of a number and clear the rest. It's a cousin of the trick from
> the start. Instead of removing the lowest 1, you keep only that one.

### 6.3 · Found at length two
*~15:47 · 21s · 39 words*
**Scene:** `a3s3` act3_x_and_negx.py (the two lines) · hold 2s

> The search went through all eleven one-instruction programs, and none of
> them worked. At length two, it found this: negate x, then AND it with the
> original. To see why that works, you need one more fact about binary.

### 6.4 · Negative numbers
*~16:07 · 42s · 81 words*
**Scene:** N3 (extends `a3s3`) · hold 3s

> Processors store negative numbers using a system called two's complement. To
> negate a number, you flip every bit, then add one. A hundred and eight, 0 1
> 1 0 1 1 0 0, flips to 1 0 0 1 0 0 1 1. Adding one sends a carry through the
> 1s at the right end, turning them back into 0s, until it reaches the first
> 0, which becomes a 1. The result is 1 0 0 1 0 1 0 0.

### 6.5 · Why the AND works
*~16:49 · 40s · 76 words*
**Scene:** N3 (extends `a3s3`, the column-by-column AND) · hold 4s

> Now line up x and minus x. Above the lowest 1, every bit was flipped, so the
> rows never match and the AND gives 0. Below it, both rows are 0. At the
> lowest 1 itself, both have a 1. So the AND keeps exactly one bit: 0 0 0 0 0
> 1 0 0. Every one-instruction program had failed, so two is the minimum. That
> was the day I started to believe this would work.

### 6.6 · The wall
*~17:29 · 35s · 68 words*
**Scene:** `a3s4` act3_the_wall.py · hold 3s

> Then the numbers caught up with me: eleven programs at length one, three
> hundred and eighty-five at length two, about twenty-seven thousand at length
> three, and over three million at length four. That's with no constants. A
> constant can be any of four billion values, so a single constant multiplies
> the whole count by four billion. Listing programs one at a time was never
> going to get far.

---

## Part 7: The smarter loop

### 7.1 · The real question
*~18:05 · 30s · 58 words*
**Scene:** `a3s6` act3_loop.py (before the loop starts) · hold 2s

> What I really want to ask the solver is whether there's a program that
> matches the function for every input. That has two layers, "there is a
> program" and "for every input," and asking both at once is slow. When I
> tried it directly on some of the harder cases, Z3 hit its one-minute limit
> and answered "unknown."

### 7.2 · CEGIS
*~18:34 · 41s · 80 words*
**Scene:** `a3s6` act3_loop.py · hold 3s

> The fix is a loop called CEGIS, short for counterexample-guided inductive
> synthesis. It splits the question in two. First, find a program that works
> on a few example inputs, which is easy because it only has to match a
> handful of numbers. Then check that program against every input with the
> proof from before. If the check passes, you're done. If not, it hands back
> the input that broke it, and that input joins the examples for the next
> round.

### 7.3 · A real run, round one
*~19:15 · 43s · 83 words*
**Scene:** `a3s8` act3_hole.py, then `a3s6` act3_loop.py with real values · hold 3s

> Here's a real run from my code. The job is to keep every odd-numbered bit of
> a 32-bit number and clear the rest. The program is one instruction, x AND
> some constant, with the constant left blank. In round one, the solver sees a
> single random input and picks a constant that works for it: hex 8 8 2 8 0 2
> 8 8. Only the bits where that input had a 1 mattered, so it could set the
> rest however it liked.

### 7.4 · Rounds two and three
*~19:58 · 43s · 82 words*
**Scene:** `a3s6` act3_loop.py, then `a3s9` act3_fill.py · hold 4s

> The check finds an input where that constant is wrong, and it becomes
> example two. Round two guesses hex 8 A A A A A A A. The check finds another
> input, a number with only bit twenty-nine set, which is exactly the bit the
> guess still has wrong. Round three guesses hex A A A A A A A A, and the
> check comes back unsat. It's proven for all four billion inputs, and the
> solver only ever looked at three.

### 7.5 · Why it converges fast
*~20:41 · 18s · 32 words*
**Scene:** `a3s7` act3_slice.py · hold 3s

> That's why the loop is quick. A counterexample rules out every candidate
> that gets that input wrong, which here meant billions of constants at once.
> Three examples were enough to leave one.

### 7.6 · Constants are unknowns
*~20:59 · 28s · 52 words*
**Scene:** `a3s9` act3_fill.py (hold on 0xAAAAAAAA) · hold 3s

> Constants surprised me more than anything else in the project. Brute force
> would have to try four billion of them to find A A A A A A A A. To a solver,
> a constant is one more unknown in the formula, and it works out what the
> number has to be.

### 7.7 · Wiring
*~21:27 · 41s · 80 words*
**Scene:** N4 (new) · hold 3s

> CEGIS can also build the whole program. This part comes from a 2010 paper by
> Jha, Gulwani, Seshia and Tiwari. You give the solver a bag of instructions,
> say one negate and one AND, and it decides how to wire them together. Number
> the lines: line zero holds x, and lines one and two hold the results of the
> two instructions. Each instruction gets an unknown for the line it writes
> to, and one for each line it reads from.

### 7.8 · The wiring rules
*~22:08 · 48s · 92 words*
**Scene:** N4 (new) · hold 4s

> Then come the rules. An instruction can only read lines before its own, so
> there are no loops. No two instructions share a line. The last line is the
> answer. And if an instruction reads line one, its input equals whatever is
> on line one. Solve for the line numbers and you've built a program. Here the
> solver puts negate on line one, reading x, and AND on line two, reading
> lines zero and one. That's x AND minus x again, found at 32 bits in about
> three hundredths of a second.

---

## Part 8: Can I trust my own proofs?

### 8.1 · A second check
*~22:56 · 40s · 77 words*
**Scene:** `a3s10` act3_two_gates.py · hold 3s

> Then I had a new worry. Every proof depends on my code translating each
> instruction into a formula correctly, and if one translation is wrong, Z3
> will confidently prove the wrong thing. So I added a second check that
> shares no code with the first: a fuzzer. It runs each answer through a
> separate, plain interpreter on a hundred thousand random inputs and compares
> it with the original function. A result only counts if both checks agree.

### 8.2 · How a translation goes wrong
*~23:35 · 40s · 78 words*
**Scene:** `a3s11` act3_saboteur.py · hold 3s

> Right shifts are the classic trap. A logical shift fills the empty spots on
> the left with zeros. An arithmetic shift copies the sign bit, so negative
> numbers stay negative. In Z3's Python library, the normal shift-right
> operator is the arithmetic one. If I'd used it where I meant logical, the
> proofs would still pass, because both sides of every comparison would use
> the same wrong shift. The fuzzer never touches the translation, so it would
> catch it.

### 8.3 · A real catch
*~24:16 · 28s · 54 words*
**Scene:** `a3s11` act3_saboteur.py (hold on the rejected chip) · hold 2s

> The fuzzer has caught something real, too: a well-known branchless trick for
> the smaller of two numbers. When x is the most negative number and y is one,
> it returns one. My proofs couldn't check it, because the minimum needs a
> comparison and my instruction set doesn't have one, but the fuzzer caught
> it.

### 8.4 · Floors
*~24:43 · 36s · 70 words*
**Scene:** `a4s1` act4_green_suite.py · hold 3s

> All of this runs as a test suite every time I push code. The most important
> tests prove floors, meaning nothing shorter exists at 32 bits, whatever the
> constants. To prove absolute value needs three instructions, I gave the
> synthesizer every possible bag of one instruction, eleven of them, and every
> bag of two, sixty-six of them. Every one came back unsat. By late July, the
> whole suite was green.

### 8.5 · Too fast
*~25:20 · 24s · 44 words*
**Scene:** `a4s3` act4_timer.py · hold 3s

> Then I noticed a timing. Floor proofs are the hardest questions this project
> asks, because the solver has to rule out every wiring and every constant.
> Some were finishing in two hundredths of a second. A question that hard
> shouldn't come back that fast.

### 8.6 · Four becomes zero
*~25:44 · 39s · 76 words*
**Scene:** `a4s4` act3_the_twist.py (the 2-bit register) · hold 3s

> The problem was in the wiring. Line numbers are stored in a few bits, and
> I'd sized them to fit the largest line number. Four lines means zero to
> three, which fits in two bits. But one rule says every line number is less
> than four, the number of lines. Four in binary is 1 0 0, which needs three
> bits. In two bits, the top one falls off and leaves 0 0, which is zero.

### 8.7 · Unsat for the wrong reason
*~26:23 · 24s · 45 words*
**Scene:** `a4s4` act3_the_twist.py (the unsat stamp, then the 3-bit fix) · hold 3s

> So the rule became "every line number is less than zero." No unsigned number
> is less than zero, so the rule could never hold, and Z3 correctly said
> unsat. The mistake was in my question, not the solver, and the fix was one
> extra bit.

### 8.8 · Why nothing caught it
*~26:47 · 37s · 72 words*
**Scene:** `a4s5` act4_does_not_work.py · hold 3s

> The worst part is that unsat is exactly what a floor proof expects. The most
> common setup in my sweeps, one input, one constant and two instructions, has
> exactly four lines, so part of the evidence for three published floors
> rested on this bug. It had even shown up once. A test with one constant "did
> not work" and got bumped to two constants, which made five lines and hid the
> problem.

### 8.9 · A test that expects a yes
*~27:24 · 24s · 44 words*
**Scene:** `a4s6` act4_regression.py · hold 3s

> A test that expects "no" can't catch a bug that makes everything say no. So
> the new test checks the other direction. It takes the exact four-line setup
> that used to fail and requires a program to come back: x AND x minus one.

### 8.10 · Rerun
*~27:48 · 29s · 52 words*
**Scene:** `a4s7` act4_slow_suite.py · hold 4s

> Then I reran everything. Floor proofs that took two hundredths of a second
> now took real time, because the solver was finally checking every wiring.
> They all still came back unsat, so every published result held. Since then,
> when a proof says "no" suspiciously fast, I check it before I believe it.

---

## Part 9: Back to the original question

### 9.1 · Fourteen jobs
*~28:17 · 26s · 49 words*
**Scene:** `a5s1` act5_fourteen.py · hold 3s

> With that fixed, I went back to the question that started all this: do
> compilers find these tricks? I picked fourteen small jobs, mostly from
> Hacker's Delight, and wrote each one the plain way, once in Python for
> superopt and once, line for line, in C for the compilers.

### 9.2 · How I counted
*~28:44 · 29s · 57 words*
**Scene:** N5 (new, optional), or hold on `a5s1` · hold 2s

> I compiled with gcc on my own machine and clang through Compiler Explorer,
> every optimization on, and counted every instruction except the final
> return. A script does the counting, so the rule is the same for every job.
> Superopt's numbers are labeled proven, best found, verified upper bound, or
> no result. Seven of the fourteen are proven.

### 9.3 · The scoreboard
*~29:13 · 21s · 35 words*
**Scene:** `a5s2` act4_scoreboard.py · hold 4s

> Clearing the lowest bit, the example from the start: gcc, eighteen. Clang,
> ninety-eight. Superopt, two, proven. Smearing the lowest bit: nineteen,
> ninety-seven, two. Isolating it, the job the search solved in June:
> fourteen, ninety-seven, two.

### 9.4 · What the compilers did
*~29:33 · 33s · 63 words*
**Scene:** `a5s3` act5_naive_loop.py · hold 3s

> Gcc keeps the loop: a counter, a 1 shifted into position, a test, and a jump
> back, up to thirty-two times. Clang unrolls it into the thirty-two copies
> from the start. Newer processors even have one instruction that does exactly
> x AND x minus one, called BLSR. With it turned on, neither compiler used it,
> because neither recognized what the loop was doing.

### 9.5 · Where superopt loses
*~30:06 · 39s · 75 words*
**Scene:** `a5s4` act5_honesty_rows.py · hold 3s

> Superopt doesn't win everything, and I picked some jobs expecting to lose.
> Rotating bits has its own x86 instruction, so the compilers need one or two.
> My instruction set has no rotate, so my best is two shifts and an OR: three,
> proven minimal within my set. Byte swapping has its own instruction too. My
> best is nine, an upper bound rather than a proven floor. A table of only
> wins wouldn't tell you much.

### 9.6 · A trick I'd never write
*~30:45 · 43s · 85 words*
**Scene:** `a5s5` act5_alien_trick.py · hold 3s

> It also found things I'd never write. For absolute value, it shifts x right
> by x itself. In my instruction set, a shift of thirty-two or more fills the
> result with the sign bit. A negative x, read as a shift amount, is huge, so
> the result is all 1s. A positive x is always less than two to the x, so the
> result is zero. That one step builds a "negative or not" mask with no
> constant, and two more instructions finish the job.

### 9.7 · Only in its own world
*~31:29 · 24s · 44 words*
**Scene:** `a5s5` act5_alien_trick.py (the copy that cracks outside the ring) · hold 3s

> Real x86 chips only use the bottom five bits of a shift amount, though, so
> on real hardware this program says the absolute value of thirty-two is minus
> thirty-two. It's proven under my rules and wrong on the chip, and the
> writeup says so.

### 9.8 · Filed upstream
*~31:52 · 14s · 23 words*
**Scene:** `a5s6` act5_filed_issue.py · hold 3s

> The bit-scan results held up, so I filed them with the LLVM project, which
> makes clang, as a missed optimization. It's issue two-one-two-nine-oh-eight.

---

## Part 10: Limits, credit, outro

### 10.1 · The wall I didn't get past
*~32:06 · 46s · 91 words*
**Scene:** `a5s7` act5_still_cant.py · hold 3s

> Some jobs are still too big. Popcount counts the 1 bits in a number, and its
> fast version uses a few magic masks, so it looked like a perfect target. But
> each CEGIS round has to find one wiring that fits every example so far, and
> that gets expensive as examples pile up. Even at eight bits, the first five
> rounds took six hundredths of a second, a tenth, four seconds, eleven and
> twenty-seven, and then it stopped finishing. The test stays in the suite, so
> the limit is on record.

### 10.2 · Credit
*~32:53 · 18s · 31 words*
**Scene:** `a5s10` act5_attribution.py · hold 3s

> None of the core ideas here are mine. Superoptimization is Alexia
> Massalin's. CEGIS comes from Armando Solar-Lezama's work on program
> synthesis, and the wiring comes from Jha, Gulwani, Seshia and Tiwari.

### 10.3 · What I built
*~33:11 · 26s · 51 words*
**Scene:** `a5s11` act5_suite.py · hold 2s

> What I built is the instruction set, the translation into formulas, the two
> checks, the benchmarks and the measurements. There are over a hundred tests,
> and every proof in this video reruns on your own machine. The stretch goal I
> haven't done yet is using machine learning to guide the search.

### 10.4 · Outro
*~33:37 · 15s · 23 words*
**Scene:** `a5s12` act5_end.py · hold 4s

> I want to study computer science next. Everything is on GitHub, linked
> below: the code, the proofs, and the mistakes. Thanks for watching.

---

## Sources for the numbers

- **98 and 2:** `results/asm/clang-clear_lowest_bit-base.s` (clang 22.1.0 via
  Compiler Explorer, 32 × `mov`/`test`/`jne` + 2); the scoreboard numbers come
  from `results/compiler_gap.md`.
- **11 / 385 / 27,720 / 3,381,840 programs:** counted with
  `superopt/search.py`'s own enumerator, one input, no constants.
- **The CEGIS run (`0x88280288` → `0x8AAAAAAA` → `0xAAAAAAAA`,
  counterexamples `0x0282A822`, `0x20000000`):** logged from
  `synth.synthesize_constants`, seed 0, the setup in `tests/test_synth.py`.
- **Wiring in about 0.03 s:** logged from `cegis.synthesize`,
  `Library(NEG, AND)`, 32-bit, seed 0 (converged in one round).
- **"Unknown" at one minute:** `report/report.md`, "What broke and what it
  taught".
- **11 + 66 libraries for the absval floor:** `DECISION_LOG.md`, Phase 5B.
- **The min trick (x = INT_MIN, y = 1):** `test_folklore_min_trick_is_wrong`.
- **abs(32) = −32 on x86:** checked by modeling `sar`'s 5-bit count mask
  against the synthesized program.
- **Popcount round times:** `DECISION_LOG.md`, Phase 4b.
- **BLSR unused:** the `-march=x86-64-v3` columns (gcc 16, clang 98) in
  `results/compiler_gap.md`.
- **Stockfish `pop_lsb`:** `b &= b - 1` in Stockfish's `bitboard.h`. Check the
  current source before filming.

---

## Read-through (VO only, for recording)

**[I.1 · ~0:00]** Hi, I'm Curtis. I'm a high schooler, and I like coding and games. This summer I built a project called superopt, and this video is the story of how it went, from the first idea to the mistakes to what I found at the end.

**[I.2 · ~0:23]** It started with reading about compilers. When you write code, the processor can't run it directly. A compiler translates it into the processor's own instructions, tiny steps like add, subtract and compare. A compiler also tries to make the result fast, and that part is what caught my attention.

**[I.3 · ~0:50]** On the side, I was playing with bit tricks. Inside a computer, a number is stored as a row of 1s and 0s, and bit tricks are shortcuts that work directly on those 1s and 0s. The classic collection of them is a book called Hacker's Delight.

**[I.4 · ~1:15]** Here's one of them. Say you want to take a number and switch off its lowest 1 bit. The obvious way is a loop: look at the bits one at a time until you find a 1, then switch it off. The book's version is x AND x minus one. There's no loop, and it takes two instructions. I'll show you exactly why it works in a few minutes.

**[I.5 · ~1:52]** That's where the two things met. If a trick like that exists, does the compiler know it? If I write the slow loop, does the compiler swap in the two-instruction version on its own? Later in the summer I measured it, and the answer surprised me.

**[I.6 · ~2:17]** This isn't only a puzzle, and games are a good example. Chess engines like Stockfish keep the board as 64-bit numbers, one bit for each square. To go through the pieces, they use this exact trick, x AND x minus one, over and over, millions of times a second while they search for a move.

**[I.7 · ~2:46]** Compilers also work at a huge scale. Clang, one of the two big C compilers, builds iPhone apps, Android apps and Chrome. When a piece of code runs millions of times a second on billions of devices, one wasted instruction adds up.

**[I.8 · ~3:09]** So the question got bigger. Forget this one trick. For any small function, what's the shortest program that computes it? And could I prove that nothing shorter exists, for every possible input, including the ones I never tried?

**[I.9 · ~3:30]** That problem has a name, superoptimization, and people have been working on it since 1987. From the end of May to the middle of August, I built one. This video is how it works, what went wrong along the way, and what I found.

**[1.1 · ~3:54]** Let's start with that loop, written out in C. It checks bit zero, then bit one, and so on up to bit thirty-one. The first 1 it finds, it switches off and returns. If the number is zero, it returns zero. That's how most people would write it, and it's what I handed the compiler.

**[1.2 · ~4:24]** I gave this to clang with every optimization on, and this came out. Clang copied the check thirty-two times, once per bit. Each copy is three instructions: load the bit's value, test it, and jump out if it's set. Thirty-two times three is ninety-six, plus two at the end: ninety-eight instructions.

**[1.3 · ~4:54]** And here's the trick from the book, as the processor sees it. Subtract one, then AND with the original. Two instructions, and the same answer for every one of the four billion possible inputs.

**[1.4 · ~5:14]** That gap, ninety-eight against two, is what this project is about. Superopt finds answers like the two on its own, and then proves there's nothing shorter.

**[2.1 · ~5:31]** To see why the trick works, you have to look at numbers the way the processor does: as a row of switches, each one on or off, 1 or 0. Each position is worth double the one to its right: one, two, four, eight, and so on. A hundred and eight is sixty-four plus thirty-two plus eight plus four, so it reads 0 1 1 0 1 1 0 0. Real registers have thirty-two or sixty-four switches. I'll use eight so it fits.

**[2.2 · ~6:14]** Now subtract one. It works like subtracting one from a thousand in decimal: you borrow from the left. The 0s at the right end turn into 1s, the lowest 1 turns into a 0, and everything above stays the same. So a hundred and eight becomes a hundred and seven, 0 1 1 0 1 0 1 1.

**[2.3 · ~6:44]** AND compares two numbers switch by switch and keeps a 1 only where both have a 1. Line up a hundred and eight with a hundred and seven. Above the lowest 1, the rows are identical, so those bits survive. At the lowest 1 and below it, one row always has a 0, so those bits become 0. The result is 0 1 1 0 1 0 0 0. The lowest 1 is gone, and nothing else changed.

**[2.4 · ~7:25]** Subtract and AND are each one instruction, one of the basic operations built into the chip. I allow eleven: add, subtract, multiply, AND, OR, XOR, NOT, negate, and three kinds of shift. The shortest program means the one with the fewest of those.

**[3.1 · ~7:48]** So think of a program as a little machine. A number goes in, passes through a few stations, one instruction each, and a number comes out. This one turns six into twelve and twenty-one into forty-two. It doubles things. From outside, you can't see how many stations it has, and that's the number I want to shrink.

**[3.2 · ~8:18]** There's more than one way to double a number: add x to itself, multiply by two, or shift every bit one place left. The shift works for the same reason that adding a zero to the end of a decimal number multiplies it by ten. Each binary place is worth twice the one before, so sliding everything left doubles it. Put seven, three or ten through all three machines and you get the same answer.

**[3.3 · ~8:57]** Those are one instruction each. You could also multiply by four and subtract x twice, which is three instructions for the same function. For doubling, the shortest version is easy to spot. For most functions it isn't. So how would you know you have the shortest one?

**[3.4 · ~9:22]** Compilers answer that with rules. A modern compiler sends your code through dozens of passes, and many of them are rewrite rules: a multiply by two becomes a shift, adding zero gets deleted, a pointless copy gets cut. Each rule is a small, safe improvement, and the compiler keeps applying them until nothing matches. Then it stops, with no way of knowing whether the result is the shortest program. That's how clang, with no rule for that loop, ended up at ninety-eight.

**[4.1 · ~10:05]** In 1987, Alexia Massalin tried something different, in a paper called Superoptimizer: A Look at the Smallest Program. Instead of rules, search. List every possible program, shortest first, and try each one until one computes the function you want. Massalin's superoptimizer checked candidates against test inputs, and it found programs short and strange enough that nobody would have written them by hand.

**[4.2 · ~10:38]** The order matters. With one input and my eleven instructions, there are exactly eleven one-instruction programs. If none work, you move to two instructions, and there are three hundred and eighty-five of those. Go through the lengths in order, and the first program that works has to be the shortest, because you've already tried everything shorter.

**[4.3 · ~11:07]** The catch is the word "works." Massalin's machine tested candidates on sample inputs. Passing a test is a good sign, but it isn't a proof, and I wanted a proof.

**[5.1 · ~11:24]** Take x plus x and x shifted left by one. Put in seven, and both give fourteen. Put in twelve, and both give twenty-four. They'll agree on anything you try, but agreeing on every input you tried doesn't mean they agree on every input.

**[5.2 · ~11:47]** A 32-bit number can hold a little over four billion values, and a million tests covers about two hundredths of a percent of them. With two inputs, there are eighteen quintillion combinations. And the input that breaks a program is usually one you'd never think to try, like the most negative number, which comes back unchanged when you negate it.

**[5.3 · ~12:18]** Math has a way around this. You know an even number plus an even number is always even, and you didn't check every even number to know it. You reasoned about it once, and that covers all of them. I needed something that reasons like that about bits.

**[5.4 · ~12:44]** That's what a SAT solver does. You give it a logic formula made of true-or- false variables, and it answers one question: is there any way to set them that makes the formula true? An SMT solver adds arithmetic on top. I used Z3, from Microsoft Research. It turns each 32-bit value into thirty-two true-or-false variables, one per bit, and each instruction into the logic gates a chip would use.

**[5.5 · ~13:20]** Then I ask the question backwards. I translate both programs into formulas, add one condition, "the outputs are different," and ask Z3 whether any input satisfies it. For x plus x and a shift by one, it answers "unsat," short for unsatisfiable. Out of all four billion inputs, there's none where they differ.

**[5.6 · ~13:49]** Z3 doesn't get there by trying inputs one at a time. When it hits a contradiction, it works out why and writes that down as a new rule, and each rule rules out a huge region of possibilities at once. When every region has been ruled out, the answer is unsat, and that's a proof that covers every input without running any of them.

**[5.7 · ~14:22]** If the programs are different, the answer comes with evidence. Change the shift to a shift by two, and Z3 says "sat" and hands back an input that breaks it: one gives two on one side and four on the other. So a "no" is a proof, and a "yes" comes with a counterexample. Both turn out to be useful.

**[6.1 · ~14:54]** Now I had both halves of a superoptimizer: list programs shortest first, and check each one properly. My first version worked at eight bits, where there are only two hundred and fifty-six inputs, so it could run every candidate on every one of them. That's also a complete check, just a slower one.

**[6.2 · ~15:22]** The first real test, in early June, was a job from the book: keep only the lowest 1 bit of a number and clear the rest. It's a cousin of the trick from the start. Instead of removing the lowest 1, you keep only that one.

**[6.3 · ~15:47]** The search went through all eleven one-instruction programs, and none of them worked. At length two, it found this: negate x, then AND it with the original. To see why that works, you need one more fact about binary.

**[6.4 · ~16:07]** Processors store negative numbers using a system called two's complement. To negate a number, you flip every bit, then add one. A hundred and eight, 0 1 1 0 1 1 0 0, flips to 1 0 0 1 0 0 1 1. Adding one sends a carry through the 1s at the right end, turning them back into 0s, until it reaches the first 0, which becomes a 1. The result is 1 0 0 1 0 1 0 0.

**[6.5 · ~16:49]** Now line up x and minus x. Above the lowest 1, every bit was flipped, so the rows never match and the AND gives 0. Below it, both rows are 0. At the lowest 1 itself, both have a 1. So the AND keeps exactly one bit: 0 0 0 0 0 1 0 0. Every one-instruction program had failed, so two is the minimum. That was the day I started to believe this would work.

**[6.6 · ~17:29]** Then the numbers caught up with me: eleven programs at length one, three hundred and eighty-five at length two, about twenty-seven thousand at length three, and over three million at length four. That's with no constants. A constant can be any of four billion values, so a single constant multiplies the whole count by four billion. Listing programs one at a time was never going to get far.

**[7.1 · ~18:05]** What I really want to ask the solver is whether there's a program that matches the function for every input. That has two layers, "there is a program" and "for every input," and asking both at once is slow. When I tried it directly on some of the harder cases, Z3 hit its one-minute limit and answered "unknown."

**[7.2 · ~18:34]** The fix is a loop called CEGIS, short for counterexample-guided inductive synthesis. It splits the question in two. First, find a program that works on a few example inputs, which is easy because it only has to match a handful of numbers. Then check that program against every input with the proof from before. If the check passes, you're done. If not, it hands back the input that broke it, and that input joins the examples for the next round.

**[7.3 · ~19:15]** Here's a real run from my code. The job is to keep every odd-numbered bit of a 32-bit number and clear the rest. The program is one instruction, x AND some constant, with the constant left blank. In round one, the solver sees a single random input and picks a constant that works for it: hex 8 8 2 8 0 2 8 8. Only the bits where that input had a 1 mattered, so it could set the rest however it liked.

**[7.4 · ~19:58]** The check finds an input where that constant is wrong, and it becomes example two. Round two guesses hex 8 A A A A A A A. The check finds another input, a number with only bit twenty-nine set, which is exactly the bit the guess still has wrong. Round three guesses hex A A A A A A A A, and the check comes back unsat. It's proven for all four billion inputs, and the solver only ever looked at three.

**[7.5 · ~20:41]** That's why the loop is quick. A counterexample rules out every candidate that gets that input wrong, which here meant billions of constants at once. Three examples were enough to leave one.

**[7.6 · ~20:59]** Constants surprised me more than anything else in the project. Brute force would have to try four billion of them to find A A A A A A A A. To a solver, a constant is one more unknown in the formula, and it works out what the number has to be.

**[7.7 · ~21:27]** CEGIS can also build the whole program. This part comes from a 2010 paper by Jha, Gulwani, Seshia and Tiwari. You give the solver a bag of instructions, say one negate and one AND, and it decides how to wire them together. Number the lines: line zero holds x, and lines one and two hold the results of the two instructions. Each instruction gets an unknown for the line it writes to, and one for each line it reads from.

**[7.8 · ~22:08]** Then come the rules. An instruction can only read lines before its own, so there are no loops. No two instructions share a line. The last line is the answer. And if an instruction reads line one, its input equals whatever is on line one. Solve for the line numbers and you've built a program. Here the solver puts negate on line one, reading x, and AND on line two, reading lines zero and one. That's x AND minus x again, found at 32 bits in about three hundredths of a second.

**[8.1 · ~22:56]** Then I had a new worry. Every proof depends on my code translating each instruction into a formula correctly, and if one translation is wrong, Z3 will confidently prove the wrong thing. So I added a second check that shares no code with the first: a fuzzer. It runs each answer through a separate, plain interpreter on a hundred thousand random inputs and compares it with the original function. A result only counts if both checks agree.

**[8.2 · ~23:35]** Right shifts are the classic trap. A logical shift fills the empty spots on the left with zeros. An arithmetic shift copies the sign bit, so negative numbers stay negative. In Z3's Python library, the normal shift-right operator is the arithmetic one. If I'd used it where I meant logical, the proofs would still pass, because both sides of every comparison would use the same wrong shift. The fuzzer never touches the translation, so it would catch it.

**[8.3 · ~24:16]** The fuzzer has caught something real, too: a well-known branchless trick for the smaller of two numbers. When x is the most negative number and y is one, it returns one. My proofs couldn't check it, because the minimum needs a comparison and my instruction set doesn't have one, but the fuzzer caught it.

**[8.4 · ~24:43]** All of this runs as a test suite every time I push code. The most important tests prove floors, meaning nothing shorter exists at 32 bits, whatever the constants. To prove absolute value needs three instructions, I gave the synthesizer every possible bag of one instruction, eleven of them, and every bag of two, sixty-six of them. Every one came back unsat. By late July, the whole suite was green.

**[8.5 · ~25:20]** Then I noticed a timing. Floor proofs are the hardest questions this project asks, because the solver has to rule out every wiring and every constant. Some were finishing in two hundredths of a second. A question that hard shouldn't come back that fast.

**[8.6 · ~25:44]** The problem was in the wiring. Line numbers are stored in a few bits, and I'd sized them to fit the largest line number. Four lines means zero to three, which fits in two bits. But one rule says every line number is less than four, the number of lines. Four in binary is 1 0 0, which needs three bits. In two bits, the top one falls off and leaves 0 0, which is zero.

**[8.7 · ~26:23]** So the rule became "every line number is less than zero." No unsigned number is less than zero, so the rule could never hold, and Z3 correctly said unsat. The mistake was in my question, not the solver, and the fix was one extra bit.

**[8.8 · ~26:47]** The worst part is that unsat is exactly what a floor proof expects. The most common setup in my sweeps, one input, one constant and two instructions, has exactly four lines, so part of the evidence for three published floors rested on this bug. It had even shown up once. A test with one constant "did not work" and got bumped to two constants, which made five lines and hid the problem.

**[8.9 · ~27:24]** A test that expects "no" can't catch a bug that makes everything say no. So the new test checks the other direction. It takes the exact four-line setup that used to fail and requires a program to come back: x AND x minus one.

**[8.10 · ~27:48]** Then I reran everything. Floor proofs that took two hundredths of a second now took real time, because the solver was finally checking every wiring. They all still came back unsat, so every published result held. Since then, when a proof says "no" suspiciously fast, I check it before I believe it.

**[9.1 · ~28:17]** With that fixed, I went back to the question that started all this: do compilers find these tricks? I picked fourteen small jobs, mostly from Hacker's Delight, and wrote each one the plain way, once in Python for superopt and once, line for line, in C for the compilers.

**[9.2 · ~28:44]** I compiled with gcc on my own machine and clang through Compiler Explorer, every optimization on, and counted every instruction except the final return. A script does the counting, so the rule is the same for every job. Superopt's numbers are labeled proven, best found, verified upper bound, or no result. Seven of the fourteen are proven.

**[9.3 · ~29:13]** Clearing the lowest bit, the example from the start: gcc, eighteen. Clang, ninety-eight. Superopt, two, proven. Smearing the lowest bit: nineteen, ninety-seven, two. Isolating it, the job the search solved in June: fourteen, ninety-seven, two.

**[9.4 · ~29:33]** Gcc keeps the loop: a counter, a 1 shifted into position, a test, and a jump back, up to thirty-two times. Clang unrolls it into the thirty-two copies from the start. Newer processors even have one instruction that does exactly x AND x minus one, called BLSR. With it turned on, neither compiler used it, because neither recognized what the loop was doing.

**[9.5 · ~30:06]** Superopt doesn't win everything, and I picked some jobs expecting to lose. Rotating bits has its own x86 instruction, so the compilers need one or two. My instruction set has no rotate, so my best is two shifts and an OR: three, proven minimal within my set. Byte swapping has its own instruction too. My best is nine, an upper bound rather than a proven floor. A table of only wins wouldn't tell you much.

**[9.6 · ~30:45]** It also found things I'd never write. For absolute value, it shifts x right by x itself. In my instruction set, a shift of thirty-two or more fills the result with the sign bit. A negative x, read as a shift amount, is huge, so the result is all 1s. A positive x is always less than two to the x, so the result is zero. That one step builds a "negative or not" mask with no constant, and two more instructions finish the job.

**[9.7 · ~31:29]** Real x86 chips only use the bottom five bits of a shift amount, though, so on real hardware this program says the absolute value of thirty-two is minus thirty-two. It's proven under my rules and wrong on the chip, and the writeup says so.

**[9.8 · ~31:52]** The bit-scan results held up, so I filed them with the LLVM project, which makes clang, as a missed optimization. It's issue two-one-two-nine-oh-eight.

**[10.1 · ~32:06]** Some jobs are still too big. Popcount counts the 1 bits in a number, and its fast version uses a few magic masks, so it looked like a perfect target. But each CEGIS round has to find one wiring that fits every example so far, and that gets expensive as examples pile up. Even at eight bits, the first five rounds took six hundredths of a second, a tenth, four seconds, eleven and twenty-seven, and then it stopped finishing. The test stays in the suite, so the limit is on record.

**[10.2 · ~32:53]** None of the core ideas here are mine. Superoptimization is Alexia Massalin's. CEGIS comes from Armando Solar-Lezama's work on program synthesis, and the wiring comes from Jha, Gulwani, Seshia and Tiwari.

**[10.3 · ~33:11]** What I built is the instruction set, the translation into formulas, the two checks, the benchmarks and the measurements. There are over a hundred tests, and every proof in this video reruns on your own machine. The stretch goal I haven't done yet is using machine learning to guide the search.

**[10.4 · ~33:37]** I want to study computer science next. Everything is on GitHub, linked below: the code, the proofs, and the mistakes. Thanks for watching.
