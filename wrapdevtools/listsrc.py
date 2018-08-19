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
