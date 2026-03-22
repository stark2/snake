#!/usr/bin/env bash
set -euo pipefail

# CI quality gate script for Three-Snake Game
# Usage: ./ci/run-tests.sh

python -m pytest tests/ -q
