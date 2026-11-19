#!/usr/bin/env python3
"""audiotool.py — tiny offline audio CLI for agent-audio-skills.

Stdlib only. No dependencies, no network, no cloud.
Wraps ffmpeg when available, and always explains
what to do when it is missing.

Usage:
  python tools/audiotool.py check
  python tools/audiotool.py trim podcast.mp3 clip.mp3 --start 30 --end 90
  python tools/audiotool.py normalize quiet.mp3 loud.mp3
  python tools/audiotool.py extract video.mp4 audio.mp3
"""
import argparse
import os
import shutil
import subprocess
import sys


def fail(msg):
    print(f"audiotool: error: {msg}", file=sys.stderr)
    return 2


def need_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("audiotool: ffmpeg not found.", file=sys.stderr)
        print("Install it, then run `python tools/audiotool.py check` again:", file=sys.stderr)
        print("  Windows: winget install ffmpeg  (or choco install ffmpeg)", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Linux:   sudo apt install ffmpeg", file=sys.stderr)
        return False
    return True


def run(cmd):
    print(" ".join(cmd))
    r = subprocess.run(cmd)
    return r.returncode


def check_in(path):
    if not os.path.isfile(path):
        print(f"audiotool: error: input not found: {path}", file=sys.stderr)
        return False
    return True


def ensure_out(path):
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)


def cmd_check(_a):
    p = shutil.which("ffmpeg")
    print(f"ffmpeg: {'found at ' + p if p else 'NOT FOUND'}")
    if p:
        try:
            out = subprocess.check_output(["ffmpeg", "-version"], text=True, timeout=10)
            print("  " + out.splitlines()[0])
        except Exception as e:
            print(f"  could not run: {e}")
        print("\nOK: ready. Try: python tools/audiotool.py trim in.mp3 out.mp3 --start 30 --end 90")
        return 0
    print("Install it, then run `python tools/audiotool.py check` again:")
    print("  Windows: winget install ffmpeg  (or choco install ffmpeg)")
    print("  macOS:   brew install ffmpeg")
    print("  Linux:   sudo apt install ffmpeg")
    print("\nInstall ffmpeg (see above) to enable trim / normalize / extract.")
    return 1


def cmd_trim(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    ensure_out(a.output)
    if a.reencode:
        cmd = ["ffmpeg", "-y", "-ss", str(a.start), "-to", str(a.end),
               "-i", a.input, "-c:a", "libmp3lame", "-q:a", "4", a.output]
    else:
        cmd = ["ffmpeg", "-y", "-ss", str(a.start), "-to", str(a.end),
               "-i", a.input, "-c", "copy", a.output]
    rc = run(cmd)
    if rc == 0:
        print(f"Saved: {a.output}  ({a.start}s to {a.end}s)")
    return rc


def cmd_normalize(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    ensure_out(a.output)
    # Single-pass loudnorm to -16 LUFS (podcast level), with a true peak limit.
    cmd = ["ffmpeg", "-y", "-i", a.input,
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
           "-c:a", "libmp3lame", "-q:a", "4", a.output]
    rc = run(cmd)
    if rc == 0:
        print(f"Saved: {a.output}  (normalized to -16 LUFS)")
    return rc


def cmd_extract(a):
    if not need_ffmpeg() or not check_in(a.input):
        return 2
    ensure_out(a.output)
    cmd = ["ffmpeg", "-y", "-i", a.input, "-vn",
           "-c:a", "libmp3lame", "-q:a", "4", a.output]
    rc = run(cmd)
    if rc == 0:
        print(f"Saved: {a.output}  (audio extracted from {a.input})")
    return rc


def main(argv=None):
    p = argparse.ArgumentParser(prog="audiotool", description="Tiny offline audio CLI (stdlib only, wraps ffmpeg).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("check", help="Check ffmpeg is installed")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("trim", help="Cut audio to a start and end time")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--start", type=float, required=True)
    s.add_argument("--end", type=float, required=True)
    s.add_argument("--reencode", action="store_true", help="Re-encode (frame-accurate)")
    s.set_defaults(fn=cmd_trim)

    s = sub.add_parser("normalize", help="Normalize volume to -16 LUFS (podcast level)")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(fn=cmd_normalize)

    s = sub.add_parser("extract", help="Extract audio from a video file as MP3")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(fn=cmd_extract)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
