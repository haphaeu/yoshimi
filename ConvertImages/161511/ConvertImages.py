# -*- coding: utf-8 -*-
"""
 ConvertImages.py

 Recursively finds all image files from a given root path and re-code them
 using ImageMagick convert function. The converted images are saved in a
 given output path, keeping the same sub-directories structure.
 
 The input files are preserved.

 This script uses ImageMagick - so make sure to have it available

 by R Rossi, 10th October 2011
"""

import os
import sys
import subprocess
from math import log

# Path to ImageMagick convert function
CONVERT_PATH = os.path.normpath("c:/users/rarossi/portable"
                                "/ImageMagick/convert.exe")

# #############################################################################
# Classes to handle exceptions


class ArgError(BaseException):
    pass


class QuietError(BaseException):
    pass

# #############################################################################
# Helper function to print final sizes


def get_formatted_size(size):
    '''1024 -> 1 kB'''

    if size == 0:
        return '0 B'

    units = ['B', 'kB', 'MB', 'GB', 'TB']
    order = int(log(size, 1024))

    return '%.1f %s' % (size / (1024**order), units[order])


# #############################################################################
# ### Argument parsing and sanity checks ###
try:

    if not len(sys.argv) == 5:
        raise ArgError

    try:
        resize = int(sys.argv[1])
        quality = int(sys.argv[2])
    except:
        raise ArgError
    # Some sanity check in the inputs
    if quality < 10 or quality > 100:
        print("Error: jpeg quality should be between 10 and 100.")
        raise QuietError
    if resize < 100 or resize > 5000:
        print("Sanity error: size is constraint between 100 and 5000.")
        raise QuietError

    # Input folder with original files (won't be harmed :)
    # and folder to output converted pictures. Both need to exist
    try:
        inp_path = sys.argv[3]
        out_path = sys.argv[4]
    except:
        raise ArgError

    # Work with abs paths
    inp_path, out_path = os.path.abspath(inp_path), os.path.abspath(out_path)

    # Check existence of input path
    if not os.path.exists(inp_path):
        print("Input path must exist.")
        raise QuietError
        
    # Check for output path. It cannot be a sub-directory to input path
    if os.path.commonpath((inp_path, out_path)) == inp_path:
        print('Error: Output path is a sub-folder to input path. ')
        raise QuietError

except ArgError:
    print("Error in the arguments.")
    print("Use: ConvertImages size quality input_path output_path")
    print("   - size in pixels, will apply for the larger picture dimension,")
    print("     aspect ratio will be kept")
    print("   - quality is the jpeg compression quality in %")
    print("   - set any of the above to 0 to disable it")
    print("   - input and output paths must exist")
    raise SystemExit
    
except QuietError:
    raise SystemExit
    
except BaseException as err:
    print("Unkown error.")
    print(err)
    raise SystemExit

# Check for existence, if not, create
if not os.path.exists(out_path):
    print('Creating output path {}'.format(out_path))
    os.makedirs(out_path)

print("Converting all image files in \"", inp_path, 
      "\" into \"", out_path, "\".")
if resize: print("Applying smart resize to ", resize, "px.")
if quality: print("Applying JPEG quality of ", quality, "%.")

# #############################################################################
# ### Find all files in input path and attempt to convert them ###

# Create a list of all *candidates* to be converted
# Aggressive approach: list all files. 
all_files_full_path = []
for root, subdirs, files in os.walk(inp_path):
    for names in files:
        all_files_full_path.append(os.path.join(root, names))

num_files = len(all_files_full_path)
print("Found ", num_files, " files.")

# list to be filled with valid input and output files
all_inp_full_path, all_out_full_path = [], []

for i, image_file_full_path in enumerate(all_files_full_path):

    print("(", i + 1, "/", num_files, ") Converting", 
          image_file_full_path, end='. ')

    # split the input file into path and name
    inp_dir, inp_filename = os.path.split(image_file_full_path)
    
    # output file full path 
    out_dir = os.path.join(out_path, 
                           os.path.split(os.path.relpath(image_file_full_path, 
                                                         inp_path))[0])
    
    # and finally the output path and filename are merged together
    # note that inp_filename is only a filename (no path)
    out_filename_full_path = os.path.join(out_dir, 
                                          os.path.splitext(inp_filename)[0] 
                                          + '.jpg')
    
    # check if output file exists, if it does, does not proceed
    if os.path.exists(out_filename_full_path):
        print("Output file exists, will NOT be overwriten.")
        continue
        
    # check existence of output folder, if it doens't exist, create it
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # prepare command and run it
    # command convert from ImageMagick is called
    cmd = [CONVERT_PATH]
    if resize:
        cmd.append("-resize")
        cmd.append(str(resize))
    if quality:
        cmd.append("-quality")
        cmd.append(str(quality))
    cmd.append(os.path.normpath(image_file_full_path))
    cmd.append(os.path.normpath(out_filename_full_path))

    proc = subprocess.Popen(cmd, 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
    if not proc.wait():
        # success. update the list with the output files (with complete path)
        all_out_full_path.append(out_filename_full_path)
        all_inp_full_path.append(image_file_full_path)
    else:
        # failed attempt to convert
        print('FAILED. Invalid image file?', end='')
    print(' ')

print("Convertions finished. Calculating statistics.")
print("Converted ", len(all_out_full_path), " files.")

# #############################################################################
# ### Final statistics ###

# Calculate size of input files
inp_size = float(sum([os.path.getsize(inp) for inp in all_inp_full_path]))

# Calculate size of converted files 
out_size = 0
for jpg in all_out_full_path:
    try:
        tmp = os.path.getsize(jpg)
        out_size += tmp
    except FileNotFoundError:
        pass

# Print out stats:
print("Original input files consume %s" % get_formatted_size(inp_size))
print("Converted output files consume %s" % get_formatted_size(out_size))
print("Done.")
