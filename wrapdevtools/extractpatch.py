"""extractpatch.

Extract changes to an upstream into a patch directory. For now this
works with file (tarball) based wraps only """

import argparse
from pathlib import Path
import configparser

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
    

if __name__ == "__main__":
    main()
