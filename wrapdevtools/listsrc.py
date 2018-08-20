# listsrc.py
#
# Copyright 2018 Charlie Barto <barto.charlie@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later


"""listsrc.

List sources in a subdirectory matching a pattern, and format them for
pasting into a meson build file"""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('pattern', help='the glob pattern to search for')


def main():
    args = parser.parse_args()
    files = Path.cwd().glob(args.pattern)
    output = ""
    for file in files:
        relfile = file.relative_to(Path.cwd())
        output += "'{}',\n".format(str(relfile))
    print(output)


if __name__ == "__main__":
    main()
