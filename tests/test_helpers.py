from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/video-editing-starter/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg tools required')
class MediaChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='video-skill-check-')
        cls.folder = Path(cls.temp.name)
        cls.video = cls.folder / 'sample.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        'color=c=navy:s=320x180:r=24:d=1', '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p', '-y', str(cls.video)], check=True)
        cls.original = hashlib.sha256(cls.video.read_bytes()).hexdigest()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_inventory_preserves_source_and_ignores_nonmedia(self):
        (self.folder / '.env').write_text('test-only-placeholder', encoding='utf-8')
        result = load('media_inventory').inventory(self.folder)
        self.assertEqual([m['file'] for m in result['media']], ['sample.mp4'])
        self.assertEqual(result['media'][0]['sha256'], self.original)
        self.assertEqual(hashlib.sha256(self.video.read_bytes()).hexdigest(), self.original)

    def test_valid_export_and_caption_pass(self):
        srt = self.folder / 'valid.srt'
        srt.write_text('1\n00:00:00,000 --> 00:00:00,800\nA permitted caption.\n', encoding='utf-8')
        result = load('check_export').check_export(self.video, srt, 320, 180, '24')
        self.assertTrue(result['passed'], result['errors'])

    def test_out_of_bounds_caption_is_rejected(self):
        srt = self.folder / 'outside.srt'
        srt.write_text('1\n00:00:00,100 --> 00:00:02,000\nToo long.\n', encoding='utf-8')
        result = load('check_export').check_export(self.video, srt)
        self.assertFalse(result['passed'])
        self.assertTrue(any('beyond' in e for e in result['errors']))

    def test_wrong_dimensions_and_missing_required_audio_are_rejected(self):
        result = load('check_export').check_export(self.video, width=1080, require_audio=True)
        self.assertFalse(result['passed'])
        self.assertEqual(len(result['errors']), 2)

    def test_report_cannot_overwrite_source(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'media_inventory.py'),
                                 str(self.video), '--out', str(self.video)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(hashlib.sha256(self.video.read_bytes()).hexdigest(), self.original)

    def test_corrupt_file_fails_cli(self):
        broken = self.folder / 'broken.bin'
        broken.write_bytes(b'not a video')
        result = subprocess.run([sys.executable, str(SCRIPTS / 'check_export.py'), str(broken)],
                                capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
