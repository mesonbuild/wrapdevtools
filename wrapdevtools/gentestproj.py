# gentestproj.py
#
# Copyright 2018 Charles Barto <bartoc@umich.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0



# not sure if good name?

"""gentestproj.

Generate a project testing a wrap. gentestproj can generate
both superproject-subproject tests, or simply extract the upstream
source code and apply the patch.
"""

import argparse
from pathlib import Path
import shutil
import configparser
import logging

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('wrap',
    help='path to a wrap patch directory (with an upstream.wrap)')

parser.add_argument('--output',
    help="Output project directory, created if it doesn't exist",
    default=Path.cwd())

parser.add_argument('--type',
    choices=['single_project', 'superproject_subproject'],
    help='Kind of testing project to generate',
    default='single_project')

def main(args=None):
    args = parser.parse_args(args)
    wrap_path = Path(args.wrap)
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=False)

    upstream_wrap = wrap_path / 'upstream.wrap'

    if not upstream_wrap.is_file():
        raise AssertionError("upstream.wrap file does not exist")
    
    
    

