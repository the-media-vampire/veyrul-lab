import json

# Minimal model of the ink runtime API documented at:
# art_01M6CFFV3P2X8HW39BHHK0H0W5 rev 2 (inkle/ink commit 35c63e52)
# Loop: Continue while canContinue → list currentChoices → ChooseChoiceIndex
# JSON format uses top-level fields: inkVersion, root

class InkStory:
    """Minimal ink runtime API model. Not a full ink engine."""
    def __init__(self, json_string):
        data = json.loads(json_string)
        self.inkVersion = data["inkVersion"]
        self._passages = data["root"]["passages"]
        self._current = 0
        self._text_buffer = []
        self._done = False

    def Continue(self):
        """Advance and return the next line of content."""
        passage = self._passages[self._current]
        self._text_buffer = [passage["text"]]
        self._choices = passage.get("choices", [])
        if not self._choices:
            self._done = True
        return self._text_buffer[0]

    @property
    def canContinue(self):
        """True when there is content to read before choices must be made."""
        return not self._done and len(self._text_buffer) == 0

    @property
    def currentChoices(self):
        return self._choices

    def ChooseChoiceIndex(self, index):
        """Provide the player's choice by zero-based index."""
        choice = self._choices[index]
        self._current = choice["next"]
        self._text_buffer = []


def run_story(story, choice_fn):
    """Drive the loop: choice_fn(choices) -> int index."""
    while True:
        text = story.Continue()
        print(text)
        choices = story.currentChoices
        if not choices:
            break
        idx = choice_fn(choices)
        story.ChooseChoiceIndex(idx)