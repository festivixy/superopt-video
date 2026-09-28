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


def test_malformed_beat_header_is_rejected():
    # Final review #2: a header that doesn't match must not silently merge into the previous beat
    bad = SAMPLE.replace("### 1.1 · The loop", "### 1.1 - The loop")
    with pytest.raises(ValueError, match="1.1 - The loop"):
        st.parse(bad)


def test_two_holds_in_one_beat_are_rejected():
    bad = SAMPLE.replace("> Here's the loop.", "> Here's the loop.\n**Scene:** extra · hold 3s\n> more")
    with pytest.raises(ValueError, match="1.1.*more than one"):
        st.parse(bad)
