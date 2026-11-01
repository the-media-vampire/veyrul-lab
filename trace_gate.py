import hashlib
import json


def fingerprint(job):
    return hashlib.sha256(json.dumps(job, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def gate(job, receipt):
    if job.get('platform') not in ('desktop', 'web'):
        return 'hold:platform'
    if receipt is None:
        return 'hold:no-measurement'
    if receipt.get('job_sha256') != fingerprint(job):
        return 'hold:stale-measurement'
    if receipt.get('scope') != 'whole-output':
        return 'hold:partial-measurement'
    count = receipt.get('anchors')
    if type(count) is not int or count < 0:
        return 'hold:invalid-count'
    limit = {'desktop': 8000000, 'web': 2000000}[job['platform']]
    return 'eligible:not-executed' if count <= limit else 'hold:over-budget'