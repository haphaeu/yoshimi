# -*- coding: utf-8 -*-
"""
 ConvertImages.py

 Converts all images in all subfolders and saves
 them into another folder

 This script uses ImageMagick - so make sure to have it available

 R Rossi, 10th October 2011

 bugs conhecidos:
 - quando o arquivo jpg de entrada esta corrompido e a saida nao eh
   gerada, o calculo final de estatisticas dah erro pois tenta
   acessar um arquivo inexistente. duas ideias pra contornar isso:
       . implementar um try/except e contar quantos arquivos deram pau
       . foda-se, deixa assim...
       -> FOI CORRIGIDO, IMPLEMENTANDO UM TRY NO SIZE COUNTING

 added on the 16 Janeiro 2012:
 - corrigido bug citado acima
 - adicionado verificacao do arquivo de saida - se ele ja existir,
   a conversao nao eh feita para nao sobre-escreve-lo. o loop
   pula este arquivo e continua normalmente

 added on the 17 Janeiro 2012:
 - parametros entrados como argumentos:
    ConvertImages size quality input_path output_path
 - added support to extension .jpeg
 - added warning rgd lack of support for some non-jpg files
 - added sanity check in the input size and jpg quality

 modified 13 December 2014:
 - comand 'convert' conflicts with windows command, so the
    full path to convert.exe is entered.
 - os.system(cmd) gives too much problem with shity windows
    replaced by subprocess.call()
 - WINDOWS EH UMA MERDA. Por alguma razao este script nao rodou no cmd,
    mas rodou dentro do Spyder, com uns tricks pra pegar sys.argv corretamente

 29 Marco 2016
 convertido para python 3

 15 November 2016
 PEP8
"""

import os
import sys
import subprocess


class ArgError(BaseException):
    pass


class QuietError(BaseException):
    pass

convertPath = os.path.normpath("c:\\ImageMagick\\convert.exe")
# sys.argv=['',
#            1280,
#            70,
#            os.path.normpath('F:/Minhas imagens/2011'),
#            os.path.normpath('d:/fotos & videos/1280px_70q/2011')]

