# tocmake.py
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


"""tocmake.

Take a meson wrap file and emit a cmake snippet using
FetchContent. This is designed to make it easier to
maintain cmake build systems for projects primaraly using meson,
and to ease transition.

Note: This will not do anything with the patch files, it's assumed
that either the upstream uses cmake or you will edit the
resulting cmake code to do your own patcher.
"""

import argparse
from pathlib import Path
import configparser
parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('wrapfile',
    help='wrap to generate cmake infomation from')


# these are two seperate templates since it's cleaner when just using format strings
# could use jinja as well, but dependencies
TEMPLATE_GIT = """
FetchContent_Declare(
    {name}
    GIT_REPOSITORY {url}
    GIT_TAG {revision}
)
FetchContent_GetProperties({name})
if(NOT {name}_POPULATED)
    FetchContent_Populate({name})
    add_subdirectory(${{{name}_SOURCE_DIR}} ${{{name}_BINARY_DIR}})
endif()
"""
TEMPLATE_FILE = """
FetchContent_Declare(
    {name}
    URL {source_url}
    URL_HASH SHA256={source_hash}
    SOURCE_DIR {directory}
)
FetchContent_GetProperties({name})
if(NOT {name}_POPULATED)
    FetchContent_Populate({name})
    add_subdirectory(${{{name}_SOURCE_DIR}} ${{{name}_BINARY_DIR}})
endif()
"""
def main(args=None):
    args = parser.parse_args(args)
    wrapfile_path = Path(args.wrapfile)
    if not wrapfile_path.exists():
        raise AssertionError("Wrap file does not exist")
    if not wrapfile_path.is_file():
        raise AssertionError("Wrap file is not a file")
    
    wrap = configparser.ConfigParser()
    wrap.read_string(wrapfile_path.read_text())
    if wrap.has_section('wrap-file'):
        # we're a file style wrap
        print(TEMPLATE_FILE.format(
            name=wrapfile_path.stem, **wrap['wrap-file']))
    if wrap.has_section('wrap-git'):
        print(TEMPLATE_GIT.format(
            name=wrapfile_path.stem, **wrap['wrap-git']))

if __name__ == "__main__":
    main()