#!/usr/bin/env python3

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Callable
from typing import List


TESTS_DIR = Path(__file__).parent
PROJECT_ROOT = TESTS_DIR.parent
RESOURCES_DIR = TESTS_DIR.joinpath('resources')
SCRIPT_PATH = PROJECT_ROOT.joinpath('cpuinfo.py')

RESOURCE_FILES = []

def _get_all_resource_files() -> List[Path]:
    """Collect all resources files"""

    resource_files = []
    for entry in RESOURCES_DIR.iterdir():
        if entry.is_file():
            resource_files.append(entry)

    return sorted(resource_files)

RESOURCE_FILES = _get_all_resource_files()
del _get_all_resource_files


class TestResourceFiles(unittest.TestCase):
    """Test suite for resource files in tests/resources."""

    def assert_resource_returns_valid_json(self, resource_file: Path) -> None:
        """Run cpuinfo.py for one resource file and assert it returns valid JSON."""

        # Run script with resource file
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(resource_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=(f'Script failed for {resource_file.name}: '
                f'{result.stdout.decode().strip()}')
        )

        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            self.fail(
                f'Invalid JSON for {resource_file.name}: {error}\n'
                f'Output was:\n{result.stdout.decode()}')

        self.assertIsInstance(parsed, list)
        for cpu_entry in parsed:
            self.assertIsInstance(cpu_entry, dict)

    def test_resources_discovered(self) -> None:
        """Ensure that resource files are discovered."""

        self.assertGreater(
            len(RESOURCE_FILES),
            0,
            msg='No resource files found in tests/resources')




# Create one distinct unittest test function per resource file
def _make_test_name(resource_file: Path) -> str:
    file_name = str(resource_file.name)
    sanitized_name = re.sub(r'[^0-9a-zA-Z_]+', '_', file_name).strip('_')
    return f'test_valid_json_for_cpuinfo_{sanitized_name}'

def _make_resource_test(resource_file: Path) -> Callable[[TestResourceFiles], None]:
    def test_method(self: TestResourceFiles) -> None:
        self.assert_resource_returns_valid_json(resource_file)

    test_method.__doc__ = (
        f'Test resource file: {resource_file.name}'
    )

    return test_method

# Patch function into class
for _resource_file in RESOURCE_FILES:
    setattr(
        TestResourceFiles,
        _make_test_name(_resource_file),
        _make_resource_test(_resource_file))

# Clean up global variables
del _make_test_name
del _make_resource_test

try:
    del _resource_file
except NameError:
    pass
