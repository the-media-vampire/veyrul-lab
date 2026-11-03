"""English pronoun substitution only; not semantic coreference resolution."""
import re
PRONOUNS = {'he','she','they','him','her','them','his','their'}

def rewrite(text, mapping):
    normalized = {}
    for key, value in mapping.items():
        key = key.casefold()
        if key not in PRONOUNS or not value.strip():
            raise ValueError('invalid mapping')
        if key in normalized and normalized[key] != value:
            raise ValueError('conflicting mapping')
        normalized[key] = value
    pattern = r'\b(?:' + '|'.join(sorted(PRONOUNS)) + r')\b'
    def replace(match):
        key = match.group().casefold()
        if key not in normalized:
            raise ValueError('unresolved')
        return normalized[key]
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)