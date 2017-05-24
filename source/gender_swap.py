#!/usr/bin/env python
"""
The purpose of this program is to gender swap LARP character sheets.
The sheets are expected to be in .txt or .rtf formats and a gendersList.txt
file defining the genders to select is expected.

Copyright Eva Schiffer 2012 - 2015

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

from optparse import OptionParser

import swap_util

def main () :
    usage = """
%prog [options] 
run "%prog help" to list commands
examples:

python -m gender_swap swap -g genderList_201310run.txt -i ./character_sheets -o ./201310genderedSheets
python -m gender_swap gui

"""
    
    parser = OptionParser()
    
    parser.add_option("-g", "--genderList", dest="genderList",
                      help="the file that should be used to determine what genders to swap in")
    parser.add_option("-i", "--inDir", default="./",
                      dest="inputDirectory", 
                      help="the directory to get the input character sheets from")
    parser.add_option("-o", "--outDir", default="./out",
                      dest="outDirectory", 
                      help="the directory where the revised character sheets will be placed")
    parser.add_option('-p', '--processFileName', dest='processName',
                      action="store_true", default=False, help="process the file name to gender it")
    parser.add_option('-v', '--version', dest='version',
                      action="store_true", default=False, help="view the program version")
    
    (options, args) = parser.parse_args()
    
    # display the version
    if options.version :
        print ("gender_swap, version 0.6 \n") # because having a version history is cool

    # set up the commands dictionary
    commands = {}
    prior = None
    prior = dict(locals())
    
    
    def swap ( ) :
        """swap in specific genders for a set of documents
        
        given information in the form of commandline options:
        
            1. load a gender list document that will define the genders
               of the characters for this run
            2. load the files in the input directory and process genders
               in any sheets that have file types we know how to process
            3. save the resulting gendered documents to the output directory
        """
        
        # make sure we aren't going to overwrite our input files
        if options.outDirectory == options.inputDirectory :
            print ("Input and output directories cannot be the same. "
                   + "Please select a different output directory to avoid "
                   + "destroying your original sheets.")
            return 1
        
        # make sure we have a gender list to work with
        if options.genderList is None :
            print ("Unable to process files without a gender list document "
                   + "defining the character's genders.")
            return 1
        
        print ("Opening and parsing gender list: " + options.genderList)
        genderListFile = open(options.genderList, "r")
        genderDefinitions, genderOrdering = swap_util.parse_genderlist_file(genderListFile.readlines())
        genderListFile.close()
        
        # create the output directory if needed
        if not os.path.exists(options.outDirectory):
            print "Making output directory: " + options.outDirectory
            os.makedirs(options.outDirectory)
        
        # get a list of files in the input directory
        print ("Examining all input character sheets in: " + options.inputDirectory)
        possibleSheets = os.listdir(options.inputDirectory)
        
        # for each file in the input directory...
        for possibleSheet in possibleSheets :
            
            processThisSheet = False
            
            # check to see if it looks like the kind of sheet we're expecting
            print ("----------------------------------")
            print ("Examining file: " + possibleSheet)
            number      = possibleSheet.split('.')[0]
            _, fileType = os.path.splitext(possibleSheet)
            
            # if this really is a number and it represents a character that's
            # in the gender definitions we were given, the name looks good so far
            if number.isdigit() and int(number) in genderDefinitions :
                processThisSheet = True
            # double check that this is a type of file we can process
            processThisSheet = (processThisSheet and
                                (fileType == ".txt" or fileType == ".rtf"))
            #print "fileType: " + fileType
            
            if processThisSheet :
                
                #process_one_file (file_path, output_path, gender_defs, process_file_names=False)
                swap_util.process_one_file(os.path.join(options.inputDirectory, possibleSheet),
                                           options.outDirectory,
                                           genderDefinitions,
                                           genderOrdering,
                                           process_file_names=options.processName)
                
            else :
                print ("File " + possibleSheet
                       + " does not match character sheet name patterns. "
                       + "This file will not be processed.")
        
        return 0
    
    def gui ( ) :
        """a gui to handle gender swapping in a pretty UI
        this commandline option starts up a gui that allows a user
        to swap genders in a set of sheets based on gender definitions;
        this is similar to how the swap() method works but is more
        flexible and (hopefully) intuitive for a user
        """
        
        import gender_swap_gui_view
        
        gender_swap_gui_view.temp_run_ui()
    
    def help(command=None):
        """print help for a specific command or list of commands
        e.g. help swap
        """
        if command is None: 
            # print first line of docstring
            for cmd in commands:
                ds = commands[cmd].__doc__.split('\n')[0]
                print "%-16s %s" % (cmd,ds)
        else:
            print commands[command].__doc__
    
    # all the local public functions are included, collect them up
    commands.update(dict(x for x in locals().items() if x[0] not in prior))    
    
    # if what the user asked for is not one of our existing functions, print the help
    if (not args) or (args[0] not in commands):
        if not options.version :
            #gui() # TEMP I don't like hardcoding this for application making
            parser.print_help()
            help()
            return 1
    else:
        # call the function the user named, given the arguments from the command line  
        locals()[args[0]](*args[1:])

    return 0

if __name__ == "__main__":
    main()