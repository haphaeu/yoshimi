#!/usr/bin/env python
#Written by Jarrod Lombardo,
#Copylefted under GPL, 2004 (http://www.gnu.org/copyleft/gpl.html)

#relister.py Usage documentation
#executable input_file output_file

#Documentation:
#Key stroke    Function
#q             quit, discarding changes
#w             write and quit
#up-arrow      move cursor up
#down-arrow    move cursor down
#left-arrow    move item up
#right-arrow   move item down

#definitions
#input-file: a text file which is a list, separated by '\n'
#output-file: a text file which is a list, separated by '\n',
#             generated by this program

import sys, curses, os.path

# - - - - - o p e n f i l e s - - - - - 
def openfiles(argv):
    """Open the 2 files named in argv[1] and argv[2] or error
    """

    #check if the args are there
    if (len(argv) != 3):
        sys.stderr.write("Usage " + argv[0] + " input_file output_file\n")
        sys.exit(0)

    #error if the files are the same
    if (os.path.realpath(argv[1]) == os.path.realpath(argv[2])):
        sys.stderr.write("Usage " + argv[0] + " input_file output_file\n")
        sys.stderr.write(
            "input_file and output_file must be different files.\n")
        sys.stdout.write(
            "Please re-run the program with a different output file.\n")
        sys.exit(0)

    #prompt if the output_file exists
    if os.path.isfile(argv[2]):
        sys.stdout.write("\n" + os.path.basename(argv[2]) + " exists.\n")
        ynval = raw_input("Would you like to overwrite it (y/n)?")
        if (ynval[0].upper() != 'Y'):
            sys.stdout.write(
                "Please re-run the program with a different output file.\n")
            sys.exit(0)

    #actually open the files
    return file(argv[1]), file(argv[2], 'w')

# - - - - - i n i t i a l i z e E v e r y t h i n g - - - - -
def initialize(stdscr, itemlist):
    """Initialize the screen and all of the positions.
    """
    ymax, xmax = stdscr.getmaxyx() #the size of the window
    stdscr.move(0, 0) #move the the top left corner (it should already
                      #be there (at 0,0), but do it just in case).

    #Print ymax lines to the screen
    yoffset = 0
    for line in itemlist:
        if (yoffset <= ymax - 2):

            #it's really anoying, but the next 2 lines must be
            #separate for it to work.
            line = '%.4d ' + line
            line = line % (yoffset)
            stdscr.addnstr(yoffset, 0, line, xmax - 1)

            #move down one line
            yoffset += 1

        else:
            break
    
    #create the cursor (highlight) initial position
    line = '0000 ' + itemlist[0]
    stdscr.addnstr(0, 0, line, xmax - 1, curses.A_REVERSE)
    stdscr.move(0, 0)

    #refresh the screen
    stdscr.refresh()

    return (stdscr, itemlist, 0)
    
# - - - - - c u r d o w n - - - - -
def curdown(stdscr, itemlist, listpos):
    """Move the cursor down one line.
    """
    #if at bottom of list, do nothing
    if (len(itemlist) - 1 == listpos):
        return (stdscr, itemlist, listpos)

    ymax, xmax = stdscr.getmaxyx()
    ycur, xcur = stdscr.getyx()

    #if at bottom of screen
    if (ycur == ymax - 2):
        #shift all items up one line on the screen
        stdscr.move(0,0)
        stdscr.deleteln() #removes the line at 0,0 and moves all
                          #other lines up one

        #display itemlist[listpos] as A_NORMAL
        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur - 1, 0, line1, xmax - 1)
        
        #display itemlist[listpos + 1] as A_REVERSE
        listpos = listpos + 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur, 0)
        
    #if anywhere else
    else:
        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur, 0, line1, xmax - 1)

        listpos += 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur + 1, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur + 1, 0)

    return (stdscr, itemlist, listpos)

# - - - - - c u r u p - - - - -
def curup(stdscr, itemlist, listpos):
    """Move the cursor up one line.
    """
    #if at top of list, do nothing
    if (0 == listpos):
        return (stdscr, itemlist, listpos)

    ymax, xmax = stdscr.getmaxyx()
    ycur, xcur = stdscr.getyx()

    #if at top of screen
    if (ycur == 0):
        #shift all items down one line on the screen
        stdscr.move(0, 0)
        stdscr.insertln() #inserts a blank line at 0,0 and moves all other
                          #lines down one
        stdscr.move(ymax-1, 0)
        stdscr.deleteln()

        #display itemlist[listpos] as A_NORMAL
        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur + 1, 0, line1, xmax - 1, curses.A_NORMAL)
        
        #display itemlist[listpos + 1] as A_REVERSE
        listpos -= 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur, 0)
        
    #if anywhere else
    else:
        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur, 0, line1, xmax - 1)

        listpos -= 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur - 1, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur - 1, 0)

    return (stdscr, itemlist, listpos)

