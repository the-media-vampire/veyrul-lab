# Stage-level evidence-quality audit for the book-trailer pipeline
# Source: art_01M6H5ADPZ1P46TM3CRGGYVTJK rev 2 (documentary, nothing run)
# Companion to Theo artifact f69a8a88 commit ec79266e
#
# Evidence labels (from the pipeline record's own framing):
#   SC = source/platform claim   CR = creator-reported (incl. sponsored demo)
#   DR = desk-reading of repo/paper/terms   CS = clip-study (sampled stills)
# Rank: CS=3  DR=2  SC=1  CR=0  (higher = stronger recoverable basis)

STAGES = [
    {"n":1, "label":"Shot plan / continuity ledger",
     "ev":["CR"], "rank":0,
     "gap":"Ledger design is a synthesis; sponsored-agent claim unverified."},
    {"n":2, "label":"Reference stills",
     "ev":["CR","SC"], "rank":1,
     "gap":"Illustration rights not covered. GAP-A: last-frame export format unspecified."},
    {"n":3, "label":"Image-to-video from first frame",
     "ev":["CS"], "rank":3,
     "gap":"CS found rules that did not hold (lighting, person count)."},
    {"n":4, "label":"Invented-event check",
     "ev":["CS"], "rank":3,
     "gap":"No video run; collector checks only."},
    {"n":5, "label":"Camera-move vocabulary",
     "ev":["DR","SC"], "rank":2,
     "gap":"Two wording styles untested side by side; validation on synthetic scenes only."},
    {"n":6, "label":"Sound effects",
     "ev":["DR"], "rank":2,
     "gap":"MMAudio checkpoints CC-BY-NC 4.0 (not MIT). Alignment drift reported, not measured."},
    {"n":7, "label":"Music licence / loudness",
     "ev":["DR","SC"], "rank":2,
     "gap":"One provider only. Loudness is 2015 cinema snapshot; no online target. GAP-B."},
    {"n":8, "label":"Edit structure",
     "ev":["CR","DR"], "rank":2,
     "gap":"Two sources disagree on split-edit frequency; no audience measurement."},
    {"n":9, "label":"Publishing labels / trailer slot",
     "ev":["SC"], "rank":1,
     "gap":"Meta wording unverified. No measurable realism threshold. GAP-C."},
]

def report():
    print(f"{'N':<3} {'Stage':<34} {'Ev':<8} {'Rank':<5} Gap (excerpt)")
    print("-" * 90)
    for s in STAGES:
        print(f"{s['n']:<3} {s['label']:<34} {'/'.join(s['ev']):<8} {s['rank']:<5} {s['gap'][:48]}")
    weak = [s['n'] for s in STAGES if s['rank'] < 2]
    print(f"\nStages with rank < DR (weakest basis): {weak}")
    print("These carry the highest recovery risk for a future agent.")

if __name__ == "__main__":
    report()