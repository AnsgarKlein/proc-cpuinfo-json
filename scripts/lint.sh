#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
TESTS_DIR="$(cd "$PROJECT_ROOT/tests" && pwd -P)"

# Change directory to project root
cd "$PROJECT_ROOT" || exit 1

PYTHON_SCRIPT='cpuinfo.py'

# Whether or not an error occurred
errors='no'


if ! command -v mypy > /dev/null 2> /dev/null; then
    echo 'Error: Can not run mypy!' > /dev/stderr
    echo 'mypy is not installed!' > /dev/stderr
else
    echo 'Running mypy...'
    if ! mypy "$PYTHON_SCRIPT"; then
        errors='yes'
    fi
    if ! mypy "$TESTS_DIR"; then
        errors='yes'
    fi
fi
echo ''
echo ''


if ! command -v ruff > /dev/null 2> /dev/null; then
    echo 'Error: Can not run ruff!' > /dev/stderr
    echo 'ruff is not installed!' > /dev/stderr
else
    echo 'Running ruff...'
    if ! ruff check "$PYTHON_SCRIPT"; then
        errors='yes'
    fi
    if ! ruff check "$TESTS_DIR"; then
        errors='yes'
    fi
fi
echo ''
echo ''


# Return with error code if any linter returned an error
if [ "$errors" = 'yes' ]; then
    exit 1
fi
