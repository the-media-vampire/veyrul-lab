from dataclasses import dataclass, field

@dataclass
class EntityTag:
    tag: str
    look: str
    look_only: bool = False

@dataclass
class CrowdRule:
    crowd_tag: str
    allow_in: str
    deny_in: list  # locations explicitly denied; must be non-empty

@dataclass
class LightState:
    allowed_sources: list  # the ONLY sources permitted
    prohibitions: list     # written negatives (e.g. 'NO screens')

@dataclass
class ShotBlock:
    label: str
    start: float
    end: float
    light_ref: str
    blocking_prop: str     # prop name blocking is relative to
    framing: str           # description
    framing_measurable: bool  # True if degrees/head-height given

@dataclass
class PromptSpec:
    entities: list
    crowd_rules: list
    light_state: LightState
    shots: list

@dataclass
class ValidationResult:
    valid: bool
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

class CrowdLocationContract:
    """Validates structured prompts against location-tagging / crowd-exclusivity
    mechanism (art_01M687Y92Z73146YZ2W3CYZKBW r1). MIT."""

    def validate(self, s: PromptSpec) -> ValidationResult:
        e, w = [], []
        for ent in s.entities:
            if not ent.tag.startswith('@'):
                e.append(f'Tag must start @: {ent.tag}')
            if not ent.look.strip():
                e.append(f'{ent.tag}: empty look line')
        for cr in s.crowd_rules:
            if not cr.allow_in:
                e.append(f'{cr.crowd_tag}: missing allow_in')
            if not cr.deny_in:
                e.append(f'{cr.crowd_tag}: no deny_in — exclusivity not stated')
        if not s.light_state.allowed_sources:
            e.append('LightState: allowed_sources empty — state only sources, not just prohibitions')
        if not s.light_state.prohibitions:
            w.append('LightState: no prohibition negatives')
        for sh in s.shots:
            if sh.end <= sh.start:
                e.append(f'{sh.label}: end <= start')
            if not sh.blocking_prop.strip():
                e.append(f'{sh.label}: blocking_prop empty')
            if not sh.framing_measurable:
                w.append(f'{sh.label}: framing word-only; add degrees or head-height fraction')
        for ent in s.entities:
            if ('ref' in ent.look.lower() or 'hall' in ent.look.lower()) and not ent.look_only:
                w.append(f'{ent.tag}: looks like reference but look_only=False — model may copy frame')
        return ValidationResult(valid=len(e) == 0, errors=e, warnings=w)