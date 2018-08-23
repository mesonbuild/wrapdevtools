# extractpatch.py
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




"""extractpatch.

Extract changes to an upstream into a patch directory. For now this
works with file (tarball) based wraps only. Additionally this tool
will copy the wrap file to upstream.wrap in the destination
directory

"""

import argparse
from pathlib import Path
import configparser
import tempfile
import shutil
import filecmp

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('wrapfile',
                    help='wrap file to extract a patch from')

parser.add_argument('--output',
                    help='directory in which to output patch',
                    required=True)

def main():
    args = parser.parse_args()
    wrapfile_path = Path(args.wrapfile)
    if not wrapfile_path.exists():
        raise AssertionError("Wrap file does not exist")
    if not wrapfile_path.is_file():
        raise AssertionError("Wrap file is not a file")
    wrap = configparser.ConfigParser()
    wrap.read_string(wrapfile_path.read_text())
    subprojects_dir = wrapfile_path.parent
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    packagecache_path = subprojects_dir / 'packagecache'
    project_directory = subprojects_dir / wrap['wrap-file']['directory']
    package_upstream_path = packagecache_path / wrap['wrap-file']['source_filename']
    if not project_directory.exists():
        raise AssertionError("Wrap file output directory does not exist")
    if not package_upstream_path.is_file():
        raise AssertionError("Wrap upstream tarball does not exist")
    flist = []
    with tempfile.TemporaryDirectory() as extract_dir:
        shutil.unpack_archive(str(package_upstream_path), extract_dir)
        dcmps = [filecmp.dircmp(Path(extract_dir) / wrap['wrap-file']['directory'], project_directory)]
        while len(dcmps) > 0:
            dcmp = dcmps.pop()
            for f in dcmp.right_only:
                fullpath = Path(dcmp.right) / f
                flist.append(fullpath.relative_to(project_directory))
            dcmps += list(dcmp.subdirs.values())
    print("copying changed files to output directory")
    for file in flist:
        src_file = project_directory/file
        tgt_file = output_dir/file
        tgt_file.parent.mkdir(exist_ok=True)
        print("copying {} to {}".format(str(src_file), str(tgt_file)))
        shutil.copy(str(src_file), str(tgt_file))
    upstream_wrap_path = output_dir / "upstream.wrap"
    print("copying {} to {}".format(str(wrapfile_path), str(upstream_wrap_path)))
    shutil.copy(str(wrapfile_path), str(upstream_wrap_path))
        
if __name__ == "__main__":
    main()
