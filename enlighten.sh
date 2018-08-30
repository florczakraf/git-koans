#!/usr/bin/env bash

set -e

WORKDIR=$(dirname "$0")
export PYTHONPATH="${WORKDIR}:${PYTHONPATH}"

python "${WORKDIR}/ensure-env.py"
pytest -svx --tb=line "${WORKDIR}"/git-koans/git-koans.py "${@}"
