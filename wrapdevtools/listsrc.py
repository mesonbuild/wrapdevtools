# listsrc.py
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


"""listsrc.

List sources in a subdirectory matching a pattern, and format them for
pasting into a meson build file"""

import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('pattern', help='the glob pattern to search for')


def main(args = None):
    args = parser.parse_args(args)
    files = Path.cwd().glob(args.pattern)
    output = ""
    for file in files:
        relfile = file.relative_to(Path.cwd())
        output += "'{}',\n".format(str(relfile))
    print(output)


if __name__ == "__main__":
    main()
