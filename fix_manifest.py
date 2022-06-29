import re
import sys
import os

def clean_manifest(textfile):
    patterns = ['._', '.DS_Store', '.ds_store', '.DS_STORE', '~.', '~']
    linecount = 0
    delete = []

    #open file to read lines
    i = open(textfile, "r")
    # with open(textfile, 'r') as input:
    lines = i.readlines()
    i.close()

    #open file to write
    i=open(textfile, "w")
    for line in lines:
        if '._' not in line:
            i.write(line)



def main():
    clean_manifest(sys.argv[1])

if __name__ == '__main__':
     main()
     exit(0)
