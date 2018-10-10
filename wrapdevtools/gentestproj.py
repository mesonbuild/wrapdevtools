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


# note that we hardcode the name of the dependency varialbe
# this may change, but the intention was to enforce some predictability on
# the dependency variable name
BUILD_TEMPLATE = """
project('{name}', 'c', version: '0.1.0')

sub = subproject('{wrap_name}')
dep = sub.get_variable('{wrap_name}_dep')

exe = executable('{name}', 'main.c',
    dependencies: dep)
"""
MAIN_TEMPLATE = """
#include <stdlib.h>
int main(int argc, char** argv) {
    return EXIT_SUCCESS;
}
"""

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('wrap',
    help='path to a wrap patch directory (with an upstream.wrap)')

parser.add_argument('--output',
    help="Output project directory, created if it doesn't exist",
    default=Path.cwd())

parser.add_argument('--name',
    help="project name, specify if you want a custom name for the generated project and"
         "executable",
    default="testproj")

def main(args=None):

    EXCLUDE_NAMES = [
        'upstream.wrap',
        'readme.txt',
        'LICENSE.build'
    ]

    args = parser.parse_args(args)
    wrap_path = Path(args.wrap)
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)

    upstream_wrap = wrap_path / 'upstream.wrap'
    subprojects_path = output_path / 'subprojects'
    if not upstream_wrap.is_file():
        raise AssertionError("upstream.wrap file does not exist")

    wrap = configparser.ConfigParser()
    wrap.read_string(upstream_wrap.read_text())

    subprojects_path.mkdir(exist_ok=True)
    wrap_name = wrap['wrap-file']['directory']
    shutil.copyfile(upstream_wrap, subprojects_path / f"{wrap_name + '.wrap'}")
    shutil.copytree(wrap_path, subprojects_path / wrap_name, ignore=shutil.ignore_patterns(*EXCLUDE_NAMES))
    
    mesonbuild_file = Path(output_path / 'meson.build')
    main_file = Path(output_path / 'main.cpp')

    mesonbuild_file.write_text(BUILD_TEMPLATE.format(name=args.name, wrap_name=str(wrap_name)))
    main_file.write_text(MAIN_TEMPLATE)





    
    
    
    
    

