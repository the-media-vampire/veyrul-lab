from filter_private import filter_twee

cases = [
 ('private EOF', ':: Secret [Twine.private]\nsecret', ''),
 ('public EOF', ':: Start\nhello', ':: Start\nhello'),
 ('private then public', ':: Secret [Twine.private]\nsecret\n:: Start\nhello', ':: Start\nhello'),
 ('tag prefix', ':: Start [Twine.privateNotes]\nhello', ':: Start [Twine.privateNotes]\nhello'),
 ('title mention', ':: Twine.private diary\nhello', ':: Twine.private diary\nhello'),
 ('body mention', ':: Start\nTwine.private', ':: Start\nTwine.private'),
 ('tag list and CRLF', ':: Secret [note Twine.private other]\r\nsecret\r\n:: Start\r\nhello', ':: Start\r\nhello'),
]
for name, src, want in cases:
    assert filter_twee(src) == want, name
for src in [':: Start {"position":"0,0"}\nhello', ':: Start [unclosed\nhello']:
    try:
        filter_twee(src)
    except ValueError:
        pass
    else:
        raise AssertionError('unsupported header must be rejected')
print('9 checks passed')