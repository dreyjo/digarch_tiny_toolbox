#!/usr/local/bin/ python3

import re
import sys
import os

def clean_manifest(textfile):
    patterns = ['._', '.DS_Store', '.ds_store', '.DS_STORE', '~.', '~', '.~']
    linecount = 0
    delete = []
    val = []


    #open file to read lines
    with open(textfile, 'r+') as fp:
    # i =open(textfile, "r+")
    # with open(textfile, 'r') as input:
        lines = fp.readlines()
        pre = len(lines)

        for line in lines:
            for pattern in patterns:
                if pattern in line:
                    delete.append(line)
                else:
                    val.append(line)

    # print(len(delete))
    # print(delete)
        fp.seek(0)
        fixed = 0
        for line in lines:
        #     for d in delete:
            if line not in delete:
                fp.write(line)
                fixed = fixed + 1
                fp.truncate()

        def validate(lines, pre_count, fixed_count, delete_list, validate_list):
            expected = pre_count-len(delete_list)
            x = set(lines)
            y = set(validate_list)

            print(f'{pre_count} lines before fixing')
            print(f'{len(delete_list)} lines to be removed')
            print(f'expecting {expected} lines')
            print(f'{fixed_count} lines in fixed manifest')

            if fixed_count == expected:
                print('expected line count matches')

            if x == y:
                print('expceted fixed lines present in manifest')


        validate(lines, pre, fixed, delete, val)


def main():
    clean_manifest(sys.argv[1])

if __name__ == '__main__':
     main()
     exit(0)
