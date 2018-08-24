# newwrap.py
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


"""newwrap.

Initialize a new wrap from an upstream tarball. 

Newwrap will download the tarball (with curl) saving it under the
packagecache directory.  It will use the filename supplied by the
server, or, if the server doesn't supply a filename it will use the
end of the url (This is the ``-O -J`` option for curl). After downloading
it will take the sha256 hash of the tarball, and output a wrap file.

Note that this command will fail if the wrap's tarball or extraction
directory already exists

Todo:
    * handle tarballs without a root directory

"""
from pathlib import Path
import argparse
import subprocess
import hashlib
import shutil
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--wrapdev-tree',
                    help='Project tree. Should be the root of a meson project',
                    default=Path.cwd())
parser.add_argument('url',
                    help='URL of the upstream tarball')

parser.add_argument('wrap_name',
                    help='the name of the wrap, this will be the basename of the generated wrap file')

wrapfile = """[wrap-file]
directory={unpack_directory}

source_url={source_url}
source_filename={source_filename}
source_hash={source_hash}
"""


def main(args = None):
    args = parser.parse_args(args)
    wrapdev_path = Path(args.wrapdev_tree)
    subprojects_path = wrapdev_path / "subprojects"
    packagecache_path = subprojects_path / "packagecache"
    wrap_file_path = subprojects_path / (args.wrap_name + ".wrap")
    if wrap_file_path.exists():
        raise AssertionError("Wrap file already exists, aborting")
    subprojects_path.mkdir(exist_ok=True)
    packagecache_path.mkdir(exist_ok=True)

    # this here is a race
    cache_cts = set(packagecache_path.iterdir())
    subprocess.run(['curl', '-L', '-O', '-J', args.url], cwd=packagecache_path)
    new_cache_cts = set(packagecache_path.iterdir())
    downloaded_items = new_cache_cts - cache_cts
    if len(downloaded_items) != 1:
        raise AssertionError(
            "Didn't download any items, or downloaded more than one item")
    print("hashing file {}".format(downloaded_items))
    source_tarball = list(downloaded_items)[0]
    source_hash = hashlib.sha256(source_tarball.read_bytes()).hexdigest()

    cache_cts = set(subprojects_path.iterdir())
    print("extracting source tarball: {}".format(source_tarball))
    shutil.unpack_archive(str(source_tarball), str(subprojects_path))
    new_cache_cts = set(subprojects_path.iterdir())
    extracted_folders = new_cache_cts - cache_cts
    if len(extracted_folders) != 1:
        raise AssertionError("Didn't find any new extracted folders")
    unpack_directory = list(extracted_folders)[0]
    wrap_file_str = wrapfile.format(unpack_directory=str(unpack_directory.relative_to(subprojects_path)),
                                    source_url=args.url,
                                    source_filename=str(source_tarball.relative_to(packagecache_path)),
                                    source_hash=source_hash)
    print("writing wrapfile: {}".format(str(wrap_file_path)))
    wrap_file_path.write_text(wrap_file_str)
    

if __name__ == "__main__":
    main()
