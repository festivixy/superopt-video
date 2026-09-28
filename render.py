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
