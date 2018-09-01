#!/usr/bin/env bash

set -e

WORKDIR=$(dirname "$0")
TMPDIR=$(mktemp -d)
trap "rm -rf ${TMPDIR}" EXIT

export PYTHONPATH="${WORKDIR}:${PYTHONPATH}"
export GIT_CONFIG_NOSYSTEM=1
export HOME=${TMPDIR}

python "${WORKDIR}/ensure-env.py"
pytest -svx --tb=line "${WORKDIR}"/git-koans/git-koans.py "${@}"
