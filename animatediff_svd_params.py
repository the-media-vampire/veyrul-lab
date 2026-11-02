# AnimateDiff & SVD parameter comparison
# Source: art_01M6F0HYSTG2XTRQWZ10DDT2A9 r2 (stated, not tested)
# All values from record text; nothing is run or rendered here.

ANIMATEDIFF_VARIANTS = [
    {
        "name": "v1-5-3",
        "scheduler": "Euler Ancestral",
        "beta_schedule": "linear",
        "steps": 25,
        "cfg": 7.5,
        "frames": 16,
        "distilled": False,
        "licence": "none declared",
        "note": "v1-5-2 used DDIM; card does not explain scheduler change",
    },
    {
        "name": "Lightning 2-step",
        "scheduler": "Euler trailing timesteps",
        "beta_schedule": "linear",
        "steps": 2,
        "cfg": 1.0,
        "frames": None,
        "distilled": True,
        "licence": "creativeml-openrail-m",
        "note": "Authors tested 3 steps; CFG >1.0 may help some bases; LoRA at 0.7-0.8",
    },
    {
        "name": "Lightning 4-step",
        "scheduler": "Euler trailing timesteps",
        "beta_schedule": "linear",
        "steps": 4,
        "cfg": 1.0,
        "frames": None,
        "distilled": True,
        "licence": "creativeml-openrail-m",
        "note": "Authors rated highly; 576x1024 clips at 8s/30fps used in author tests",
    },
    {
        "name": "AnimateLCM",
        "scheduler": "LCMScheduler",
        "beta_schedule": "linear",
        "steps": "4-6",
        "cfg": 2.0,
        "frames": 16,
        "distilled": True,
        "licence": "none declared",
        "note": "Card says 4 steps; example uses 6. Source reads as range, not tested optimum. t2v LoRA at 0.8.",
    },
]

SVD_VARIANTS = [
    {
        "name": "SVD",
        "frames": 14,
        "resolution": "576x1024",
        "max_seconds": 4,
        "conditioning_fps": None,
        "motion_bucket_id": None,
        "text_control": False,
        "licence": "stable-video-diffusion-community (research only)",
        "limits": "static output or slow pans; no legible text; watermarked by default",
    },
    {
        "name": "SVD-XT",
        "frames": 25,
        "resolution": "576x1024",
        "max_seconds": 4,
        "conditioning_fps": None,
        "motion_bucket_id": None,
        "text_control": False,
        "licence": "stable-video-diffusion-community (non-commercial + research)",
        "limits": "short clips; no motion or slow pan; no legible text",
    },
    {
        "name": "SVD 1.1",
        "frames": 25,
        "resolution": "1024x576",
        "max_seconds": 4,
        "conditioning_fps": 6,
        "motion_bucket_id": 127,
        "text_control": False,
        "licence": "stable-video-diffusion-community",
        "limits": "imperfect photorealism; outside defaults may be worse than 1.0; no legible text",
    },
]


def print_animatediff_table():
    print("AnimateDiff variants (source: art_01M6F0HYSTG2XTRQWZ10DDT2A9 r2)")
    print(f"{'Name':<20} {'Scheduler':<26} {'Steps':<7} {'CFG':<5} {'Frames'}")
    print("-" * 68)
    for v in ANIMATEDIFF_VARIANTS:
        print(f"{v['name']:<20} {v['scheduler']:<26} {str(v['steps']):<7} {v['cfg']:<5} {str(v['frames'])}")


def print_step_ratios(baseline_steps=25):
    print(f"\nStep ratios vs baseline ({baseline_steps} steps)")
    for v in ANIMATEDIFF_VARIANTS:
        if isinstance(v["steps"], int):
            r = v["steps"] / baseline_steps
            print(f"  {v['name']:<20} {v['steps']:>2} steps = {r:.2f}x ({(1-r)*100:.0f}% fewer)")
        else:
            print(f"  {v['name']:<20} {v['steps']} steps (range)")


def print_svd_table():
    print("\nSVD variants")
    print(f"{'Model':<10} {'Frames':<8} {'Res':<12} {'Cond FPS':<10} {'MBId':<6} Licence")
    print("-" * 68)
    for s in SVD_VARIANTS:
        print(f"{s['name']:<10} {s['frames']:<8} {s['resolution']:<12} "
              f"{str(s['conditioning_fps']):<10} {str(s['motion_bucket_id']):<6} {s['licence']}")


def check_consistency():
    print("\nDocumented notes and ambiguities")
    for v in ANIMATEDIFF_VARIANTS:
        if v["note"]:
            print(f"  {v['name']}: {v['note']}")


if __name__ == "__main__":
    print_animatediff_table()
    print_step_ratios()
    print_svd_table()
    check_consistency()