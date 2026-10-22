#!/usr/bin/env python3
"""Check local video decoding, optional format expectations and SRT timing."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

TIMING = re.compile(r'^(\d{2,}):(\d{2}):(\d{2})[,\.](\d{3})\s+-->\s+(\d{2,}):(\d{2}):(\d{2})[,\.](\d{3})\s*$')


def seconds(parts: tuple[str, ...]) -> float:
    hour, minute, second, milli = map(int, parts)
    if minute >= 60 or second >= 60:
        raise ValueError('Caption minutes and seconds must be below 60.')
    return hour * 3600 + minute * 60 + second + milli / 1000


def check_srt(path: Path, duration: float) -> dict:
    errors, warnings = [], []
    blocks = re.split(r'\n\s*\n', path.read_text(encoding='utf-8-sig').replace('\r\n', '\n').strip())
    previous_start, previous_end, count = -1.0, -1.0, 0
    for number, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if not lines:
            continue
        if len(lines) < 3 or not lines[0].strip().isdigit():
            errors.append(f'Block {number}: missing cue number, timing or text.')
            continue
        match = TIMING.fullmatch(lines[1].strip())
        if not match:
            errors.append(f'Block {number}: invalid SRT timing.')
            continue
        try:
            start, end = seconds(match.groups()[:4]), seconds(match.groups()[4:])
        except ValueError as error:
            errors.append(f'Block {number}: {error}')
            continue
        if start >= end:
            errors.append(f'Block {number}: cue must have a positive duration.')
        if start < previous_start:
            errors.append(f'Block {number}: cue starts are not ordered.')
        if start < previous_end:
            warnings.append(f'Block {number}: overlap with the preceding cue; review intent.')
        if end > duration + 0.1:
            errors.append(f'Block {number}: cue ends beyond the video duration.')
        if not any(line.strip() for line in lines[2:]):
            errors.append(f'Block {number}: empty caption text.')
        previous_start, previous_end = start, end
        count += 1
    if not count:
        errors.append('No valid caption cues were found.')
    return {'cues': count, 'errors': errors, 'warnings': warnings}


def check_export(video: Path, srt: Path | None = None, width: int | None = None,
                 height: int | None = None, fps: str | None = None,
                 require_audio: bool = False) -> dict:
    probe, ffmpeg = shutil.which('ffprobe'), shutil.which('ffmpeg')
    if not probe or not ffmpeg:
        raise RuntimeError('ffmpeg and ffprobe are required on PATH.')
    video = video.resolve(strict=True)
    info = subprocess.run([probe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)],
                          capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
    data = json.loads(info.stdout)
    streams = data.get('streams', [])
    picture = next((stream for stream in streams if stream.get('codec_type') == 'video'), None)
    if picture is None:
        raise ValueError('The selected file has no video stream.')
    duration = float(data.get('format', {}).get('duration', picture.get('duration', 0)))
    actual_fps = float(Fraction(picture.get('avg_frame_rate') or picture.get('r_frame_rate', '0/1')))
    errors = []
    if duration <= 0:
        errors.append('Video duration is not positive.')
    if width is not None and picture['width'] != width:
        errors.append(f'Width is {picture["width"]}, expected {width}.')
    if height is not None and picture['height'] != height:
        errors.append(f'Height is {picture["height"]}, expected {height}.')
    if fps is not None and abs(actual_fps - float(Fraction(fps))) > 0.001:
        errors.append(f'Frame rate is {actual_fps:g}, expected {fps}.')
    audio_present = any(stream.get('codec_type') == 'audio' for stream in streams)
    if require_audio and not audio_present:
        errors.append('An audio stream was required but is absent.')
    decoded = subprocess.run([ffmpeg, '-v', 'error', '-i', str(video), '-f', 'null', '-'],
                             capture_output=True, text=True, encoding='utf-8', errors='replace')
    if decoded.returncode or decoded.stderr.strip():
        errors.append('Decode reported an error: ' + decoded.stderr.strip()[-1000:])
    captions = check_srt(srt, duration) if srt else None
    if captions:
        errors.extend(captions['errors'])
    return {'passed': not errors, 'duration_seconds': duration,
            'width': picture['width'], 'height': picture['height'], 'fps': actual_fps,
            'audio_present': audio_present, 'full_decode': 'passed' if not decoded.returncode and not decoded.stderr.strip() else 'failed',
            'captions': captions, 'errors': errors,
            'scope': 'Technical and timing checks only; not factual, visual, linguistic or listening approval.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--srt', type=Path)
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--fps')
    parser.add_argument('--require-audio', action='store_true')
    parser.add_argument('--json-out', type=Path, help='Create a new report; never overwrite a file.')
    args = parser.parse_args()
    try:
        result = check_export(args.video, args.srt, args.width, args.height, args.fps, args.require_audio)
        text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        if args.json_out:
            with args.json_out.open('x', encoding='utf-8') as stream:
                stream.write(text)
        print(text, end='')
        return 0 if result['passed'] else 1
    except (OSError, ValueError, RuntimeError, ZeroDivisionError, subprocess.CalledProcessError) as error:
        print(f'Export check failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
