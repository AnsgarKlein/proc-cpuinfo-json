#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
TESTS_DIR="$(cd "$PROJECT_ROOT/tests" && pwd -P)"

# Change directory to project root
cd "$PROJECT_ROOT" || exit 1

python -m unittest discover -v --start-directory "$TESTS_DIR"
