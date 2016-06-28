#!/usr/bin/env python

# Download subtitles from opensubtitles.org
# Default language is english, to change the language change sublanguageid parameter
# in the searchlist.append function

# Carlos Acedo (carlos@linux-labs.net)
# Inspired by subdownloader
# License GPL v2

import os
import sys
from struct import *
from sys import argv
from xmlrpclib import ServerProxy, Error

def hashFile(name): 
      try: 
            longlongformat = 'Q'  # unsigned long long little endian
            bytesize = calcsize(longlongformat) 
            format= "<%d%s" % (65536//bytesize, longlongformat)

            f = open(name, "rb") 
                    
            filesize = os.fstat(f.fileno()).st_size
            hash = filesize 
            
            if filesize < 65536 * 2: 
               return "SizeError" 
            
            buffer= f.read(65536)
            longlongs= unpack(format, buffer)
            hash+= sum(longlongs)
            
            f.seek(-65536, os.SEEK_END) # size is always > 131072
            buffer= f.read(65536)
            longlongs= unpack(format, buffer)
            hash+= sum(longlongs)
            hash&= 0xFFFFFFFFFFFFFFFF
            
            f.close() 
            returnedhash =  "%016x" % hash 
            return returnedhash 
                 
      except(IOError): 
                os.system('kdialog --error "Input/Output error while reading file hash"')
                return "IOError"

# ================== Main program ========================

server = ServerProxy("http://api.opensubtitles.org/xml-rpc")
peli = argv[1]
################################################################
# Use kdialog?
# Type "True" if you want to use kdialog or "False" otherwise.
################################################################
use_kdialog = False

try:
    myhash = hashFile(peli)
    print 'myhash = %s' % myhash
    size = os.path.getsize(peli)
    session =  server.LogIn("","","en","OS Test User Agent")
    
    #print session
    token = session["token"]
    
    searchlist = []
    searchlist.append({'sublanguageid':'eng,pob,spa,fre','moviehash':myhash,'moviebytesize':str(size)})
    #searchlist.append({'sublanguageid':'all','moviehash':myhash,'moviebytesize':str(size)})
    #print "searchlist: %s" % searchlist
    
    moviesList = server.SearchSubtitles(token, searchlist)
    if moviesList['data']:
		mindex = 0
		kdialog_items = ''
		kdialog_items_dict = {}
		for item in moviesList['data']:
			#print "item: %s" % item
			kdialog_items = kdialog_items + '"' + str(mindex) + '" "' + item['SubFileName'] + "(" + item['SubLanguageID'] + item['SubRating'] + ")" + '" '
			kdialog_items_dict[mindex] = item['SubFileName'] + "(" + item['SubLanguageID'] + item['SubRating'] + ")"
			mindex = mindex + 1
		print "*" * 50	
		print "kdialog_items: %s" % kdialog_items
		print "*" * 50
		if use_kdialog:
			resp = os.popen('kdialog --geometry 400x200 --menu "Select subtitle" ' + kdialog_items).readline()
		else:
			for k,v in kdialog_items_dict.items():
				print "(%s) %s" % (k,v)
			if kdialog_items_dict:
				resp = raw_input("Choose one of the above subtitles: ")
				print "Choosed number: %s" % resp
		print '*' * 50
		subFileName = os.path.basename(peli)[:-3] + moviesList['data'][int(resp)]['SubFileName'][-3:]
		subDirName = os.path.dirname(peli)
		subURL = moviesList['data'][int(resp)]['SubDownloadLink']
		response = os.system('wget -O - ' + subURL + ' | gunzip  > "' + subDirName + '/' + subFileName + '"' )
		print 'wget -O - ' + subURL + ' | gunzip  > "' + subDirName + '/' + subFileName + '"' 
		if response != 0:
			if use_kdialog:
				os.system('kdialog --error "An error ocurred downloading or writing the subtitle"')
			else:
				print "An error ocurred downloading or writing the subtitle"
				sys.exit(1)
		
    else:
		if use_kdialog:
			os.system('kdialog --error "No subtitles found"')
		else:
			print "No subtitles found"
			sys.exit(1)
    server.Logout(session["token"])
except Error, v:
	if use_kdialog:
		os.system('kdialog --error "An error ocurred: %s"' % v)
	else:
		print "An error ocurred: %s" % v



