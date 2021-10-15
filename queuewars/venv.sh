#!/bin/bash
set -eout pipefail
python3 -m venv .direnv
source .direnv/bin/activate
pip3 install -r requirements.txt
