from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='hicutils',
    version='0.0.1',
    author='Aaron M. Rosenfeld',
    author_email='aaron.rosenfeld@pennmedicine.upenn.edu',
    url='https://github.com/PennHIC/hicutils',
    packages=[
        'hicutils',
        'hicutils.core',
    ],
    install_requires=[
        'pandas>=1.5.1',
        'seaborn>=0.12.1'
    ],
)
