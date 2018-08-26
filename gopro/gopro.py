# -*- coding: utf-8 -*-
"""

Process gopro videos in working directory.

Merge multi-chapter videos.

Optinaly re-encode and scale videos.

Videos are found by file name pattern. Implemented for Hero3:

First/Single Video : GOPRnnnn.mp4
Chapter videos     : GPccnnnn.mp4

Merged and re-encoded videos are saved as GOPRnnnn_out.mp4

Existing output files are not overwritten.


Created on Fri Aug 17 09:40:08 2018
@author: rarossi
"""
import os
import sys
from glob import glob
import os.path as path
import subprocess


def find_videos():
    '''Find all base gopro videos.'''
    videos_2_merge = dict()
    for fname in glob('GOPR????.MP4'):
        #                                          GOPRnnnn.mp4 -> nnnn
        videos_2_merge[fname] = find_chapters(path.splitext(fname)[0][4:])

    return videos_2_merge


def find_chapters(fnumber):
    '''Find files for multi-chapters videos.'''
    chapters_fnames = list()
    for chapter in range(1, 100):
        chapter_file = 'GP%02d%s.MP4' % (chapter, fnumber)
        if not path.exists(chapter_file):
            break
        else:
            chapters_fnames.append(chapter_file)
    return chapters_fnames


def out_filename(filename):
    '''Filename to save processed output video.'''
    name, ext = path.splitext(filename)
    return '%s_out%s' % (name, ext)


def process(base, chapters, crf=False, scale=False):
    '''Process base and, if present, chapters.
    Merge base and chapters into one video.
    Re-encode if crf and scale given.
    For single videos, call only makes sense for re-encoding and scaling.
    '''

    if not chapters and not crf and not scale:
        # Nothing to do if video has no chapters and no re-code/scale are given.
        return 

    with open('input_list.txt', 'w') as fout:
        for vid in (base, *chapters):
            fout.write("file '%s'\n" % vid)

    print("    Processing video with ffmpeg.\n")

    # General ffmpeg options
    cmd = ['ffmpeg', 
           '-hide_banner',
           '-loglevel', 'warning', 
           '-stats',
           '-safe', '0',
           '-f', 'concat',  # concat works even in single file
           '-i', 'input_list.txt']

    # Copy stream - no re-encoding required 
    if not crf and not scale:
        cmd.extend(['-c', 'copy'])  # do not re-encode

    # Re-encode video
    else:
        cmd.extend(['-c:v', 'libx265'])  # re-encode to h265
        cmd.extend(['-crf', '%d' % crf])  # compression. higher number gives lower quality
        cmd.extend(['-c:a', 'copy'])  # copy audio

    # Scale video resolution. Note this requires re-encoding.
    if scale:
        cmd.extend(['-vf', 'scale=iw*{0:.3f}:ih*{0:.3f}'.format(scale)])  # scale video resolution

    # Finally, output file name
    cmd.append('%s' % (out_filename(base)))
    
    proc = subprocess.run(cmd)
    
    if proc.returncode > 0:
        print('==> Something went wrong.')

    os.remove('input_list.txt')

    
def help():
        print('Use: gopro [-c crf [-s scale]]')
        print()
        print('  -c crf   : compression for re-encoding. Higher number gives lower quality.')
        print('             From 0 (lossless) to 50 (worst quality). ')
        print()
        print('  -s scale : Scale for resize, as a fraction of original size.')
        print('             Implies -c 25 if not given.')
        print()
        print('  If no options given, videos will not be re-encoded. Only multi-chapters will be merged.')
    

def main():

    print('Process gopro videos: merge multi-chapters and optionally re-encode and scale.')

    # Parsing input arguments
    
    crf = False
    scale = False

    options = iter(sys.argv[1:])
    for arg in options:
        
        if arg in ('-h', '--help'):
            help()
            sys.exit(0)

        elif arg == '-c':
            arg = next(options, None)
            try:
                crf = int(arg)
            except (ValueError, TypeError):
                print('Error in -c option: cannot convert %s to integer.' % arg)
                sys.exit(1)
            except IndexError:
                print('Missing argument crf.')
                sys.exit(1)
            if not 0 <= crf <= 50:
                print('Error: crf must be between 0 and 50.')
                sys.exit(1)
            continue

        elif arg == '-s':
            arg = next(options, None)
            try:
                scale = float(arg)
            except (ValueError, TypeError):
                print('Error in -s option: cannot convert %s to float.' % arg)
                sys.exit(1)
            except IndexError:
                print('Missing argument scale.')
                sys.exit(1)
             
            continue

        else:
            print('Unknown argument: %s' % arg)
            sys.exit(1)

    # If scale is input but crf is not, re-encode assuming crf og 25
    if scale and not crf:
        crf = 25

    # Print summary of options
    print()
    print('Input options:')
    
    if not crf and not scale:
        print('  Only merging multi-chapter videos.')

    if crf:
        print('  Re-encoding with compression %d' % crf)
    else:
        print('  Copy original encoding.')
    if scale:
        print('  Scaling video to %.3f' % scale)
        if scale > 1:
            print('Warning: scale > 1')
    else:
        print('  Using original resolution.')
    


    vids = find_videos()
    for base in sorted(vids.keys()):
        print('\n\n', '*'*80, '\n', base, '\n')
        chaps = vids[base]

        if len(chaps) == 0:
            print('    This is a single video.')
            if not crf:  # and not scale  # only merging, skip single files
                print('    Nothing to do.')
                continue
        else:
            print('    %d chapters found.' % len(chaps))

        if path.exists(out_filename(base)):
            print('    Output file exists. Not overwriting.')
            continue

        process(base, chaps, crf=crf, scale=scale)


if __name__ == '__main__':
    main()
