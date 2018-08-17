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
    for fname in glob('GOPR????.mp4'):
        #                                          GOPRnnnn.mp4 -> nnnn
        videos_2_merge[fname] = find_chapters(path.splitext(fname)[0][4:])

    return videos_2_merge


def find_chapters(fnumber):
    chapters_fnames = list()
    for chapter in range(1, 100):
        chapter_file = 'GP%02d%s.mp4' % (chapter, fnumber)
        if not path.exists(chapter_file):
            break
        else:
            chapters_fnames.append(chapter_file)
    return chapters_fnames


def merged_filename(filename):
    name, ext = path.splitext(filename)
    return '%s_merged%s' % (name, ext)


def merge(base, chapters):
    '''
    # https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg#11175851

    # prefered option - not working on my work laptop
    ffmpeg -f concat -i mylist.txt -c copy output.mp4


    # this one doesnt seem to work - only first video is copied, also not supposed to work for mp4
    ffmpeg -i concat:input1.mp4^|input2.mp4 -codec copy output.mp4

    #this is doing the job - people are saying transcode is not necessary though...
    ffmpeg -i test1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts temp1.ts
    ffmpeg -i test2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts temp2.ts
    // now join
    ffmpeg -i "concat:temp1.ts|temp2.ts" -c copy -bsf:a aac_adtstoasc output.mp4

    #there is also this:
    # https://stackoverflow.com/questions/5415006/ffmpeg-combine-merge-multiple-mp4-videos-not-working-output-only-contains-the?noredirect=1&lq=1
    '''

    ffmpeg = 'C:/Users/rarossi/portable/ffmpeg/bin/ffmpeg.exe'

    print('    Transcoding chapters of %s:' % base)
    cmd_concat = ''
    for i, vid in enumerate((base, *chapters)):
        cmd = ffmpeg + ' -loglevel 24 -y -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts temp%d.ts' % (vid, i)
        print('        ', vid, '...')
        proc = subprocess.run(cmd)

        if proc.returncode > 0:
            print('Error. Skipping.')
            cleanup()
            return False

        if i > 0:
            cmd_concat += '|'
        cmd_concat += 'temp%d.ts' % i

    print('    Merging chapters')
    cmd_concat = ffmpeg + ' -loglevel 24 -i "concat:%s" -c copy -bsf:a aac_adtstoasc %s' % (
            cmd_concat, merged_filename(base))
    proc = subprocess.run(cmd_concat)

    cleanup()


def cleanup():
    for tmp in glob('temp*.ts'):
        os.remove(tmp)


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
