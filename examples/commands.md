# Example commands

Any `.mp3` or `.mp4` file works with these commands. No sample audio is
committed to this repo — generate a test file with ffmpeg, or use your own:

```sh
# Make a 5-second test tone with ffmpeg
ffmpeg -f lavfi -i "sine=frequency=440:duration=5" -c:a libmp3lame test.mp3

# Check ffmpeg is ready
python tools/audiotool.py check

# Trim 1–3 seconds (fast copy)
python tools/audiotool.py trim test.mp3 clip.mp3 --start 1 --end 3

# Trim with re-encoding (frame-accurate)
python tools/audiotool.py trim test.mp3 clip.mp3 --start 1 --end 3 --reencode

# Normalize volume to -16 LUFS (podcast level)
python tools/audiotool.py normalize test.mp3 loud.mp3

# Extract audio from a video file
python tools/audiotool.py extract video.mp4 audio.mp3
```
