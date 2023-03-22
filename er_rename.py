# needed libraries:
import sys
import argparse
import os
import re

#arguments:
#directory path for the files to be renamed
#pattern to look for
#pattern to replace with
def args():
    parser = argparse.ArgumentParser(
    description='takes source directory, select pattern for finding and replace with given pattern'
    )
    parser.add_argument(
    '-s', '--source',
    type=str,
    help='input path to source dir for files to rename',
    required=True,
    action='store'
    )
    parser.add_argument(
    '-f', '--find',
    type=str,
    help='input pattern to find',
    required=True,
    action='store'
    )
    parser.add_argument(
    '-r', '--replace',
    type=str,
    help='input pattern to replace with',
    required=True,
    action='store'
    )

    args = parser.parse_args()
    return args

#find strategy for limiting the depth 
def get_paths(source):
    dirs = []
    for root, subfolders, filename in os.walk(source):
        for name in subfolders: 
            # print(name)
            if not re.search('.DS_Store', name, re.IGNORECASE):
                oldpath = os.path.join(root, name)
                dirs.append(oldpath)
    return dirs

#input pattern string to look for:
#input pattern string to replace with:
def find_replace(find, repl, dirlist):
    f = str(find)
    r = str(repl)
    repl_list = []

    for path in dirlist:
        if re.search(f, path):
            newpath = re.sub(f, r, path)
            # print(newpath)
            os.renames(path,newpath)

def main():
    source= args().source
    find= args().find
    repl= args().replace
    dirlist = get_paths(source)
    find_replace(find, repl, dirlist)

if __name__ == '__main__':
    main()
