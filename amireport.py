#creates a count of and size (in gb) report of files in a given directory
#during a given period.

import time
from datetime import datetime
import os
import argparse
import sys
import re


#last 30 days
days = 30

def args():
    parser = argparse.ArgumentParser(
        description='takes path to directory'
    )
    parser.add_argument(
    '-f','--file',
    type=str,
    help='path to directory',
    required=True,
    action='store'
    )

#walk through a directory and get all filenames/filepaths
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
    return file_list


#get modifed/creation date as add to dictionary
def get_dates(file_list):
    for file in file_list:
        file['time']=os.path.getctime(file['path'])
        file['c_date'] = datetime.fromtimestamp(
        file['time']
        ).strftime(
        '%Y-%m-%d'
        )

        # print(f'{file['name']}:{file['date']}')
        # print(file['c_date'])

#get size in bytes and add to dictionary
def get_size(file_list):
    for file in file_list:
        file['size_in_bytes']=os.path.getsize(file['path'])
        # print(file)
#

#sum bytes of files and convert to gigabytes
def get_gb(file_list):
    count = []
    for file in file_list:
        count.append(file['size_in_bytes'])
    byte_sum = sum(count)
    gb_sum = byte_sum/(1024*1024*1024)

    print(f'there are {gb_sum}gb in directory')

#FIGURE OUT THE LAST 30 DAYS

#return report
#test report
files = get_files(sys.argv[1])
get_dates(files)
get_size(files)
get_gb(files)
# print(f'In the last 30 days {} files, {}gb have been processed')


# def main():
#
#
# if __name__ == '__main__':
#     main()
#     exit(0)
