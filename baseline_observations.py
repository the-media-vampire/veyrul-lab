"""Four clips from art_01M6A19D9WCBJFN6YNNXNTP570 r2. Stills only, no playback."""
from frame_rule_checker import Rule, FrameObs, score_clip
from collections import Counter

# HF-PKG-007 Extend clip (higgsfield.ai/@pandaproduction/projects/thread)
r007 = [Rule("007-R1","layout and staging kept","boolean",True),
        Rule("007-R2","colour-state rule held","boolean",True),
        Rule("007-R3","hands match written state","boolean",True),
        Rule("007-R4","named mirror in final frame","boolean",True)]
o007 = [FrameObs("007-R1",True,"clear"),FrameObs("007-R2",False,"clear"),
        FrameObs("007-R3",False,"partial"),FrameObs("007-R4",True,"clear")]

# HF-PKG-011 20s clip (higgsfield.ai/@allan_ripley/projects/the-prompter)
r011 = [Rule("011-R1","exactly one person in first frame","exact",1),
        Rule("011-R2","mouth closed in first frame","boolean",True),
        Rule("011-R3","last-frame failed-take conditions met","boolean",True)]
o011 = [FrameObs("011-R1",2,"clear"),FrameObs("011-R2",False,"partial"),
        FrameObs("011-R3",True,"clear")]

# HF-PKG-014 vertical clip (higgsfield.ai/@seeyousoonx/projects/azul-cobalto)
r014 = [Rule("014-R1","no lid on prop","boolean",False)]
o014 = [FrameObs("014-R1",True,"clear")]

# HF-PKG-022 three-shot edit (higgsfield.ai/@higgsfield.commercials/projects/inside-ai-commercial)
r022 = [Rule("022-R1","room not brightly lit","boolean",False),
        Rule("022-R2","cast lists held","boolean",True),
        Rule("022-R3","blocking relative to prop held","boolean",True)]
o022 = [FrameObs("022-R1",True,"clear"),FrameObs("022-R2",True,"clear"),
        FrameObs("022-R3",True,"clear")]

if __name__ == "__main__":
    clips = [("HF-PKG-007",r007,o007),("HF-PKG-011",r011,o011),
             ("HF-PKG-014",r014,o014),("HF-PKG-022",r022,o022)]
    verdicts = []
    for cid,rules,obs in clips:
        for row in score_clip(rules,obs):
            print(f"{cid} {row['rule_id']} {row['description'][:42]:<44} {row['verdict']}")
            verdicts.append(row['verdict'])
    print("Summary:", dict(Counter(verdicts)))