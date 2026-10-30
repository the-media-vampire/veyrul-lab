import argparse, copy, hashlib, json
from pathlib import Path

TEMPLATE_SHA256 = "23c93b88adecbdf5bcf4c5438117070fe757f30aca373dd6a2eb488d2c6a585a"

def patch(g, image, frame, seed, prompt):
    # This is an editor-workflow patch, NOT a ComfyUI API prompt.
    if type(seed) is not int or not 0 <= seed <= 2**53 - 1:
        raise ValueError("seed must be a JavaScript-safe integer from 0 to 9007199254740991")
    if Path(image).name != image or image in ("", ".", "..") or "/" in image or "\\" in image:
        raise ValueError("use a staged ComfyUI input basename")
    if not prompt.strip():
        raise ValueError("empty prompt")
    if frame.get("sha256") != hashlib.sha256(frame["_bytes"]).hexdigest():
        raise ValueError("frame hash mismatch")
    a = frame.get("attestation", {})
    if a.get("adaptation_and_likeness_cleared") is not True or not all(
        isinstance(a.get(k), str) and a[k].strip()
        for k in ("operator", "basis", "evidence_ref", "attested_at")
    ):
        raise ValueError("missing attributable rights attestation")
    if not all(frame.get(k) for k in ("source_record", "source_revision", "experiment_id", "frame_locator")):
        raise ValueError("missing frame lineage")
    out = copy.deepcopy(g)
    nodes = {n["id"]: n for n in out["nodes"]}
    if len(nodes) != len(out["nodes"]): raise ValueError("duplicate node ID")
    expected = {56:"LoadImage",55:"Wan22ImageToVideoLatent",3:"KSampler",6:"CLIPTextEncode",57:"CreateVideo"}
    for i, t in expected.items():
        if nodes[i]["type"] != t: raise ValueError("template node drift")
    link = next(x for x in nodes[55]["inputs"] if x["name"] == "start_image")["link"]
    if [link,56,0,55,1,"IMAGE"] not in out["links"]:
        raise ValueError("start_image edge drift")
    if any(x.get("link") is not None for x in nodes[57]["inputs"] if x["name"] == "audio"):
        raise ValueError("audio must stay disconnected")
    if len(nodes[3]["widgets_values"]) != 7: raise ValueError("sampler widget drift")
    nodes[56]["mode"] = 0
    nodes[56]["widgets_values"][0] = image
    nodes[3]["widgets_values"][:2] = [seed,"fixed"]
    nodes[6]["widgets_values"][0] = prompt
    return out

def main():
    p = argparse.ArgumentParser()
    for name in ("workflow","image","frame","seed","prompt","output"):
        p.add_argument("--"+name, required=True, type=int if name=="seed" else str)
    a = p.parse_args()
    workflow = Path(a.workflow).read_bytes()
    if hashlib.sha256(workflow).hexdigest() != TEMPLATE_SHA256:
        raise ValueError("unsupported template bytes; fetch the pinned upstream template")
    f = json.loads(Path(a.frame).read_text())
    f["_bytes"] = Path(a.image).read_bytes()
    result = patch(json.loads(workflow), Path(a.image).name, f, a.seed, a.prompt)
    with Path(a.output).open("x") as output:
        output.write(json.dumps(result, indent=2))
    print("patched_ui_only; render_not_run; weight_licenses_unresolved")

if __name__ == "__main__": main()
