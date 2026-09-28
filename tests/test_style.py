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
