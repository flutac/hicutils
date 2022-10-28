import pytest

from hicutils.core.io import read_tsvs
from .expected import is_expected


@pytest.mark.parametrize(
    'path,features,expected_path',
    [
        ('input', 'disease', 'expected/io_test.tsv'),
    ]
)
def test_read_tsvs(path, features, expected_path):
    df = read_tsvs(path, features)
    is_expected(df, expected_path)
