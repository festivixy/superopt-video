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
        "renders/media/part2/B_2_3/videos/part2/480p15/B_2_3.mp4"
    )
    assert "1080p60" in render.output_path("beats/part2.py", "B_2_3", "final").as_posix()


def test_concat_list_escapes_quotes():
    text = render.concat_list_text([Path("a/b's.mp4")])
    assert text.strip() == "file '" + Path("a/b's.mp4").resolve().as_posix().replace("'", "'\\''") + "'"


def test_each_beat_renders_into_its_own_media_dir():
    # parallel manim processes race on a shared text/tex SVG cache; one dir per beat avoids it
    a = render.manim_command("beats/intro.py", "B_I_1", "preview")
    b = render.manim_command("beats/intro.py", "B_I_2", "preview")
    media = lambda cmd: cmd[cmd.index("--media_dir") + 1]
    assert media(a) != media(b)


def test_scene_class_names_match_their_beat_ids():
    # Final review #3: render.py selects scenes by class name, the registry by beat_id
    from beats import all_beats

    for beat_id, cls in all_beats().items():
        assert cls.__name__ == render.class_name(beat_id)


def test_registry_rejects_a_misnamed_scene():
    import types

    from beats import all_beats
    from kit.beat import BeatScene

    module = types.ModuleType("fake_beats")

    class B_9_9(BeatScene):
        beat_id = "9.8"

    module.B_9_9 = B_9_9
    import sys
    sys.modules["fake_beats"] = module
    try:
        with pytest.raises(ValueError, match="B_9_9.*9.8"):
            all_beats(("fake_beats",))
    finally:
        del sys.modules["fake_beats"]


def test_child_renders_never_wait_on_stdin(monkeypatch, tmp_path):
    seen = {}

    def fake_run(cmd, **kwargs):
        seen.update(kwargs)
        raise SystemExit  # stop before checking outputs

    monkeypatch.setattr(render.subprocess, "run", fake_run)
    with pytest.raises(SystemExit):
        render._render_one("beats/intro.py", "B_I_1", "preview")
    assert seen.get("stdin") == render.subprocess.DEVNULL
