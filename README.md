# agent-audio-skills

> **Agent Skills for audio — trim podcasts, normalize volume, and extract audio from video. Offline, ffmpeg-powered.**

**1 skill · 1 CLI · ffmpeg-powered · 100% offline**

[![GitHub stars](https://img.shields.io/github/stars/megaartaiking-cmd/agent-audio-skills?style=social)](https://github.com/megaartaiking-cmd/agent-audio-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](tools/audiotool.py)

AI agents are great at code, but audio still means opening a DAW or a heavy editor for the simplest jobs — cut a clip, even out the volume, or pull the audio out of a video. This repo fixes that gap: a small Agent Skill (SKILL.md) plus a tiny Python CLI that wraps ffmpeg, so an agent can do the common audio jobs — in the terminal, on the user's own PC.

Works with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and any agent that reads SKILL.md files.

## Why this exists

Agent Skills are the fastest-growing category on GitHub — small, composable skill bundles, one job per skill, install in one step. Audio is the missing one: podcasts, voice notes, and video soundtracks are everywhere, and no small, offline, agent-native skill edits them.

This one is:

- **Agent-native** — a skill in the open SKILL.md format, one job, clear rules
- **Offline** — no upload, no cloud render, files never leave the PC
- **Lightweight** — stdlib-only Python plus ffmpeg, no DAW, no 150 MB app
- **Low-end friendly** — fast cuts first, podcast-level normalization, built for the same PCs as LiteCut Pro (512 MB RAM, single-core)

## Skills

| Skill | What it does | Command |
|---|---|---|
| `audio-edit` | Trim audio, normalize volume, extract audio | `audiotool.py` |

The skill lives in `skills/audio-edit/SKILL.md` — copy that folder into your agent's skills folder, or point your agent at this repo.

## Quick start

```sh
git clone https://github.com/megaartaiking-cmd/agent-audio-skills.git
cd agent-audio-skills

# 1. Check ffmpeg is installed
python tools/audiotool.py check

# 2. Trim 30–90 seconds (fast copy)
python tools/audiotool.py trim podcast.mp3 clip.mp3 --start 30 --end 90

# 3. Normalize volume to podcast level
python tools/audiotool.py normalize quiet.mp3 loud.mp3
```

No ffmpeg yet? Install it once:

- Windows: `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

## Usage

```sh
# Trim audio to a start and end time
python tools/audiotool.py trim podcast.mp3 clip.mp3 --start 30 --end 90

# Frame-accurate trim (slower, re-encodes)
python tools/audiotool.py trim podcast.mp3 clip.mp3 --start 30 --end 90 --reencode

# Normalize volume to -16 LUFS (podcast level)
python tools/audiotool.py normalize quiet.mp3 loud.mp3

# Extract audio from a video file as MP3
python tools/audiotool.py extract video.mp4 audio.mp3
```

See [examples/commands.md](examples/commands.md) for all commands. No sample audio is committed to this repo — any `.mp3` or `.mp4` file works, and the commands file shows how to generate a test tone with ffmpeg.

## How it works

1. You (or your agent) describe the job in plain words: "trim 30–90 seconds, then normalize it".
2. The skill in `skills/audio-edit/` tells the agent the exact workflow, the command to run, and the rules — never overwrite the original, always write to a new file.
3. `tools/audiotool.py` (stdlib-only Python) runs ffmpeg locally and reports the output path.
4. Nothing is uploaded. The edit happens on your PC.

For visual editing, pair this with [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — the same offline, low-end editor, with a timeline, titles, and filters in the browser.

## Works with

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini CLI
- Any agent that reads Agent Skills (SKILL.md)

Copy `skills/audio-edit/` into your agent's skills directory, or ask your agent to read the SKILL.md file in this repo directly.

## FAQ

**Does it need the internet?**
No. After `git clone`, everything runs offline. ffmpeg runs locally.

**Does it need a DAW?**
No. It uses ffmpeg, which is free and far lighter than a full audio editor.

**Will it run on an old PC?**
Yes — that is the point. Fast cuts avoid re-encoding, and there is no Electron / Chromium app to load.

**What is -16 LUFS?**
The loudness level podcasts usually target. Normalizing to it makes a quiet recording as loud as a typical podcast.

**What formats?**
Input: MP3 and anything ffmpeg reads, including MP4 video. Output: MP3.

**Can I add a skill?**
Yes — copy `skills/audio-edit/` as a template, write a SKILL.md with a clear name, description, workflow, and rules, and open a pull request.

## Contributing

Issues and pull requests are welcome. Keep skills small, one job per skill, with a tested command in `tools/audiotool.py`. Please do not add dependencies — stdlib only.

## License

MIT — see [LICENSE](LICENSE).

## More Agent Skills

More offline Agent Skills by the same author — one focused skill per repo:

- [agent-csv-skills](https://github.com/megaartaiking-cmd/agent-csv-skills) — Clean, filter, summarize CSVs; convert to JSON and Markdown
- [agent-json-skills](https://github.com/megaartaiking-cmd/agent-json-skills) — Validate, format, flatten, query, and diff JSON
- [agent-markdown-skills](https://github.com/megaartaiking-cmd/agent-markdown-skills) — Markdown to HTML, table of contents, link check, word count
- [agent-git-skills](https://github.com/megaartaiking-cmd/agent-git-skills) — Commit messages, changelogs, repo health, branch cleanup
- [agent-text-skills](https://github.com/megaartaiking-cmd/agent-text-skills) — Summarize text, extract keywords, readability, dedupe
- [agent-file-skills](https://github.com/megaartaiking-cmd/agent-file-skills) — Organize folders, find duplicates, batch rename
- [agent-sql-skills](https://github.com/megaartaiking-cmd/agent-sql-skills) — Explore SQLite, run queries, export to CSV
- [agent-video-skills](https://github.com/megaartaiking-cmd/agent-video-skills) — Edit video offline — trim, make Shorts, add titles, colour-grade
- [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — lightweight offline video editor for Windows 10

---

**Keywords:** agent skills, AI agent audio, audio editing skills, podcast trim, normalize volume, extract audio from video, Claude Code skills, Cursor skills, offline audio editor, ffmpeg CLI, lightweight audio editor
