#
# os.path
#
# examples on how to use os.path to work
# with files in folders and subfolders

import os

path='C:\\tmp'
# this returns a 3-tuple for every
# subdirectory, including root, with:
# directory, sub-directories, files
tmp=os.walk(path)

# this makes a list of all .txt files amongst
# all files in all subfolders
allfiles=[]
for root, subdirs, files in tmp:
    for names in files:
        file=os.path.join(root,names)
        name,ext=os.path.splitext(file)
        if ext=='.txt':
            allfiles.append(file)
