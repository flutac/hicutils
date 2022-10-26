import pytest
import pandas as pd

from hicutils.core.io import read_tsvs


@pytest.mark.parametrize(
    'path,features,expected_len',
    [
        ('tests/input', 'disease', 32774),
    ]
)
def test_read_tsvs(path, features, expected_len):
    df = read_tsvs(path, features)
    assert len(df) == expected_len
