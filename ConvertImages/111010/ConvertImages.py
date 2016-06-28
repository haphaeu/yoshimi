#
# ConvertImages.py
#
# Converts all images in all subfolders and saves
# them into another folder
#
# This script uses ImageMagick - so make sure to have it available
#
# R Rossi, 10th October 2011
#
# bugs conhecidos:
# - quando o arquivo jpg de entrada esta corrompido e a saida nao eh
#   gerada, o calculo final de estatisticas dah erro pois tenta
#   acessar um arquivo inexistente. duas ideias pra contornar isso:
#       . implementar um try/except e contar quantos arquivos deram pau
#       . foda-se, deixa assim...
#

import os

#input folder with original files (won't be harmed :)
#and folder to output converted pictures
#both need to exist
inp_path='/media/Samsung250GB/Pictures_Reduced/1280px_70q/2011/111222_Peru/'
out_path='/media/Samsung250GB/Pictures_Reduced/800px_40q/2011/111222_Peru/'

#conversion options
#input 0 (zero) to disable
#resize is in pixels, will apply for the larger picture dimension
#aspect ratio will be kept
#quality is the jpeg compression quality in %
#
# comments after running the script:
# had ~70GB of pictures (34k files)
# using 1280px & 70%, reduced to 6GB (11x)
# using 800px & 40%, reduced to 2GB (35x)
resize = 800
quality = 40

#ok, ok...could have input the folders and convertion settings as
# sys.argv[]... but, seriously, how many time am I running this script :P

#check existence of input and output paths
if not ( os.path.exists(inp_path) and os.path.exists(out_path) ):
    print "Input and output paths must exist"
else:
    print "Converting all jpg files in \"", inp_path, "\" into \"", out_path,"\"."
    if resize: print "Applying smart resize to ", resize, "px."
    if quality: print "Applying JPEG quality of ", quality, "%."
    
    # this returns a 3-tuple for every
    # subdirectory, including root, with:
    # directory, sub-directories, files
    tmp=os.walk(inp_path)

    # this searches for all jpg files
    # in all subfolders
    jpg_files=[]
    for root, subdirs, files in tmp:
        for names in files:
            file=os.path.join(root,names)
            name,ext=os.path.splitext(file)
            if ext.lower()=='.jpg':     #!!! note that .jpeg are ignored
                jpg_files.append(file)
    num_files=len(jpg_files)
    print "Found ", num_files, " jpg files."
    #list to be filled with output jpg files
    out_jpg=[]
    i=0
    for jpg in jpg_files:
        i+=1
        #split the input file into path and name
        inp_dir, inp_file=os.path.split(jpg)
        #this simple command below builds the path were the output file will be saved
        out_dir=os.path.join(out_path,os.path.split(os.path.relpath(jpg,inp_path))[0])
        #and finally the output path and filename are merged together
        #note that although inp_file is only a filename, out_file has the complete path
        #ok, yes, this is not that convenient, but... fuck off...
        out_file= os.path.join(out_dir,inp_file)
        #update the list with the output files (with complete path)
        out_jpg.append(out_file)
        #check existence of output folder, if it doens't exist, create it
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        print "(",i,"/",num_files,") Converting ", jpg, " into ", out_dir, ""
        #converting files...
        #prepare command and run it
        #command convert from ImageMagick is called
        cmd = "convert"
        if resize:
            cmd+=" -resize "+str(resize)
        if quality:
            cmd+=" -quality "+str(quality)
        cmd+=" \""+jpg+"\" \""+out_file+"\""
        os.system(cmd)
    print "Convertions finished. Calculating statictics."
    #Statistics calculations Tabajara Inc! it is only a size compare :p
    #Calculate size of input files and format string to display
    inp_size=float(sum([os.path.getsize(jpg) for jpg in jpg_files]))
    if inp_size < 1024:
        inp_unit="B"
    elif inp_size < 1048576:
        inp_size/=1024
        inp_unit="kB"
    elif inp_size < 1073741824:
        inp_size/= 1048576
        inp_unit="MB"
    else:
        inp_size/=1073741824
        inp_unit="GB"
    #Calculate size of converted files and format string to display
    out_size=float(sum([os.path.getsize(jpg) for jpg in out_jpg]))
    if out_size < 1024:
        out_unit="B"
    elif out_size < 1048576:
        out_size/=1024
        out_unit="kB"
    elif out_size < 1073741824:
        out_size/= 1048576
        out_unit="MB"
    else:
        out_size/=1073741824
        out_unit="GB"
    #Print out stats:
    print "Original input files consume %0.2f%s" % (inp_size, inp_unit)
    print "Converted output files consume %0.2f%s" % (out_size, out_unit)
    print "Done."
