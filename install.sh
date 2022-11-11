#!/bin/bash
set -e

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
git clone https://github.com/PennHIC/hicutils.git
cd hicutils
pip install -e .
deactivate
