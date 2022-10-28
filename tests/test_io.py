import pytest

from hicutils.core import io
from .expected import is_expected


@pytest.mark.parametrize(
    'path,features',
    [
        ('input', 'disease'),
    ]
)
def test_read_tsvs(path, features):
    df = io.read_tsvs(path, features)
    is_expected(df, 'expected/io_test.tsv')
