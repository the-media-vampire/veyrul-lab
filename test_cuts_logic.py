import math, re, sys

FILL = {"um", "uh"}
PAD, MAXP, KEEP = 0.05, 0.5, 0.25
ROOM = max(PAD, KEEP / 2)

def gone(w):
    if w.get("drop", False): return True
    return re.sub(r"^[\W_]+|[\W_]+$", "", w["w"]).lower() in FILL

def validate(words, SR, N, OFF=0.0, TOL=0.25):
    DUR = N / SR
    ws = [{**w, "start": w["start"]+OFF, "end": w["end"]+OFF} for w in words]
    for w in ws:
        if not isinstance(w.get("w"), str) or not w["w"].strip(): raise ValueError(f"bad entry: {w}")
        if any(type(w.get(k)) not in (int,float) or not math.isfinite(w[k]) for k in ("start","end")): raise ValueError(f"non-finite: {w}")
        if type(w.get("drop", False)) is not bool: raise ValueError(f"drop not bool: {w}")
    for u,v in zip(ws, ws[1:]):
        if v["start"] < u["start"]: raise ValueError(f"out of order: {u['w']} / {v['w']}")
        if v["start"] < u["end"] - 0.01: raise ValueError(f"overlap >10 ms: {u['w']} / {v['w']}")
    for w in ws:
        if w["end"] <= w["start"]: raise ValueError(f"{w['w']} has no length")
        if w["start"] < -TOL or w["end"] > DUR+TOL: raise ValueError(f"{w['w']} outside file")
    for i,u in enumerate(ws):
        for v in ws[i+1:]:
            if v["start"] >= u["end"]: break
            if gone(u) != gone(v): raise ValueError(f"removed overlaps kept: {u['w']} / {v['w']}")
    return ws

def build_segments(ws):
    kept = [w for w in ws if not gone(w)]
    if not kept: raise ValueError("no words left")
    before = [w["end"] for w in ws if gone(w) and w["end"] <= kept[0]["start"]]
    s = max(0.0, kept[0]["start"]-PAD, *before)
    segs = []
    for a,b in zip(kept, kept[1:]):
        cut = [w for w in ws if a["end"]<=w["start"] and w["end"]<=b["start"] and gone(w)]
        if cut:
            e = min(a["end"]+ROOM, cut[0]["start"])
            n = max(b["start"]-ROOM, cut[-1]["end"])
        elif b["start"]-a["end"] > MAXP:
            e = a["end"]+KEEP/2; n = b["start"]-KEEP/2
        else:
            e = None
        if e is not None:
            segs.append((s, e)); s = n
    after = [w["start"] for w in ws if gone(w) and w["start"]>=kept[-1]["end"]]
    segs.append((s, min(kept[-1]["end"]+PAD, *after) if after else kept[-1]["end"]+PAD))
    return segs

def expected_samples(segs, SR, X):
    hard = sum(round(e*SR)-round(s*SR) for s,e in segs)
    return hard, hard - (len(segs)-1)*(X//2)

SR, N = 44_100, 441_000
X = (round(SR*0.01)//2)*2
WORDS = [
    {"w":"So",    "start":0.10,"end":0.35},
    {"w":"um",    "start":0.36,"end":0.60},
    {"w":"we",    "start":0.65,"end":0.90},
    {"w":"need",  "start":1.00,"end":1.40},
    {"w":"uh",    "start":2.35,"end":2.60},
    {"w":"to",    "start":2.65,"end":2.85},
    {"w":"start", "start":2.90,"end":3.30},
]

passed = failed = 0
def check(name, fn):
    global passed, failed
    try: fn(); print(f"  PASS  {name}"); passed += 1
    except Exception as e: print(f"  FAIL  {name}: {e}"); failed += 1
def expect(c, m):
    if not c: raise AssertionError(m)

print("=== filler-cut logic fixture ===")

check("validate accepts fixture", lambda: expect(len(validate(WORDS,SR,N))==7,"count"))

def t_gone():
    for w in ("um","Um,"," uh..."): expect(gone({"w":w}), w)
    for w in ("umbrella","uh-huh","umm"): expect(not gone({"w":w}), w)
    expect(gone({"w":"x","drop":True}), "explicit drop")
check("gone() filler rules", t_gone)

def t_segs():
    segs = build_segments(validate(WORDS,SR,N))
    expect(len(segs)>=2, f"{len(segs)} segments")
    for i,(s,e) in enumerate(segs): expect(e>s, f"seg {i} empty")
check("segments non-empty", t_segs)

def t_pause():
    segs = build_segments(validate(WORDS,SR,N))
    total = sum(e-s for s,e in segs)
    expect(total < N/SR*0.9, f"long pause not trimmed: {total:.2f}s of {N/SR}s")
check("long pause shortened", t_pause)

def t_samples():
    segs = build_segments(validate(WORDS,SR,N))
    hard, xf = expected_samples(segs, SR, X)
    expect(xf < hard, "xfade not < hard")
    nj = len(segs)-1
    expect(hard-xf == nj*(X//2), f"delta {hard-xf} != {nj}*{X//2}")
    print(f"         hard={hard} xfade={xf} joins={nj} X={X}")
check("sample math: delta = joins x X/2", t_samples)

def t_guard_overlap():
    bad=[{"w":"a","start":0.0,"end":0.5},{"w":"b","start":0.48,"end":0.9}]
    try: validate(bad,SR,N); raise AssertionError("no error")
    except ValueError as e: expect("overlap" in str(e).lower(), str(e))
check("guard: >10ms overlap rejected", t_guard_overlap)

def t_guard_mix():
    bad=[{"w":"So","start":0.0,"end":0.4},{"w":"um","start":0.3,"end":0.6}]
    try: validate(bad,SR,N); raise AssertionError("no error")
    except ValueError: pass
check("guard: removed-overlaps-kept rejected", t_guard_mix)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)