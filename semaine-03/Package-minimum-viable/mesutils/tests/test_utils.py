from mesutils import chunk, format_fcfa


def test_chunk():
    assert chunk([1, 2, 3, 4, 5], 2) == [
        [1, 2],
        [3, 4],
        [5],
    ]


def test_format_fcfa():
    assert format_fcfa(1500000) == "1 500 000 FCFA"