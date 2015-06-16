#!/usr/bin/env python
"""
This module includes the model behind the gender swap's gui code.

Copyright Eva Schiffer 2013 - 2015

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

import sys
import os

import swap_util
from constants import *

class GenderSwapGUIModel :
    """
    This class holds information shown in the gui.
    """
    
    def __init__ ( self, associate_gui_view ) :
        """
        setup the initial state of the data with nothing loaded
        """
        
        self.gui_for_updates = associate_gui_view
        
        self.loaded_list_path      = None
        self.gender_defs           = None
        self.gender_orders         = None
        self.were_genders_edited   = False
        
        self.output_path           = None
        self.files_to_process_list = set( )
        self.do_process_file_names = False
    
    def send_updated_information (self) :
        """
        pass information from the model to the view
        """
        
        print("Sending updates from model.")
        
        self.gui_for_updates.recieveUpdate ( genderListFilePath=self.loaded_list_path,
                                             genderDefinitions=self.gender_defs,
                                             genderOrdering=self.gender_orders,
                                             outputPath=self.output_path,
                                             filesToProcessList=list(self.files_to_process_list),
                                             doProcessFileNames=self.do_process_file_names)
    
    def set_new_gender_list (self, file_path) :
        """
        a new gender list file has been selected; load that list
        and send an appropriate update to the UI
        """
        
        # if we have a valid file path with a non-directory at the end of it
        if ( (file_path is not None)     and (file_path != '') and
             (os.path.exists(file_path)) and (not os.path.isdir(file_path)) ) :
            
            # open the file and set our internal gender data accordingly
            genderFile = open(file_path, 'r')
            self.loaded_list_path = file_path
            self.gender_defs, self.gender_orders = swap_util.parse_genderlist_file(genderFile.readlines())
            
            # let the view know that the gender information changed
            self.gui_for_updates.recieveUpdate ( genderListFilePath=self.loaded_list_path,
                                                 genderDefinitions=self.gender_defs,
                                                 genderOrdering=self.gender_orders,)
            
        else :
            print ("Unable to open file path: " + str(file_path))
    
    def change_other_settings (self, do_process_names=None) :
        """
        given the new settings values, change them and update the view
        
        FUTURE, if there's more settings that are added later, add them here
        """
        
        did_change_something = False
        
        if do_process_names is not None :
            self.do_process_file_names = do_process_names
            did_change_something       = True
        
        # if we changed anything, let the gui know
        if did_change_something :
            self.send_updated_information()
    
    def set_new_output_path (self, new_output_path) :
        """
        a new output path has been selected; hang onto that
        for later
        """
        
        # if we got an output path and it's minimally acceptable
        if ( (new_output_path is not None)     and (new_output_path != '') and
             (os.path.exists(new_output_path)) and (os.path.isdir(new_output_path)) ) :
            
            self.output_path = new_output_path
            
            self.gui_for_updates.recieveUpdate ( outputPath=self.output_path, )
            
        else :
            print ("Path is not suitable for output: " + str(new_output_path))
    
    def add_more_files_to_process (self, list_of_file_paths) :
        """
        given more file paths, add them to the list
        """
        
        if self.files_to_process_list is None :
            self.files_to_process_list = set( )
        
        # first deal with any directories in the list
        clean_paths = set( )
        for file_path in list_of_file_paths :
            file_path = str(file_path)
            
            # if we found a directory, explode it
            if os.path.isdir(file_path) :
                
                more_files = os.listdir(file_path)
                for deeper_file in more_files :
                    deeper_file = os.path.join(file_path, deeper_file)
                    if not os.path.isdir(deeper_file) :
                        clean_paths.update([deeper_file])
                
                print ("Searching directory for additional files: " + str(file_path))
            else :
                clean_paths.update([file_path])
        
        # now check to see if the paths are actually acceptable
        for file_path in clean_paths :
            
            print ("Checking path for inclusion in processing: " + str(file_path))
            
            # look at the file extension to see if it's one we can process
            _, file_type = os.path.splitext(file_path)
            if (file_type in POSSIBLE_FILE_TYPES) :
                self.files_to_process_list.update([file_path])
                
                print ("Path is of an acceptable type. Adding to it to processing list.")
                
            else :
                
                print ("File is not a type this program understands. Ignoring file.")
        
        self.gui_for_updates.recieveUpdate ( filesToProcessList=list(self.files_to_process_list))
    
    def clear_files_to_process (self) :
        """
        clear the current list of files for processing
        """
        
        self.files_to_process_list = set( )
        
        self.gui_for_updates.recieveUpdate ( filesToProcessList=list(self.files_to_process_list))
    
    def preview_file (self, file_path) :
        """
        Create a preview version of the file using the current gender definitions.
        """
        
        # check the minimum prerequisites for file processing
        if self.check_processing_prereqs() is None:
            return
        
        """ TODO I have no idea why this comparison doesn't work
        # check that we have a selected file
        found = False
        for temp_path in list(self.files_to_process_list) :
            print (str(str(found) == str(temp_path)))
            if str(found) == str(temp_path) :
                found = True
        if not found :
            print ("Unrecognized file path given for preview: " + str(file_path))
            return
        """
        
        # at this point we've minimally validated that we can process the file
        return swap_util.open_and_gender_sheet (file_path, 
                                                self.gender_defs,
                                                self.gender_orders,
                                                reason=" to create gendered preview")
    
    def process_files (self) :
        """
        if possible given the current state of the model, process the files
        and save the resulting outputs to disk
        
        in order to process files:
        
            there must be at least one file in the list for processing
            a gender list must be loaded
            an output directory must be set
                the output directory must not be the same as the directory that
                holds any of the files in the list for processing
        
        FUTURE, this method handles errors with printing, move to throwing
        an exception for the gui to handle.
        """
        
        # check the minimum prerequisites for file processing
        if self.check_processing_prereqs() is None:
            return
        
        # check that we have files to process
        if len(self.files_to_process_list) <= 0 :
            print ("No files to process.")
            return
        
        # check if we have an output directory set at all
        if self.output_path is None :
            print ("No output directory is selected.")
            return
        
        # check if the output directory contains any of the input files
        # if so, we don't want to process them!
        for file_path in list(self.files_to_process_list) :
            file_directory = os.path.dirname(file_path)
            if os.path.samefile(self.output_path, file_directory) :
                print ("Unable to output to directory containing input files.")
                return
        
        # at this point we've minimally validated that we can process the files
        for file_path in list(self.files_to_process_list) :
            
            swap_util.process_one_file(file_path,
                                       str(self.output_path),
                                       self.gender_defs,
                                       self.gender_orders,
                                       process_file_names=self.do_process_file_names)
    
    def check_processing_prereqs (self) :
        """
        Check that we have the minimum information needed to process files.
        
        FUTURE, this method handles errors with printing and returning None, move to throwing
        an exception for the gui to handle.
        """
        
        # check if we have gender defintions loaded
        if (self.gender_defs is None) or (len(self.gender_defs.keys()) <= 0) :
            print ("No gender definitions are loaded.")
            return None
        
        # check if we have gender orderings loaded
        if (self.gender_orders is None) or (len(self.gender_orders.keys()) <= 0) :
            print ("No gender orderings are loaded.")
            return None
        
        return 1



def main () :
    return 0

if __name__ == "__main__":
    main()