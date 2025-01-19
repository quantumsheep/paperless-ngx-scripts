#!/usr/bin/env bash

set -e

SCRIPT_FILEPATH=$(readlink -f -- "$0")
ROOT_DIR=$(dirname "$SCRIPT_FILEPATH")

/usr/bin/env python3 -m pip install -r "$ROOT_DIR/requirements.txt"
export PYTHONPATH="$PYTHONPATH:$ROOT_DIR/src"

names="${PAPERLESS_POST_CONSUME_SCRIPT_NAMES//,/ }"

pushd "$ROOT_DIR" >/dev/null

for name in $names; do
  /usr/bin/env python3 "$ROOT_DIR/src/scripts/post-consumption/$name.py"
done

popd >/dev/null
