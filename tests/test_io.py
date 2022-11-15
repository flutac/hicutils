import pytest

from hicutils.core import io
from .expected import is_expected


@pytest.mark.parametrize(
    'path,features',
    [
        ('tests/input', 'disease'),
    ]
)
def test_read_tsvs(path, features):
    df = io.read_tsvs(path, features)
    is_expected(df, 'tests/expected/io_test.tsv')
