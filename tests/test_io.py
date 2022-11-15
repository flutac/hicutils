import pytest

from hicutils.core import io, metadata
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
    mdf = metadata.make_metadata_table(df, 'disease')
    is_expected(mdf, 'tests/expected/metadata.tsv')
