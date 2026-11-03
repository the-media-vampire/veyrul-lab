from reference_guard import rewrite

CASES = [
    ('She waited.', {'she':'Mira'}, 'Mira waited.'),
    ('The shelter stood.', {'he':'Orin'}, 'The shelter stood.'),
    ('He met her.', {'He':'heron','her':'Mira'}, 'heron met Mira.'),
    ('“She” waited.', {}, None),
    ('They waved.', {'They':'Mira and Orin'}, 'Mira and Orin waved.'),
    ('She waited.', {}, None),
]

if __name__ == '__main__':
    for text, mapping, expected in CASES:
        try:
            result = rewrite(text, mapping)
        except ValueError:
            result = None
        assert result == expected, (text, result, expected)
    print('6 authored fixtures passed')