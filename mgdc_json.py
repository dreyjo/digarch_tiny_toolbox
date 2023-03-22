#!/usr/bin/env python3

import argparse
import os
import csv
import re
import sys
import json

def args():
    parser = argparse.ArgumentParser(
    description='takes source directory and csv path'
    )
    parser.add_argument(
    '-c', '--csv',
    type=str,
    help='input path to CMS csv export file',
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
    parser.add_argument(
    '-d', '--dest',
    type=str,
    help='input path to destination directory for json files',
    required=True,
    action='store'
    )

    args = parser.parse_args()
    return args

def get_files(source):
    file_list = []

    for root, dirs, files in os.walk(source):
        for file in files:
            if file.endswith(('.mov', '.wav', '.flac', '.mkv', '.dv', '.mp4')):
                i = re.search(r'_(\d{6})_', file)
                file_dict = {'path':os.path.join(root, file),
                             'filename':file, 
                             'id': i.group(1)}
                file_list.append(file_dict)

    return file_list
    #testing
    # print(file_list)

def csv_to_ami_barcode(a_csv, file_list):
#this function opens cms csv report, compares cms id  to the file list from source. 
# if a cms id in filelist matches a cms id in the cms report, a dictionary record is created
# with the cms id and barcode
#returns a list of dictionaries holding primary ids and barcodes 
    fh = open(a_csv, 'r', encoding='utf-8', errors='ignore')
    reader = csv.reader(fh)

    next(reader, None)
    ami_list = []

    for row in reader:
        # for filepath in sorted(file_list):
        for file in file_list:
            filename = file['filename']
            cmsID = file['id']
            if cmsID in row[0]:
                barcode = row[8]
                id = row[0]
                ami_dict = {
                    'primaryID': id,
                    'barcode': barcode
                }
                ami_list.append(ami_dict)
    
    return ami_list
    # testing:
    # print(ami_list)

def make_json(file_list, ami_list, dest):
    # f = sorted(file_list)
    for record in ami_list:
        p = record['primaryID']
        b = record['barcode']
        for file in file_list:
            filename = file['filename']
            filepath = file['path']
            nested_json = {
                'asset': {
                'referenceFilename': filename
                },
                'bibliographic':{
                'primaryID':p,
                'barcode':b
            }
            }
            json_filename = os.path.splitext(filename)[0] + ".json"
            json_filepath = os.path.join(dest, json_filename)
            with open(json_filepath, 'w') as f:
                json.dump(nested_json, f, indent = 4)


#from Ben
# for row in reader:
#     for filepath in sorted(sync_list):
#         filename = filepath.split('/')[-1]
#         cmsID = filename.split('_')[1]
#         if cmsID in row[0]:
#             print(filename)
#             nested_json = {'asset': {'referenceFilename': filename},
#                         'bibliographic': {'primaryID': row[0],
#                         'barcode': row[8]}}
#             json_filename = os.path.splitext(filename)[0] + ".json"
#             json_filepath = os.path.join(dest, json_filename)
#             with open(json_filepath, 'w') as f:
#                 json.dump(nested_json, f, indent = 4)

def main():
    report = args().csv
    source = args().source
    dest = args().dest
    files = get_files(source)
    ami_ids = csv_to_ami_barcode(report, files)
    make_json(files, ami_ids, dest)
    #testing:


if __name__ == '__main__':
    main()