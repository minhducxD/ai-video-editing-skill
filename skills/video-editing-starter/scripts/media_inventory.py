#!/usr/bin/env python3
"""Inspect selected local media and hash originals without modifying them."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

MEDIA = {'.mp4', '.mov', '.mkv', '.webm', '.avi', '.wav', '.mp3', '.m4a', '.aac', '.flac'}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def inventory(source: Path, recursive: bool = False) -> dict:
    probe = shutil.which('ffprobe')
    if not probe:
        raise RuntimeError('ffprobe is required but was not found on PATH.')
    source = source.resolve(strict=True)
    if source.is_file():
        if source.suffix.lower() not in MEDIA:
            raise ValueError('Select a supported media file or a directory of media files.')
        files, base = [source], source.parent
    else:
        entries = source.rglob('*') if recursive else source.iterdir()
        files = sorted(p for p in entries if p.is_file() and p.suffix.lower() in MEDIA)
        base = source
    if not files:
        raise ValueError('No supported media files were found in the selected location.')
    rows = []
    for path in files:
        result = subprocess.run([
            probe, '-v', 'error', '-show_entries',
            'stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels,duration:format=duration',
            '-of', 'json', str(path),
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
        data = json.loads(result.stdout)
        rows.append({
            'file': path.relative_to(base).as_posix(),
            'bytes': path.stat().st_size,
            'sha256': digest(path),
            'duration_seconds': float(data.get('format', {}).get('duration', 0)),
            'streams': data.get('streams', []),
        })
    return {'schema_version': 1, 'media': rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--recursive', action='store_true', help='Include media in subdirectories.')
    parser.add_argument('--out', type=Path, help='Create a new JSON report; never overwrite a file.')
    args = parser.parse_args()
    try:
        data = inventory(args.source, args.recursive)
        text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        if args.out:
            with args.out.open('x', encoding='utf-8') as stream:
                stream.write(text)
        else:
            print(text, end='')
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f'Inventory failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
