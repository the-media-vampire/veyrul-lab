"""Original offline routing policy. Not a SoundCraft protocol implementation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    mode: str
    session: str
    read_roots: tuple = ()
    write_roots: tuple = ()
    endpoint: str | None = None

def choose(p):
    if not p.session:
        raise ValueError('explicit session identity required')
    if p.mode == 'headless':
        if p.endpoint is not None:
            raise ValueError('headless policy cannot select desktop endpoint')
        return 'headless'
    if p.mode == 'desktop':
        if p.read_roots or p.write_roots:
            raise ValueError('desktop cannot honor in-process roots')
        if not p.endpoint:
            raise ValueError('verified endpoint required; no default port')
        return 'desktop'
    raise ValueError('explicit mode required')

def after_send(outcome):
    if outcome not in ('confirmed', 'rejected', 'unknown'):
        raise ValueError('invalid outcome')
    return {'confirmed': 'inspect', 'rejected': 'stop',
            'unknown': 'reconcile_without_replay'}[outcome]