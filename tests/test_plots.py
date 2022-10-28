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
    ['clones', 'copies']
)
def test_cdr3_aa_usage(size_metric):
    path = 'expected/cdr3_aa_usage_{}'.format(size_metric)
    _, pdf = plots.plot_cdr3_aa_usage(DF, POOL, size_metric=size_metric)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'gene,size_metric',
    itertools.product(
        ['v_gene', 'j_gene'],
        ['clones', 'copies'],
    )
)
def test_gene_usage(gene, size_metric):
    path = 'expected/gene_usage_{}_{}'.format(gene, size_metric)
    _, pdf = plots.plot_gene_usage(DF, POOL, gene, size_metric=size_metric)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'intervals',
    [
        (0, 10, 100, 1000),
        (0, 20, 50, 100, 500, 1000),
    ]
)
def test_plot_ranges(intervals):
    path = 'expected/range_{}'.format('-'.join([
        str(s) for s in intervals
    ]))
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
    'only_overlapping,overlapping_features,scale,logscale,limit',
    itertools.product(
        [True, False],
        [('cdr3_aa',), ('cdr3_aa', 'v_gene')],
        [True, False],
        [True, False],
        [10, 100, 500]
    )
)
def test_overlap_strings(only_overlapping, overlapping_features, scale,
                         logscale, limit):
    path = 'expected/overlap_strings_{}_{}_{}_{}_{}'.format(
        only_overlapping, '-'.join(overlapping_features), scale,
        logscale, limit
    )
    g, pdf = plots.plot_strings(
        DF,
        POOL,
        only_overlapping=only_overlapping,
        overlapping_features=overlapping_features,
        scale=scale,
        logscale=logscale,
        limit=limit
    )
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')


@pytest.mark.parametrize(
    'cutoff,annotate',
    itertools.product(
        [10, 20, 50],
        [True, False]
    )
)
def test_top_clones(cutoff, annotate):
    path = 'expected/top_clones_{}_{}'.format(cutoff, annotate)
    g, pdf = plots.plot_top_clones(DF, cutoff=cutoff)
    is_expected(pdf, path + '.tsv')
    plt.savefig(path + '.pdf', bbox_inches='tight')
