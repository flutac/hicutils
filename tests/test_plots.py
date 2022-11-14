import itertools
import pytest

import numpy as np
from hicutils.core import io
import hicutils.plots as plots
import matplotlib.pyplot as plt

from .expected import is_expected


POOL = 'subject'
DF = io.read_tsvs('input', 'subject')


@pytest.mark.parametrize(
    'size_metric',
    ('clones', 'copies')
)
def test_cdr3_aa_usage(size_metric):
    path = f'expected/cdr3_aa_usage_{size_metric}'
    _, pdf = plots.plot_cdr3_aa_usage(DF, POOL, size_metric=size_metric)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'by,length',
    [
        ('cdr3_aa', 10),
        ('cdr3_nt', 21)
    ]
)
def test_cdr3_logo(by, length):
    path = f'expected/cdr3_logo_{by}_{length}'
    _, m = plots.plot_cdr3_logo(DF, by, length)
    is_expected(m, f'{path}.tsv')
    plt.savefig(f'{path}.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'gene,size_metric',
    itertools.product(
        ['v_gene', 'j_gene'],
        ['clones', 'copies'],
    )
)
def test_gene_usage(gene, size_metric):
    path = f'expected/gene_usage_{gene}_{size_metric}'
    _, pdf = plots.plot_gene_usage(DF, POOL, gene, size_metric=size_metric,
                                   figsize=(12, 6))
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'intervals',
    [
        (10, 100, 1000),
        (20, 50, 100, 500, 1000),
    ]
)
def test_plot_ranges(intervals):
    path = f'expected/range_{"-".join([str(s) for s in intervals])}'
    g, pdf = plots.plot_ranges(DF, POOL, intervals)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'size_metric',
    ['clones', 'copies']
)
def test_shm_distribution(size_metric):
    path = 'expected/shm_distribution_{}'.format(size_metric)
    g, pdf = plots.plot_shm_distribution(DF, POOL, size_metric=size_metric)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


def test_shm_aggregate():
    path = 'expected/shm_aggregate'
    g, pdf = plots.plot_shm_aggregate(DF, POOL)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'buckets',
    [
        (1, 10, 25),
        (1, 2, 10, 15, 20)
    ]
)
def test_shm_range(buckets):
    path = 'expected/shm_range_{}'.format('-'.join(
        [str(c) for c in buckets]
    ))
    g, pdf = plots.plot_shm_range(DF, POOL)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'color_top',
    [5, 10, 20]
)
def test_spectratype(color_top):
    path = 'expected/spectratype_{}'.format(color_top)
    g, pdf = plots.plot_spectratype(DF, color_top=color_top)
    pdf = pdf.replace('', np.nan)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'only_overlapping,overlapping_features,scale,limit',
    itertools.product(
        [True, False],
        [('cdr3_aa',), ('cdr3_aa', 'v_gene')],
        [True, False, 'log'],
        [10, 100, 500],
    )
)
def test_overlap_strings(only_overlapping, overlapping_features, scale,
                         limit):
    path = 'expected/overlap_strings_{}_{}_{}_{}'.format(
        only_overlapping, '-'.join(overlapping_features), scale,
        limit
    )
    g, pdf = plots.plot_strings(
        DF,
        POOL,
        only_overlapping=only_overlapping,
        overlapping_features=overlapping_features,
        scale=scale,
        limit=limit
    )
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'cutoff',
    [10, 20, 50]
)
def test_top_clones(cutoff):
    path = f'expected/top_clones_{cutoff}'
    g, pdf = plots.plot_top_clones(DF, cutoff=cutoff)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')
