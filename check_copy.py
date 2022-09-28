import os
import re
import argparse
import sys
import stat
import csv

#take original and copy directories as input:
def args():
    parser = argparse.ArgumentParser(
    description='input paths to directories to compare'
    )
    parser.add_argument(
    '-o', '--origdir',
    type=str,
    help='input path to the original directory',
    required=True,
    action='store'
    )
    parser.add_argument(
    '-c', '--copydir',
    type=str,
    help='input path to the copied directory',
    required=True,
    action='store'
    )

    args = parser.parse_args()
    return args


#get list of all paths to files in original directory
def get_orig_files(origdir):
    manifest = []
    for root, subfolders, filenames in os.walk(origdir):
        for file in filenames:
            path = os.path.join(root, file)
            if not re.search('.DS_Store', file, re.IGNORECASE):
                manifest.append((file, os.stat(path).st_size))

    return set(manifest)
    # #testing
    # print(manifest)


#get list of all paths to files in copied directory
def get_copy_files(copydir):
    manifest = []
    for root, subfolders, filenames in os.walk(copydir):
        for file in filenames:
            path = os.path.join(root, file)
            if not re.search('.DS_Store', file, re.IGNORECASE):
                manifest.append((file, os.stat(path).st_size))

    return set(manifest)


#compare filelists, return differences as a csv?
def compare_dirs(source_set, copy_set):
    if source_set == copy_set:
        print('no differences')
    else:
        diff = {
            'source_diff': source_set - copy_set,
            'copy_diff': copy_set - source_set
            }
        #testing
        # print(diff)

    #list of files and filesize in source dir but not in copied dir
    #i.e. files that didn't transfer over. 
    source_diff = []
    #create a fail csv with the filename and size
    for item in diff['source_diff']:
        if len(diff['source_diff']) > 0:
            #testing
            # print(item)
            source_diff.append(item)
            with open('source_fails.csv','w') as out:
                csv_out=csv.writer(out)
                headers = ['filename', 'filesize']

                for row in source_diff:
                    csv_out.writerow(headers)
                    csv_out.writerow(row)
                    # testing
                    # print(item)

    #list of files and filesize in copied dir but not in source dir
    copy_diff =[]
    #create a fail csv with the filename and size
    for item in diff['copy_diff']:
        if len(diff['copy_diff']) > 0:
            # testing
            # print(item)
            copy_diff.append(item)
            with open('copy_fail.csv','w') as out:
                csv_out=csv.writer(out)
                headers = ['filename', 'filesize']
                    
                for row in copy_diff:
                    csv_out.writerow(headers)
                    csv_out.writerow(row)
                    # testing
                    # print(item)

def main():
    o = args().origdir
    c = args().copydir
    origs = get_orig_files(o)
    cdir = get_copy_files(c)

    compare_dirs(origs, cdir)

if __name__ == '__main__':
    main()
