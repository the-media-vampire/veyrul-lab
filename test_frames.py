import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import collect_frames
from collect_frames import collect, sha, verify_run_binding


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
        self.workflow = self.root / 'workflow.json'
        self.workflow.write_text(json.dumps({'sampler': {'seed': 2**53 - 1}, 'second': {'seed': 0}}))
        self.metadata = self.root / 'run.json'
        self.run = {'schema': 'veyrul-run-metadata/1',
                    'seeds': [{'pointer': '/sampler/seed', 'value': 2**53 - 1},
                              {'pointer': '/second/seed', 'value': 0}],
                    'workflow_sha256': sha(self.workflow),
                    'input_sha256': ['a' * 64],
                    'model': {'name': 'synthetic fixture, no model executed',
                              'weights': [{'name': 'not a real weight', 'sha256': 'b' * 64}]},
                    'runtime': {'engine': 'fixture', 'revision': 'test',
                                'node_versions': {'fixture': 'test'}, 'hardware': 'no GPU'}}
        self.metadata.write_text(json.dumps(self.run))

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
        self.assertEqual(r['run']['status'], 'not_supplied')

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

    def bound_receipt(self):
        out = self.root / 'bound'
        return out, collect(self.video, self.brief, out, self.metadata, self.workflow)

    def test_seed_boundaries_and_actual_cli_verification(self):
        out, r = self.bound_receipt()
        self.assertEqual([s['value'] for s in r['run']['seed_bindings']], [2**53 - 1, 0])
        self.assertEqual(r['run']['metadata_sha256'], sha(self.metadata))
        self.assertEqual(r['run']['workflow_sha256'], sha(self.workflow))
        self.assertEqual(r['run']['execution_status'], 'not_verified')
        self.assertEqual(r['run']['reproduction_status'], 'not_tested')
        result = subprocess.run(['python3', str(Path(collect_frames.__file__)),
                                 '--video', str(self.video), '--brief', str(self.brief),
                                 '--verify-evidence', str(out / 'EVIDENCE.json'),
                                 '--run-metadata', str(self.metadata), '--workflow', str(self.workflow)],
                                capture_output=True, text=True, timeout=10, check=True)
        self.assertEqual(json.loads(result.stdout)['run_binding'], 'matched')
        self.assertEqual(json.loads(result.stdout)['reproduction'], 'not_tested')

    def test_actual_collection_cli_writes_bound_receipt(self):
        out = self.root / 'cli-output'
        result = subprocess.run(['python3', str(Path(collect_frames.__file__)),
                                 '--video', str(self.video), '--brief', str(self.brief),
                                 '--output', str(out), '--run-metadata', str(self.metadata),
                                 '--workflow', str(self.workflow)], capture_output=True,
                                text=True, timeout=20, check=True)
        self.assertEqual(json.loads(result.stdout)['run_binding'], 'bound_to_receipt')
        receipt = json.loads((out / 'EVIDENCE.json').read_text())
        self.assertEqual(receipt['run']['seed_bindings'], self.run['seeds'])

    def test_input_only_cli_verification_and_changed_brief(self):
        before = (sha(self.video), sha(self.brief))
        out = self.root / 'input-only'
        collect(self.video, self.brief, out)
        args = ['python3', str(Path(collect_frames.__file__)),
                '--video', str(self.video), '--brief', str(self.brief),
                '--verify-evidence', str(out / 'EVIDENCE.json')]
        result = subprocess.run(args, capture_output=True, text=True,
                                timeout=10, check=True)
        verified = json.loads(result.stdout)
        self.assertEqual(verified['input_binding'], 'matched')
        self.assertEqual(verified['run_binding'], 'not_supplied')
        self.assertEqual(verified['reproduction'], 'not_tested')
        self.assertEqual(verified['editorial_review'], 'not_verified')
        amended = self.root / 'amended-brief.json'
        amended.write_bytes(self.brief.read_bytes() + b'\n')
        args[args.index('--brief') + 1] = str(amended)
        refused = subprocess.run(args, capture_output=True, text=True, timeout=10)
        self.assertEqual(refused.returncode, 1)
        self.assertIn('brief digest differs', refused.stderr)
        self.assertEqual(before, (sha(self.video), sha(self.brief)))

    def test_bound_receipt_cannot_omit_run_inputs(self):
        out, _ = self.bound_receipt()
        with self.assertRaisesRegex(ValueError, 'binding differs'):
            verify_run_binding(out / 'EVIDENCE.json', self.video, self.brief,
                               None, None)

    def test_input_only_receipt_cannot_claim_supplied_run_binding(self):
        out = self.root / 'input-only'
        collect(self.video, self.brief, out)
        with self.assertRaisesRegex(ValueError, 'binding differs'):
            verify_run_binding(out / 'EVIDENCE.json', self.video, self.brief,
                               self.metadata, self.workflow)

    def test_unsafe_or_noninteger_seed_refused_before_output(self):
        for value in (2**53, 9007199254740993, -1, True, 1.0, '1'):
            with self.subTest(seed=value):
                self.run['seeds'][0]['value'] = value
                self.metadata.write_text(json.dumps(self.run))
                with self.assertRaisesRegex(ValueError, 'integer from'):
                    collect(self.video, self.brief, self.root / 'bad', self.metadata, self.workflow)
                self.assertFalse((self.root / 'bad').exists())

    def test_seed_mismatch_and_missing_pointer_refused(self):
        for pointer, value in (('/sampler/seed', 42), ('/missing/seed', 42)):
            with self.subTest(pointer=pointer):
                self.run['seeds'][0] = {'pointer': pointer, 'value': value}
                self.metadata.write_text(json.dumps(self.run))
                with self.assertRaisesRegex(ValueError, 'differs|absent'):
                    collect(self.video, self.brief, self.root / 'bad', self.metadata, self.workflow)
                self.assertFalse((self.root / 'bad').exists())

    def test_changed_export_digest_refused(self):
        self.workflow.write_text('{"sampler":{"seed":42}}')
        with self.assertRaisesRegex(ValueError, 'workflow digest mismatch'):
            collect(self.video, self.brief, self.root / 'bad', self.metadata, self.workflow)
        self.assertFalse((self.root / 'bad').exists())

    def test_duplicate_json_property_refused(self):
        raw = self.metadata.read_text()
        self.metadata.write_text(raw.replace('"value": 9007199254740991',
                                              '"value": 42, "value": 9007199254740991', 1))
        with self.assertRaisesRegex(ValueError, 'duplicate JSON'):
            collect(self.video, self.brief, self.root / 'bad', self.metadata, self.workflow)
        self.assertFalse((self.root / 'bad').exists())

    def test_run_input_changed_during_collection_is_incomplete(self):
        original = collect_frames.command
        def change_after_decode(args):
            result = original(args)
            if args[0] == 'ffmpeg':
                self.metadata.write_text(self.metadata.read_text() + '\n')
            return result
        with patch('collect_frames.command', side_effect=change_after_decode):
            with self.assertRaisesRegex(ValueError, 'run input changed'):
                self.bound_receipt()
        self.assertFalse((self.root / 'bound' / 'EVIDENCE.json').exists())
        self.assertTrue((self.root / 'bound' / 'INCOMPLETE.txt').exists())

    def test_changed_clip_and_brief_fail_binding_check(self):
        out, _ = self.bound_receipt()
        for path, expected in ((self.video, 'video'), (self.brief, 'brief')):
            with self.subTest(changed=expected):
                original = path.read_bytes()
                path.write_bytes(original + b'changed')
                with self.assertRaisesRegex(ValueError, expected + ' digest differs'):
                    verify_run_binding(out / 'EVIDENCE.json', self.video, self.brief,
                                       self.metadata, self.workflow)
                path.write_bytes(original)

    def test_tampered_seed_receipt_fails_binding_check(self):
        out, r = self.bound_receipt()
        r['run']['seed_bindings'][0]['value'] = 42
        (out / 'EVIDENCE.json').write_text(json.dumps(r))
        with self.assertRaisesRegex(ValueError, 'binding differs'):
            verify_run_binding(out / 'EVIDENCE.json', self.video, self.brief,
                               self.metadata, self.workflow)

    def test_partial_metadata_input_refused(self):
        with self.assertRaisesRegex(ValueError, 'supplied together'):
            collect(self.video, self.brief, self.root / 'bad', self.metadata)
        self.assertFalse((self.root / 'bad').exists())


if __name__ == '__main__':
    unittest.main()
