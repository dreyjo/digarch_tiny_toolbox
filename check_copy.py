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
    #then create a faail csv with the filename and size
    source_diff = []
    for item in diff['source_diff']:
        if len(diff['source_diff']) > 0:
            source_diff.append(item)
            with open('source_fails.csv','wb') as out:
                csv_out=csv.writer(out)
                # csv_out.writerow(['name','size'])
                for row in source_diff:
                    csv_out.writerow(row)
            # print(item)

    #list of files and filesize in copied dir but not in source dir
    copy_diff =[]
    for item in diff['copy_diff']:
        if len(diff['copy_diff']) > 0:
            copy_diff.append(item)
            with open('copy_fail.csv','wb') as out:
                csv_out=csv.writer(out)
                # csv_out.writerow(['name','size'])
                for row in copy_diff:
                    csv_out.writerow(row)
            # print(item)

    

# #from here: main logic to copy is create a list of all file paths in directory,
# Create tuple with file path, and file size
# Add to a set (so it's unique)
#
#
# def get_files_on_source(drive_path):
#     drive_path = pathlib.Path(drive_path)
#     root_files = drive_path.glob('*')
#     audio_bag_files = drive_path.joinpath('Audio').glob('**/*')
#     video_bag_files = drive_path.joinpath('Video').glob('**/*')
#     film_bag_files = drive_path.joinpath('Film').glob('**/*')
#     manifest = []
#
#     for file_list in [root_files, audio_bag_files, video_bag_files, film_bag_files]:
#         for path in file_list:
#             if path.is_file() and path.suffix != '.txt' and path.suffix != '.json':
#                 manifest.append((str(path).replace(str(drive_path), ''), path.stat().st_size))
#
#     return set(manifest)
#
#
# --------------------------------------
# We can call this check_copy.py
# Then compare sets between he original directory and the new directory
#
# def compare_source_snowball(
#     source_set: set,
#     snowball_set: set,
# ):
#
#     if source_set == snowball_set:
#         return None
#     else:
#         difference = {
#             'source_diff': source_set - snowball_set,
#             'snowball_diff': snowball_set - source_set
#         }

#
def main():
    o = args().origdir
    c = args().copydir
    origs = get_orig_files(o)
    cdir = get_copy_files(c)

    compare_dirs(origs, cdir)




if __name__ == '__main__':
    main()