# - - - - - i t e m u p - - - - -
def itemup(stdscr, itemlist, listpos):
    """Move the current item and cursor up one line.
    """
    #if at top of list, do nothing
    if (0 == listpos):
        return (stdscr, itemlist, listpos)

    ymax, xmax = stdscr.getmaxyx()
    ycur, xcur = stdscr.getyx()

    #swap the current item up one position
    movingitem = itemlist[listpos]
    itemlist[listpos] = itemlist[listpos - 1]
    itemlist[listpos - 1] = movingitem

    #if at top of screen
    if (ycur == 0):
        #clean up the top line and shift all items down one line on the screen
        stdscr.move(1,0)
        stdscr.deleteln()
        stdscr.insertln()
        stdscr.insertln()
        stdscr.move(ymax-1, 0)
        stdscr.deleteln()

        #display itemlist[listpos + 1] as A_NORMAL
        listpos += 1
        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur + 2, 0, line1, xmax - 1)

        #display itemlist[listpos] as A_NORMAL
        listpos -= 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur + 1, 0, line2, xmax - 1)
        
        #display itemlist[listpos - 1] as A_REVERSE
        listpos -= 1
        line3 = '%.4d ' + itemlist[listpos]
        line3 = line3 % listpos
        stdscr.addnstr(ycur, 0, line3, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur, 0)
        
    #if anywhere else
    else:
        #clean up the 2 lines being swapped
        stdscr.move(ycur - 1, 0)
        stdscr.deleteln()
        stdscr.deleteln()
        stdscr.insertln()
        stdscr.insertln()

        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur, 0, line1, xmax - 1)

        listpos -= 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur - 1, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur - 1, 0)

    return (stdscr, itemlist, listpos)

# - - - - - i t e m d o w n - - - - -
def itemdown(stdscr, itemlist, listpos):
    """Move the current item and cursor down one line.
    """
    #if at bottom of list, do nothing
    if (len(itemlist) - 1 == listpos):
        return (stdscr, itemlist, listpos)

    ymax, xmax = stdscr.getmaxyx()
    ycur, xcur = stdscr.getyx()

    #swap the current item up one position
    movingitem = itemlist[listpos]
    itemlist[listpos] = itemlist[listpos + 1]
    itemlist[listpos + 1] = movingitem

    #if at bottom of screen
    if (ycur == ymax - 2):
        #shift all items up one line on the screen
        stdscr.move(0,0)
        stdscr.deleteln() #removes the line at 0,0 and moves all
                          #other lines up one

        #clean up the 2 lines being swapped
        stdscr.move(ycur - 1, 0)
        stdscr.deleteln()
        stdscr.deleteln()
        stdscr.insertln()
        stdscr.insertln()

        #display itemlist[listpos] as A_NORMAL
        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur - 1, 0, line1, xmax - 1)
        
        #display itemlist[listpos + 1] as A_REVERSE
        listpos += 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur, 0)
        
    #if anywhere else
    else:
        #clean up the 2 lines being swapped
        stdscr.move(ycur, 0)
        stdscr.deleteln()
        stdscr.deleteln()
        stdscr.insertln()
        stdscr.insertln()

        line1 = '%.4d ' + itemlist[listpos]
        line1 = line1 % listpos
        stdscr.addnstr(ycur, 0, line1, xmax - 1)

        listpos += 1
        line2 = '%.4d ' + itemlist[listpos]
        line2 = line2 % listpos
        stdscr.addnstr(ycur + 1, 0, line2, xmax - 1, curses.A_REVERSE)
        stdscr.move(ycur + 1, 0)

    return (stdscr, itemlist, listpos)

# - - - - - c u r s e s h a n d l e r - - - - - 
def curseshandler(stdscr, itemlist):
    """do curses crap, and return the reordered list
    """

    #display itemlist and initialise everything
    updateneeded = 0
    stdscr, itemlist, listpos = initialize(stdscr, itemlist)

    #wait for a signal
    while (1):
        c=stdscr.getch()		# Get a keystroke

        #call whatever function is appropriate
        if (c == curses.KEY_DOWN):
            stdscr, itemlist, listpos = curdown(stdscr, itemlist, listpos)
            updateneeded = 1
        elif (c == curses.KEY_UP):
            stdscr, itemlist, listpos = curup(stdscr, itemlist, listpos)
            updateneeded = 1
        elif (c == curses.KEY_LEFT):
            stdscr, itemlist, listpos = itemup(stdscr, itemlist, listpos)
            updateneeded = 1
        elif (c == curses.KEY_RIGHT):
            stdscr, itemlist, listpos = itemdown(stdscr, itemlist, listpos)
            updateneeded = 1
        elif (c == ord('w')):
            return itemlist
        elif (c == ord('q')):
            return None

        #update the screen if necessary
        if (updateneeded == 1):

            #update the screen
            stdscr.refresh()
            updateneeded = 0

# - - - - - m a i n - - - - - 
#Take a input-file and return an output-file

#open files cleanly or error
infile, outfile = openfiles(sys.argv)

#read data from file into a list
itemlist = infile.readlines()

#curses
itemlist = curses.wrapper(curseshandler, itemlist)

#write data to file
if (itemlist != None):
    print "\nWriting list to file."
    outfile.writelines(itemlist)
else:
    print "\nDiscarding changes to list."

#close our files
infile.close()
outfile.close()
