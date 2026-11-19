---
name: audio-edit
description: Trim audio, normalize volume, and extract audio from video, offline, with ffmpeg. Use when the user or agent wants to cut a podcast clip, even out volume, or pull audio out of a video file.
---

# Audio Edit

Do the common audio jobs without a DAW. Trim a clip, normalize volume
to podcast level, or extract the audio track from a video.
No cloud, no upload. Files stay local.

## When to use

- "Trim this podcast to 30–90 seconds"
- "Normalize the volume of this recording"
- "Extract the audio from this video"

## Workflow

1. Check ffmpeg is installed:
   ```sh
   python tools/audiotool.py check
   ```
   If it is missing, tell the user how to install it (`winget install ffmpeg` on Windows, `brew install ffmpeg` on macOS, `sudo apt install ffmpeg` on Linux) and stop.
2. Trim — fast copy first:
   ```sh
   python tools/audiotool.py trim podcast.mp3 clip.mp3 --start 30 --end 90
   ```
   Add `--reencode` if the cut lands on the wrong frame.
3. Normalize volume to -16 LUFS (podcast level):
   ```sh
   python tools/audiotool.py normalize quiet.mp3 loud.mp3
   ```
4. Extract audio from video:
   ```sh
   python tools/audiotool.py extract video.mp4 audio.mp3
   ```
5. Confirm the output file exists and report its path and length.

## Examples

**A 30-second clip from a podcast**
```sh
python tools/audiotool.py trim episode.mp3 teaser.mp3 --start 120 --end 150
# Saved: teaser.mp3  (120.0s to 150.0s)
```

**Even out a quiet recording**
```sh
python tools/audiotool.py normalize interview.mp3 interview-loud.mp3
# Saved: interview-loud.mp3  (normalized to -16 LUFS)
```

**Audio-only version of a video**
```sh
python tools/audiotool.py extract talk.mp4 talk.mp3
# Saved: talk.mp3  (audio extracted from talk.mp4)
```

## Rules

- Never overwrite the input file. Always write to a new output file.
- Keep the original audio unless the user asks to remove it.
- Normalizing changes the loudness of the whole file — do it on a copy, and say the target level (-16 LUFS).
- If the input is not an audio or video file, say so and stop.
- For very low-memory PCs, prefer the fast trim (no `--reencode`) first.
