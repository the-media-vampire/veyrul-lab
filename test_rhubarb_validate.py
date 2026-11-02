"""Inline tests for rhubarb_validate.py.

Run: python test_rhubarb_validate.py
"""
import json
from rhubarb_validate import validate_tsv, validate_xml, validate_json

GOOD_TSV = "0.00\tA\n0.35\tB\n0.72\tX\n1.10\tX\n"
BAD_TSV_NO_ZERO = "0.05\tA\n0.35\tB\n1.10\tX\n"
BAD_TSV_SHAPE   = "0.00\tA\n0.35\tZ\n1.10\tX\n"

GOOD_XML = """<rhubarbResult>
  <metadata><soundFile>r.wav</soundFile><duration>1.10</duration></metadata>
  <mouthCue start=\"0.00\" end=\"0.35\" value=\"A\"/>
  <mouthCue start=\"0.35\" end=\"0.72\" value=\"B\"/>
  <mouthCue start=\"0.72\" end=\"1.10\" value=\"X\"/>
</rhubarbResult>"""
BAD_XML_GAP = """<rhubarbResult>
  <mouthCue start=\"0.00\" end=\"0.35\" value=\"A\"/>
  <mouthCue start=\"0.40\" end=\"1.10\" value=\"X\"/>
</rhubarbResult>"""

GOOD_JSON = json.dumps({"metadata":{},"mouthCues":[
    {"start":0.00,"end":0.35,"value":"A"},
    {"start":0.35,"end":0.72,"value":"B"},
    {"start":0.72,"end":1.10,"value":"X"}]})
BAD_JSON_SHAPE = json.dumps({"metadata":{},"mouthCues":[
    {"start":0.0,"end":0.5,"value":"A"},
    {"start":0.5,"end":1.0,"value":"Q"}]})

passed = failed = 0
def chk(name, issues, expect_empty):
    global passed, failed
    ok = (len(issues) == 0) == expect_empty
    status = "PASS" if ok else "FAIL"
    if ok: passed += 1
    else:  failed += 1
    print(f"{status}  {name}  {issues or 'none'}")

chk("TSV valid",       validate_tsv(GOOD_TSV),       True)
chk("TSV no-zero",     validate_tsv(BAD_TSV_NO_ZERO), False)
chk("TSV bad shape",   validate_tsv(BAD_TSV_SHAPE),   False)
chk("XML valid",       validate_xml(GOOD_XML),        True)
chk("XML gap",         validate_xml(BAD_XML_GAP),     False)
chk("JSON valid",      validate_json(GOOD_JSON),       True)
chk("JSON bad shape",  validate_json(BAD_JSON_SHAPE),  False)
print(f"\n{passed}/{passed+failed} passed")