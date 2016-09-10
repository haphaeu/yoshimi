'''
Find potential corrupted image files.

by raf, 10-09-2016
'''
from PIL import Image
from shutil import copyfile
import os

# Base folder for the image albuns
db = r'E:\tmp'

# Extensions to analyse
extensions = {'.jpg', '.jpeg', '.bmp', '.png', '.gif'}

# Where to save corrupted files, set to False not to save them
save_corrupted = r'E:\tmp\__corrupted__'

# Delete corrupted files
# Carefull with this flag
# Runs first saving corrupted files somewhere by setting
#    save_corrupted = True
# then look at the files and finally set this flag to True
delete_corrupted = True

# prints name of every image file analysed during run
verbose = False

# #################################################################################################

print('Checking integrity of image files in %s' % db)

if not os.path.exists(save_corrupted):
    os.mkdir(save_corrupted)

ct_dir, ct_tot, ct_img, ct_inv = 0, 0, 0, 0
for rt, dirs, files in os.walk(db):
    if rt == save_corrupted:
        continue  # skip this folder
    if verbose: print(rt)
    ct_dir += 1
    for fname in files:
        ct_tot += 1
        if os.path.splitext(fname)[-1].lower() in extensions:
            ffname = os.path.join(rt, fname)
            if os.path.exists(ffname):
                try:
                    ct_img += 1
                    if verbose: print '   %s' % fname
                    fp = open(ffname, 'rb')
                    im = Image.open(fp)
                    im.verify()
                    fp.close()
                except IOError:
                    ct_inv += 1
                    fp.close()
                    # file exists, possible IO error is invalid (corrupted) file
                    print 'Invalid image file %s' % ffname
                    if save_corrupted:
                        copyfile(ffname, os.path.join(save_corrupted,
                                                      ffname.replace('\\', '-').replace(':', '')))
                    if delete_corrupted:
                        os.remove(ffname)

# some statistics
print('Finished.\n---')
print('Walked through %d directories' % ct_dir)
print('Found a total of %d files' % ct_tot)
print('Found %d image files' % ct_img)
print('Invalid image files %d' % ct_inv)
if ct_inv:
    if save_corrupted:
        print('Invalid image files saved to %s' % save_corrupted)
    if delete_corrupted:
        print('Invalid images deleted')
