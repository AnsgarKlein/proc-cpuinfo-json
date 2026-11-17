#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2026 Ansgar Klein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This script reads /proc/cpuinfo and converts it into a JSON-serializable format.
"""

import argparse
import json
import os
import sys
from typing import Dict
from typing import List
from typing import Union


JsonCpuValue = Union[str, List[str]]


def parse_cpu_block(cpu_block: str) -> Dict[str, JsonCpuValue]:
    """Parse one CPU block into a JSON-serializable dictionary"""

    cpu_data: Dict[str, JsonCpuValue] = {}

    for raw_line in cpu_block.splitlines():
        line = raw_line.strip()
        if line == '':
            continue

        if ':' not in line:
            raise ValueError(f'Invalid /proc/cpuinfo line without ":" separator: {line}')

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        if key == 'flags' or key == 'bugs':
            cpu_data[key] = value.split() if value != '' else []
        else:
            cpu_data[key] = value

    return cpu_data

def split_cpuinfo_field_to_list(field_value: str) -> List[str]:
    """Split a space-separated /proc/cpuinfo field into a list of strings."""

    return field_value.split(' ') if field_value else []

def split_cpuinfo_by_cpu(cpuinfo_text: str) -> List[str]:
    """Split /proc/cpuinfo content into one text block per CPU."""

    return [block for block in cpuinfo_text.strip().split('\n\n') if block.strip() != '']

def convert_cpuinfo_to_json_data(cpuinfo_path: str = '/proc/cpuinfo') -> List[Dict[str, JsonCpuValue]]:
    """Convert /proc/cpuinfo into a list of per-CPU dictionaries."""

    try:
        with open(cpuinfo_path, 'r', encoding='utf-8') as cpuinfo:
            cpuinfo_text = cpuinfo.read()
    except OSError as e:
        print(f"Error reading {cpuinfo_path}: {e}")
        return []

    cpu_blocks = split_cpuinfo_by_cpu(cpuinfo_text)
    return [parse_cpu_block(cpu_block) for cpu_block in cpu_blocks]

def main() -> None:
    """Main function"""

    parser = argparse.ArgumentParser(description="Convert /proc/cpuinfo to JSON")
    parser.add_argument('file',
        type=str,
        metavar='FILE',
        nargs='?',
        default='/proc/cpuinfo',
        help='''
            File to read CPU info from. This is usually /proc/cpuinfo,
            which is also the default.''')
    args = parser.parse_args()

    # Check if given /proc/cpuinfo file exists
    if not os.path.isfile(args.file):
        if args.file == '/proc/cpuinfo':
            print(f'Error: {args.file} does not exist. Probably not running on a linux system.')
            sys.exit(1)
        else:
            print(f'Error: {args.file} does not exist')
            sys.exit(1)

    info_dict = convert_cpuinfo_to_json_data(args.file)
    info_json = json.dumps(info_dict, indent=4)

    print(info_json)


if __name__ == '__main__':
    main()
