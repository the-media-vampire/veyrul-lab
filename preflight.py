"""Structural check only; no ComfyUI imports or execution."""

def preflight(workflow, node_id, replacement):
    """Inspect declared outgoing socket types, not tensors or executable API graphs."""
    nodes = [n for n in workflow['nodes'] if n['id'] == node_id]
    if len(nodes) != 1:
        raise ValueError('expected one boundary node')
    node = nodes[0]
    required = {o['type'] for o in node.get('outputs', []) if o.get('links')}
    missing = sorted(required - set(replacement))
    unknown = sorted(t for t in required if not replacement.get(t, {}).get('semantics_verified', False))
    return {
        'required_output_types': sorted(required),
        'missing_output_types': missing,
        'unverified_semantics': unknown,
        'structural_candidate': not missing,
        'ready_to_attempt': not missing and not unknown,
        'runtime_validated': False,
        'note': 'Keep downstream preprocessing intact. Verification flags are caller attestations, not evidence established by this tool.'
    }