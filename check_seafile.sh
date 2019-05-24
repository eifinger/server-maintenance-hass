#!/bin/bash
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
cd $scriptDir
source venv/bin/activate
python check_seafile.py
