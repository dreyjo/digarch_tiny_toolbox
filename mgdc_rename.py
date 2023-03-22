# needed libraries:
import sys
import argparse
import os
import csv
import re

#arguments:
#csv file to draw the filenames from
#directory path for the files to be renamed
def args():
    parser = argparse.ArgumentParser(
    description='takes source directory and csv path'
    )
    parser.add_argument(
    '-f', '--filecsv',
    type=str,
    help='input path to csv file with filenames',
    required=True,
    action='store'
    )
    parser.add_argument(
    '-s', '--source',
    type=str,
    help='input path to source dir for files to rename',
    required=True,
    action='store'
    )

    args = parser.parse_args()
    return args

#get all filenames and filepaths to be changed:
def get_files(source):
    file_list = []
    for root, subfolders, filenames in os.walk(source):
        for file in filenames:
            if not re.search('.DS_Store', file, re.IGNORECASE):
                path = os.path.join(root, file)
                file_dict = {
                'name': file,
                'path': path
                }
                file_list.append(file_dict)
    #testing
    # print(file_list)
    return file_list

#get new filenames from file reconciliation csv
def get_new_names(a_csv):
    with open(a_csv) as fh:
        reader= csv.reader(fh)
        header= next(reader)

        names = {}
        for lines in reader:
            fname = lines[2]
            sc = lines[3]
            pm = lines[4]
            names[fname]=sc
            # testing
        # print(names)
        return names




def rename(file_list, new):
    fails = []
    for f in file_list:
        oldname = f['name']
        oldpath = f['path']
        root = os.path.dirname(oldpath)
        #testing:
        # print(root)
        if oldname in new:
            try:
                os.rename(
                #src
                oldpath,
                #dest
                os.path.join(root,new[oldname])
                )
            except:
                # fails.append(oldname)
                print(f'did not find {oldname} in source directory, not renamed')

        #fail report:
        # with open('rename_fails.txt', 'w', newline='') as w:
        #     for line in fails:
        #         w.write(f'{line}\n')
            # writer = csv.writer(report)
            # writer.writerows(fails)



def main():
    a_csv= args().filecsv
    source= args().source
    files=get_files(source)
    new=get_new_names(a_csv)

    #testing
    # print(files)
    # print(new)
    # print(source)
    rename(files, new)



if __name__ == '__main__':
    main()
