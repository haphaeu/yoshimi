# -*- coding: utf-8 -*-
"""

Find and merge gopro video chapters in working directory.

Videos are found by file name pattern. Implemented for Hero3:

First/Single Video : GOPRnnnn.mp4
Chapter videos     : GPccnnnn.mp4

Merged video is saved as GOPRnnnn_merged.mp4

Existing merged videos are not overwritten.


Created on Fri Aug 17 09:40:08 2018
@author: rarossi
"""
import os
from glob import glob
import os.path as path
import subprocess


def find_videos():
    videos_2_merge = dict()
    for fname in glob('GOPR????.MP4'):
        #                                          GOPRnnnn.mp4 -> nnnn
        videos_2_merge[fname] = find_chapters(path.splitext(fname)[0][4:])

    return videos_2_merge


def find_chapters(fnumber):
    chapters_fnames = list()
    for chapter in range(1, 100):
        chapter_file = 'GP%02d%s.MP4' % (chapter, fnumber)
        if not path.exists(chapter_file):
            break
        else:
            chapters_fnames.append(chapter_file)
    return chapters_fnames


def merged_filename(filename):
    name, ext = path.splitext(filename)
    return '%s_merged%s' % (name, ext)


def merge(base, chapters):
    '''Merge base and chapters in one video using ffmpeg. '''

    with open('input_list.txt', 'w') as fout:
        for vid in (base, *chapters):
            fout.write("file '%s'\n" % vid)

    print('    Merging chapters')
    cmd = ['ffmpeg', 
           '-hide_banner',
           '-loglevel', 'warning', 
           '-stats',
           '-f', 'concat', 
           '-i', 'input_list.txt', 
           '-c', 'copy', 
           '%s' % (merged_filename(base))]
    proc = subprocess.run(cmd)
    
    if proc.returncode > 0:
        print('==> Something went wrong.')

    os.remove('input_list.txt')



def main():

    print('Find and merge gopro video chapters.')

    vids = find_videos()
    for base in vids:
        print('\n\n', '*'*80, '\n', base, '\n')
        chaps = vids[base]

        if len(chaps) == 0:
            print('    This video has no chapters.')
            continue
        else:
            print('    %d chapters found.' % len(chaps))

        if path.exists(merged_filename(base)):
            print('    Chapters already merged. Not overwriting. Skipping.')
            continue

        merge(base, chaps)


if __name__ == '__main__':
    main()
