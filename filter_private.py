"""Restricted header filter, not a complete Twee parser. MIT.
Supports :: Title and :: Title [space-separated tags].
Rejects metadata braces, bracketed titles and malformed headers.
No extension/CLI parity is claimed. Use on staging copies only.
"""
import re
import sys

HEADER = re.compile(r'::[ \t]+([^\[\]{}\r\n]+?)(?:[ \t]+\[([^\[\]\r\n]*)\])?[ \t]*')

def filter_twee(text):
    out = []
    keep = True
    for line in text.splitlines(keepends=True):
        if line.startswith('::'):
            match = HEADER.fullmatch(line.rstrip('\r\n'))
            if match is None:
                raise ValueError('Unsupported header; refusing partial filtering')
            keep = 'Twine.private' not in (match.group(2) or '').split()
        if keep:
            out.append(line)
    return ''.join(out)

if __name__ == '__main__':
    # Buffer before emitting so unsupported syntax does not emit partial output.
    sys.stdout.buffer.write(filter_twee(sys.stdin.buffer.read().decode('utf-8')).encode('utf-8'))