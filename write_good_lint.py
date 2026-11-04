"""write_good_lint.py
Report-only replica of eight write-good Vale rules.
Source: art_01M6JYTD4PWJ0G1JBGM1Z6QXQR r1 (Veyrul)
Levels: error > warning > suggestion — matches source table.
No rewrites are applied; author choices stay intact.
Usage: python write_good_lint.py <file.md>  OR  import and call lint(text).
"""
import re, sys
from dataclasses import dataclass
from typing import List

# ── Word/phrase lists (representative samples; real write-good lists are longer)
WEASEL_WORDS = {
    "clearly","completely","various","vast","very",
    "obviously","generally","simply","basically",
}
TOO_WORDY = {
    "a number of","abundance of","accede to","in order to",
    "due to the fact that","at this point in time",
}
CLICHES = {
    "at the end of the day","easier said than done",
    "bite the bullet","think outside the box",
    "back to the drawing board",
}

# ── Patterns
PASSIVE   = re.compile(r'\b(was|were|is|are|been|be)\s+\w+ed\b', re.I)
ILLUSIONS = re.compile(r'\b(\w+)\s+\1\b', re.I)
THERE_IS  = re.compile(r'^There (is|are)\b', re.I)
SO        = re.compile(r'^So\b', re.I)
EPRIME    = re.compile(r'\b(am|is|are|was|were|be|been|being)\b', re.I)


@dataclass
class Finding:
    rule:    str
    level:   str   # 'error' | 'warning' | 'suggestion'
    line:    int
    message: str


def lint(text: str) -> List[Finding]:
    """Return a list of Findings; never modifies text."""
    findings: List[Finding] = []
    for i, raw in enumerate(text.splitlines(), 1):
        low = raw.lower()

        # 1. Passive — warning
        m = PASSIVE.search(raw)
        if m:
            findings.append(Finding("Passive","warning",i,
                f"Possible passive voice: '{m.group()}'"))

        # 2. Weasel — warning
        for w in WEASEL_WORDS:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                findings.append(Finding("Weasel","warning",i,
                    f"Weasel word: '{w}'"))

        # 3. TooWordy — warning
        for phrase in TOO_WORDY:
            if phrase in low:
                findings.append(Finding("TooWordy","warning",i,
                    f"Too wordy: '{phrase}'"))

        # 4. ThereIs — error (case-sensitive per source)
        if THERE_IS.search(raw):
            findings.append(Finding("ThereIs","error",i,
                "Sentence opens with 'There is/are'"))

        # 5. So — error
        if SO.search(raw):
            findings.append(Finding("So","error",i,
                "Sentence opens with 'So'"))

        # 6. E-Prime — suggestion (forms of 'to be')
        m = EPRIME.search(raw)
        if m:
            findings.append(Finding("E-Prime","suggestion",i,
                f"Form of 'to be': '{m.group()}'"))

        # 7. Illusions (doubled words) — warning
        m = ILLUSIONS.search(raw)
        if m:
            findings.append(Finding("Illusions","warning",i,
                f"Repeated word: '{m.group()}'"))

        # 8. Cliches — warning
        for c in CLICHES:
            if c in low:
                findings.append(Finding("Cliches","warning",i,
                    f"Cliché: '{c}'"))

    return findings


def report(findings: List[Finding]) -> None:
    for f in findings:
        print(f"L{f.line:03d}  [{f.level:>10}]  {f.rule}: {f.message}")
    print(f"\n{len(findings)} finding(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python write_good_lint.py <file>")
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8").read()
    report(lint(text))