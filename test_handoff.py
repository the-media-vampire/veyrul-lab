"""No downloads/renders: pass a local copy of the pinned official template."""
import base64, copy, hashlib, importlib.util, json, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("handoff", HERE / "wan_ui_handoff.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
template = pathlib.Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(template).hexdigest() == helper.TEMPLATE_SHA256
graph = json.loads(template)
# An original synthetic single-pixel fixture; no founder or third-party image.
pixel = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl2L9sAAAAASUVORK5CYII=")
frame = {"sha256": hashlib.sha256(pixel).hexdigest(), "source_record": "SYNTHETIC",
         "source_revision": 1, "experiment_id": "fixture", "frame_locator": "synthetic pixel",
         "attestation": {"adaptation_and_likeness_cleared": True, "operator": "Veyrul Main",
                         "basis": "synthetic fixture", "evidence_ref": "test_handoff.py",
                         "attested_at": "2026-10-30"}, "_bytes": pixel}
checks = []
def reject(name, g=graph, f=frame, image="fixture.png", seed=42):
    try: helper.patch(copy.deepcopy(g), image, copy.deepcopy(f), seed, "slow push in")
    except (ValueError, KeyError): checks.append(name)
    else: raise AssertionError("accepted " + name)

with tempfile.TemporaryDirectory(prefix="veyrul-handoff-") as directory:
    root = pathlib.Path(directory)
    (root / "template.json").write_bytes(template)
    (root / "fixture.png").write_bytes(pixel)
    (root / "frame.json").write_text(json.dumps({k:v for k,v in frame.items() if k != "_bytes"}))
    command = [sys.executable, str(HERE / "wan_ui_handoff.py"), "--workflow", str(root / "template.json"),
               "--image", str(root / "fixture.png"), "--frame", str(root / "frame.json"), "--seed", "42",
               "--prompt", "slow push in", "--output", str(root / "result.json")]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    out = json.loads((root / "result.json").read_text())
    expected = copy.deepcopy(graph)
    nodes = {node["id"]:node for node in expected["nodes"]}
    nodes[56]["mode"] = 0
    nodes[56]["widgets_values"][0] = "fixture.png"
    nodes[3]["widgets_values"][:2] = [42, "fixed"]
    nodes[6]["widgets_values"][0] = "slow push in"
    assert out == expected, "unexpected graph changes"
    assert "render_not_run" in result.stdout
    checks.append("actual CLI: pinned upstream graph, exact four intended edits, render not run")
    saved = (root / "result.json").read_bytes()
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert (root / "result.json").read_bytes() == saved
    checks.append("existing output preserved")
    (root / "template.json").write_bytes(template + b" ")
    command[-1] = str(root / "drift.json")
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert not (root / "drift.json").exists()
    checks.append("unsupported template bytes rejected before output")

f = copy.deepcopy(frame); f["sha256"] = "0" * 64; reject("frame digest mismatch", f=f)
f = copy.deepcopy(frame); f["attestation"]["adaptation_and_likeness_cleared"] = False; reject("uncleared attestation", f=f)
reject("Windows path separator", image="..\\fixture.png")
reject("negative seed", seed=-1)
reject("unsafe JavaScript seed", seed=9007199254740993)
safe = helper.patch(graph, "fixture.png", copy.deepcopy(frame), 9007199254740991, "slow push in")
assert next(n for n in safe["nodes"] if n["id"] == 3)["widgets_values"][0] == 9007199254740991
checks.append("maximum JavaScript-safe seed preserved")
g = copy.deepcopy(graph); g["nodes"].append(copy.deepcopy(g["nodes"][0])); reject("duplicate node ID", g=g)
g = copy.deepcopy(graph)
for edge in g["links"]:
    if edge[1] == 56 and edge[3] == 55: edge[1] = 99
reject("wrong image connection", g=g)
before = copy.deepcopy(frame); helper.patch(graph, "fixture.png", frame, 42, "slow push in")
assert frame == before
checks.append("caller frame metadata preserved")
print(json.dumps({"passed":len(checks), "failed":0, "checks":checks,
                  "template_sha256":helper.TEMPLATE_SHA256, "rendered":False}, indent=2))
