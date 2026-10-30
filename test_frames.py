import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from collect_frames import collect, sha


class Frames(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='veyrul-frame-test-')
        self.root = Path(self.temp.name)
        self.brief = self.root / 'brief.json'
        self.brief.write_text(json.dumps({'synthetic_fixture': True}))
        self.video = self.root / 'fixture.mkv'
        # Synthetic decoder fixture: blue endpoints, a red box only at frame5.
        subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'lavfi',
                        '-i', 'color=c=blue:s=64x36:r=10:d=1', '-vf',
                        "drawbox=x=10:y=10:w=20:h=10:color=red:t=fill:enable='eq(n,5)'",
                        '-c:v', 'ffv1', str(self.video)], check=True, timeout=20)

    def tearDown(self):
        self.temp.cleanup()  # Only this test's disposable synthetic fixtures.

    def test_middle_event_and_timestamps(self):
        r = collect(self.video, self.brief, self.root / 'out')
        self.assertEqual(r['decoded_frames'], 10)
        f = r['frames']
        self.assertEqual(f[0]['sha256'], f[-1]['sha256'])
        self.assertNotEqual(f[5]['sha256'], f[0]['sha256'])
        self.assertAlmostEqual(f[5]['relative_time_seconds'], .5)
        self.assertEqual(r['review']['source_fidelity'], 'unknown')

    def test_preserves_original_inputs(self):
        before = (sha(self.video), sha(self.brief))
        collect(self.video, self.brief, self.root / 'out')
        self.assertEqual(before, (sha(self.video), sha(self.brief)))

    def test_existing_output_refused(self):
        out = self.root / 'out'
        out.mkdir()
        (out / 'keep').write_text('preserve')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            collect(self.video, self.brief, out)
        self.assertEqual((out / 'keep').read_text(), 'preserve')

    def test_missing_input_refused_before_output(self):
        out = self.root / 'out'
        with self.assertRaisesRegex(ValueError, 'existing local files'):
            collect(self.root / 'missing.mkv', self.brief, out)
        self.assertFalse(out.exists())

    def test_long_clip_refused_before_output(self):
        long = self.root / 'long.mkv'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        'color=c=blue:s=64x36:r=1:d=11', '-c:v', 'ffv1', str(long)],
                       check=True, timeout=20)
        out = self.root / 'out'
        with self.assertRaisesRegex(ValueError, '10 seconds'):
            collect(long, self.brief, out)
        self.assertFalse(out.exists())

    def test_frame_ceiling_refused_before_output(self):
        many = self.root / 'many.mkv'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        'color=c=blue:s=64x36:r=30:d=9', '-c:v', 'ffv1', str(many)],
                       check=True, timeout=20)
        out = self.root / 'out'
        with self.assertRaisesRegex(ValueError, '241 frames'):
            collect(many, self.brief, out)
        self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
