# extractpatch.py
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


"""extractpatch.

Extract changes to an upstream into a patch directory. For now this
works with file (tarball) based wraps only """

import argparse
from pathlib import Path
import configparser
import tempfile
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('wrapfile',
                    help='wrap file to extract a patch from')


def main():
    args = parser.parse_args()
    wrapfile_path = Path(args.wrapfile)
    if not wrapfile_path.exists():
        raise AssertionError("Wrap file does not exist")
    if not wrapfile_path.is_file():
        raise AssertionError("Wrap file is not a file")
    wrap = configparser.ConfigParser()
    wrap.read_file(wrapfile_path)
    subprojects_dir = wrapfile_path.parent
    project_directory = subprojects_dir / wrap['wrap-file']['directory']
    if not project_directory.existsp():
        raise AssertionError("Wrap file output directory does not exist")

    extract_dir = tempfile.TemporaryDirectory()


if __name__ == "__main__":
    main()