try:
    if not len(sys.argv) == 5:
        raise ArgError

    # at some point in the past I wrote that:
    #    ok, ok...could have input the folders and convertion settings as
    #    sys.argv[]... but, seriously, how many time am I running this script :P
    # and finally, I decided to implement it... 'cause yes, I'm using this
    # script more often...

    # conversion options
    # input 0 (zero) to disable
    # resize is in pixels, will apply for the larger picture dimension
    # aspect ratio will be kept
    # quality is the jpeg compression quality in %
    #
    #  comments after running the script:
    #  had ~70GB of pictures (34k files)
    #  using 1280px & 70%, reduced to 6GB (11x)
    #  using 800px & 40%, reduced to 2GB (35x)
    # resize = 800
    # quality = 40
    try:
        resize = int(sys.argv[1])
        quality = int(sys.argv[2])
    except:
        raise ArgError
    # some sanity check in the inputs
    if quality < 10 or quality > 100:
        print("Error: jpeg quality should be between 10 and 100.")
        raise QuietError
    if resize < 100 or resize > 5000:
        print("Sanity error: size is constraint between 100 and 5000.")
        raise QuietError

    # input folder with original files (won't be harmed :)
    # and folder to output converted pictures
    # both need to exist
    # inp_path='/media/Samsung250GB/Pictures_Reduced/1280px_70q/2011/111222_Peru/'
    # out_path='/media/Samsung250GB/Pictures_Reduced/800px_40q/2011/111222_Peru/'
    try:
        inp_path = sys.argv[3]
        out_path = sys.argv[4]
    except:
        raise ArgError

    # work with abs paths
    inp_path, out_path = os.path.abspath(inp_path), os.path.abspath(out_path)

    # check existence of input path
    if not os.path.exists(inp_path):
        print("Input path must exist.")
        raise QuietError
    # check for output path
    # it cannot be a sub-directory to input path
    if os.path.commonpath((inp_path, out_path)) == inp_path:
        print('Error: Output path is a sub-folder to input path. ')
        raise QuietError
    # check for existence, if not, create
    if not os.path.exists(out_path):
        print('Creating output path {}'.format(out_path))
        os.makedirs(out_path)

    # jetzt geht es los

    print("Converting all image files in \"", inp_path, "\" into \"", out_path, "\".")
    if resize: print("Applying smart resize to ", resize, "px.")
    if quality: print("Applying JPEG quality of ", quality, "%.")

    # this returns a 3-tuple for every
    # subdirectory, including root, with:
    # directory, sub-directories, files
    tmp = os.walk(inp_path)

    # this searches for all jpg files
    # in all subfolders
    jpg_files = []
    supported_extensions = {'.jpg', '.jpeg'}
    unsupported_extensions = {'.gif', '.tiff', '.png', '.wmf', '.emf', '.bmp', '.img'}
    for root, subdirs, files in tmp:
        for names in files:
            file = os.path.join(root, names)
            name, ext = os.path.splitext(file)
            # old approach...too restrictive
            # if ext.lower() in supported_extensions:
            #     jpg_files.append(file)
            # if ext.lower() in unsupported_extensions:
            #    print("Warning: found non-jpg pictures. They're won't be processed.")
            # new approach, try to convert everything
            jpg_files.append(file)

    num_files = len(jpg_files)
    print("Found ", num_files, " files.")
    # list to be filled with output jpg files
    valid_inp, out_jpg = [], []
    i = 0
    for jpg in jpg_files:
        i += 1
        # split the input file into path and name
        inp_dir, inp_file = os.path.split(jpg)
        # this simple command below builds the path were the output file will be saved
        out_dir = os.path.join(out_path, os.path.split(os.path.relpath(jpg, inp_path))[0])
        # and finally the output path and filename are merged together
        # note that although inp_file is only a filename, out_file has the complete path
        # ok, yes, this is not that convenient, but... fuck off...
        out_file = os.path.join(out_dir, os.path.splitext(inp_file)[0]+'.jpg')
        # check is output file exists, if it does, does not proceed
        if os.path.exists(out_file):
            print("File %s already exists, will NOT be overwriten, skipping." % out_file)
            continue
        # check existence of output folder, if it doens't exist, create it
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        print("(", i, "/", num_files, ") Converting ", jpg, " into ", out_dir, "")
        # converting files...
        # prepare command and run it
        # command convert from ImageMagick is called
        cmd = [convertPath]
        if resize:
            cmd.append("-resize")
            cmd.append(str(resize))
        if quality:
            cmd.append("-quality")
            cmd.append(str(quality))
        cmd.append(os.path.normpath(jpg))
        cmd.append(os.path.normpath(out_file))
        # print cmd
        proc = subprocess.Popen(cmd)
        if not proc.wait():
            # success. update the list with the output files (with complete path)
            out_jpg.append(out_file)
            valid_inp.append(inp_file)
        else:
            # failed attempt to convert
            print('Failed converting this file. Invalid image file?')

    print("Convertions finished. Calculating statistics.")
    print("Converted ", len(out_file), " files.")
    # Statistics calculations Tabajara Inc! it is only a size compare :p
    # Calculate size of input files and format string to display
    inp_size = float(sum([os.path.getsize(inp) for inp in valid_inp]))
    if inp_size < 1024:
        inp_unit = "B"
    elif inp_size < 1048576:
        inp_size /= 1024
        inp_unit = "kB"
    elif inp_size < 1073741824:
        inp_size /= 1048576
        inp_unit = "MB"
    else:
        inp_size /= 1073741824
        inp_unit = "GB"
    # Calculate size of converted files and format string to display
    # deprecated: out_size=float(sum([os.path.getsize(jpg) for jpg in out_jpg]))
    # the for below with a try is implemented because sometimes the conversion
    # fails and the output file is not created, resulting in an error during
    # size calculation
    out_size = 0
    for jpg in out_jpg:
        try:
            tmp = os.path.getsize(jpg)
            out_size += tmp
        except:
            pass
    if out_size < 1024:
        out_unit = "B"
    elif out_size < 1048576:
        out_size /= 1024
        out_unit = "kB"
    elif out_size < 1073741824:
        out_size /= 1048576
        out_unit = "MB"
    else:
        out_size /= 1073741824
        out_unit = "GB"
    # Print out stats:
    print("Original input files consume %0.2f%s" % (inp_size, inp_unit))
    print("Converted output files consume %0.2f%s" % (out_size, out_unit))
    print("Done.")

except ArgError:
    print("Error in the arguments.")
    print("Use: ConvertImages size quality input_path output_path")
    print("   - size is in pixels, will apply for the larger picture dimension,")
    print("     aspect ratio will be kept")
    print("   - quality is the jpeg compression quality in %")
    print("   - set any of the above to 0 to disable it")
    print("   - input and output paths must exist")
except QuietError:
    raise SystemExit
except:
    print("Unkown error.")
    raise SystemExit
