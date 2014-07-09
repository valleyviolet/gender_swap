#!/usr/bin/env python
"""
This module includes gui code for presenting the gender swap utility.

Copyright Eva Schiffer 2013 - 2014

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

from PyQt4 import QtGui, QtCore

from gender_swap_gui_model import GenderSwapGUIModel
from constants             import *

ARE_GENDERS_EDITABLE_IN_GUI = False

class GenderedGUI (QtGui.QWidget) :
    """
    this class represents the overall gui
    """
    
    def __init__ (self) :
        """
        set up the basic shape of our gui
        and fill it with the appropriate widgets
        """
        
        super(GenderedGUI, self).__init__()
        
        tabs        = QtGui.QTabWidget()
        
        temp_widget = QtGui.QWidget()
        temp_layout = self.buildDefinitionsTabLayout()
        temp_widget.setLayout(temp_layout)
        tabs.addTab(temp_widget, "Gender Definitions")
        
        temp_widget = QtGui.QWidget()
        temp_layout = self.buildFilesTabLayout()
        temp_widget.setLayout(temp_layout)
        tabs.addTab(temp_widget, "Files and Processing")
        
        # finish building the window and show it
        temp_layout = QtGui.QGridLayout()
        temp_layout.addWidget(tabs)
        self.setLayout(temp_layout)
        
        self.resize(500, 500)
        self.setWindowTitle('Gender Swap GUI')
        self.setWindowIcon(QtGui.QIcon('./art_assets/changeIcon.png'))  
        self.show()
        
        # TODO, this is a bad leaky strategy, fix it later
        #self.windows = [ ]
    
    def buildDefinitionsTabLayout (self) :
        """
        create the needed sub-widgets for the
        gender definitions tab and lay them out
        
        creates the following self held widgets
        
        self.genderListFilePathDisplay
        self.loadGenderListButton
        self.genderListDisplayTable
        """
        
        layout = QtGui.QGridLayout()
        rowNum = 1
        
        # note: addWidget has parameters in the form:
        # (widget_to_add, row_index, col_index, row_span, col_span)
        # if the spans are omitted they default to 1
        
        self.genderListFilePathDisplay = QtGui.QLineEdit()
        self.genderListFilePathDisplay.setEnabled(False)
        layout.addWidget(self.genderListFilePathDisplay, rowNum, 0, 1, 4)
        self.loadGenderListButton = QtGui.QPushButton("Load Gender List")
        self.loadGenderListButton.clicked.connect(self.loadGenderList)
        layout.addWidget(self.loadGenderListButton, rowNum, 4)
        rowNum += 1
        
        #layout.addWidget(QtGui.QLabel('Character Gender Table'), rowNum, 0)
        #rowNum += 1
        
        self.genderListDisplayTable = QtGui.QTableWidget(0, 3)
        self.genderListDisplayTable.setHorizontalHeaderLabels(QtCore.QStringList(["Name", "Number", "Gender"]))
        self.genderListDisplayTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.genderListDisplayTable.verticalHeader().hide()
        layout.addWidget(self.genderListDisplayTable, rowNum, 0, 8, 5)
        rowNum += 1
        
        return layout
    
    def buildFilesTabLayout (self) :
        """
        create the needed sub-widgets for the
        files and processing tab and lay them out
        
        creates the following self held widgets
        
        self.outputFilePathDisplay
        self.selectOutputButton
        self.searchDirsToggle
        self.loadFilesButton
        self.clearFilesButton
        self.filesToProcessDisplay
        self.processNamesToggle
        self.processButton
        """
        
        layout = QtGui.QGridLayout()
        rowNum = 1
        
        # note: addWidget has parameters in the form:
        # (widget_to_add, row_index, col_index, row_span, col_span)
        # if the spans are omitted they default to 1
        
        layout.addWidget(QtGui.QLabel('Output to: '), rowNum, 0)
        self.outputFilePathDisplay = QtGui.QLineEdit()
        self.outputFilePathDisplay.setEnabled(False)
        layout.addWidget(self.outputFilePathDisplay, rowNum, 1, 1, 2)
        self.selectOutputButton = QtGui.QPushButton("Select")
        self.selectOutputButton.clicked.connect(self.selectOutputDir)
        layout.addWidget(self.selectOutputButton, rowNum, 3)
        rowNum += 1
        
        self.searchDirsToggle = QtGui.QCheckBox("load from directory")
        layout.addWidget(self.searchDirsToggle, rowNum, 0, 1, 3)
        self.loadFilesButton = QtGui.QPushButton("Load Files")
        self.loadFilesButton.clicked.connect(self.load_files_to_process)
        layout.addWidget(self.loadFilesButton, rowNum, 2)
        self.clearFilesButton = QtGui.QPushButton("Clear")
        self.clearFilesButton.clicked.connect(self.clear_pressed)
        layout.addWidget(self.clearFilesButton, rowNum, 3)
        rowNum += 1
        
        #self.filesToProcessDisplay = QtGui.QListWidget()
        self.filesToProcessDisplay = FilesList()
        layout.addWidget(self.filesToProcessDisplay, rowNum, 0, 5, 4)
        rowNum += 5
        
        self.processNamesToggle = QtGui.QCheckBox(" also process file names to gender them")
        layout.addWidget(self.processNamesToggle, rowNum, 0, 1, 4)
        self.processNamesToggle.clicked.connect(self.process_names_toggled)
        rowNum += 1
        
        """
        self.previewButton = QtGui.QPushButton("Preview Sheet")
        self.previewButton.clicked.connect(self.preview_pressed)
        layout.addWidget(self.previewButton, rowNum, 0, 1, 2)
        """
        
        self.processButton = QtGui.QPushButton("Process")
        self.processButton.clicked.connect(self.process_pressed)
        layout.addWidget(self.processButton, rowNum, 2, 1, 2)
        
        return layout
    
    def setModel (self, modelObject) :
        """
        once the gui has been created the model should be set
        """
        
        self.model = modelObject
        self.filesToProcessDisplay.set_file_handling_method(self.model.add_more_files_to_process)
        self.model.send_updated_information()
    
    def loadGenderList (self) :
        """
        the user clicked the button to load a gender list
        """
        
        filePath = QtGui.QFileDialog.getOpenFileName(self, 'Open gender list file', './')
        
        print ("User selected file path: " + str(filePath))
        
        self.model.set_new_gender_list(filePath)
    
    def selectOutputDir (self) :
        """
        the user clicked the button to select an output directory
        """
        
        outputPath = QtGui.QFileDialog.getExistingDirectory(self, 'Output file directory', './')
        
        print ("User selected file path: " + str(outputPath))
        
        self.model.set_new_output_path(outputPath)
    
    def load_files_to_process (self) :
        """
        the user clicked the button to load files for processing
        """
        
        # if the box is checked we're looking for a directory
        toProcessList = None
        if self.searchDirsToggle.isChecked() :
            
            dirPath = QtGui.QFileDialog.getExistingDirectory(self, 'Directory to Search', './')
            
            print ("User selected directory at path: " + str(dirPath))
            
            toProcessList = [dirPath]
            
        # otherwise we want to load individual files
        else :
            
            filePaths = QtGui.QFileDialog.getOpenFileNames(self, 'Files to Process', './')
            
            print ("User selected file paths: " + str(filePaths))
            
            toProcessList = filePaths
        
        # if the user selected anything, tell the model about it
        if toProcessList is not None :
            self.model.add_more_files_to_process (toProcessList)
    
    def clear_pressed (self) :
        """
        the user pressed the button to clear the list of files for processing
        """
        
        print ("User pressed clear button.")
        
        self.model.clear_files_to_process()
    
    def preview_pressed (self) :
        """
        the user pressed the button to preview one of the files
        """
        
        """
        print ("User pressed preview button.")
        
        # get the currently selected file
        file_text = str(self.filesToProcessDisplay.currentItem().text()) if self.filesToProcessDisplay.currentItem() is not None else None
        
        # get the gendered version of the file's contents for the preview
        gendered_text = self.model.preview_file(file_text)
        
        print ("successfully gendered preview text")
        
        temp_window = QtGui.QWidget()
        temp_layout = QtGui.QGridLayout()
        
        temp_text_edit = QtGui.QLabel()
        temp_text_edit.textFormat = QtCore.Qt.RichText
        temp_text_edit.setText(gendered_text)
        
        temp_layout.addWidget(temp_text_edit, 0, 0)
        temp_window.setLayout(temp_layout)
        
        temp_window.resize(500, 500)
        temp_window.setWindowTitle('Preview of: ' + file_text)
        temp_window.show()
        
        self.windows.append(temp_window)
        """
    
    def process_pressed (self) :
        """
        the user pressed the button to process the files
        """
        
        print ("User pressed process button.")
        
        self.model.process_files()
    
    def process_names_toggled (self) :
        """
        the user toggled whether or not they want to gender file names
        """
        
        print ("User toggled process file names to gender them check box.")
        
        value = self.processNamesToggle.checkState() == QtCore.Qt.Checked
        
        self.model.change_other_settings (do_process_names=value)
    
    def recieveUpdate (self,
                       genderListFilePath=None,
                       genderDefinitions=None,
                       genderOrdering=None,
                       outputPath=None,
                       searchDirectories=None,
                       filesToProcessList=None,
                       doProcessFileNames=None) :
        """
        update the gui with information sent from the model
        
        information that is left as None will not be set
        
        genderDefinitions is expected to be a dictionary in the form
        {
            character number (int):   ["character name", pronoun_set_constant],
        }
        """
        
        # if we got a new path for the gender list document, update that
        if genderListFilePath is not None :
            print ("Updating gender list file path: " + str(genderListFilePath))
            
            self.genderListFilePathDisplay.setText(genderListFilePath)
        
        # if we got new gender definitions, update those
        if genderDefinitions is not None :
            print ("Updating gender definitions list: " + str(genderDefinitions))
            
            # this seems like a silly way to empty the table,
            # but I'm not easily finding a better one
            while self.genderListDisplayTable.rowCount() > 0 :
                self.genderListDisplayTable.removeRow(0)
            
            # for each of the characters in the definitions, add a line to the table
            for charNum in sorted(genderDefinitions.keys(), reverse=True) :
                
                # for the moment this is a meta testing setting
                if ARE_GENDERS_EDITABLE_IN_GUI :
                    self.genderListDisplayTable.insertRow(0)
                    
                    tempWidget = QtGui.QLineEdit()
                    tempWidget.setText( genderDefinitions[charNum][0] )
                    self.genderListDisplayTable.setCellWidget(0,0, tempWidget)
                    
                    tempWidget = QtGui.QLineEdit()
                    tempWidget.setText( str(charNum) )
                    # TODO, this must be an integer, add a formatter of some sort to enforce that
                    self.genderListDisplayTable.setCellWidget(0,1, tempWidget)
                    
                    tempWidget = QtGui.QComboBox()
                    tempWidget.addItems(sorted(genderOrdering[charNum].values()))
                    tempIndex = tempWidget.findText(genderDefinitions[charNum][1])
                    tempWidget.setCurrentIndex(tempIndex)
                    self.genderListDisplayTable.setCellWidget(0,2, tempWidget)
                    
                    # TODO, this isn't set up to respond correctly to editing
                    
                else : 
                    
                    self.genderListDisplayTable.insertRow(0)
                    
                    tempWidget = QtGui.QTableWidgetItem( genderDefinitions[charNum][0] )
                    tempWidget.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.genderListDisplayTable.setItem(0,0, tempWidget)
                    
                    tempWidget = QtGui.QTableWidgetItem( str(charNum) )
                    tempWidget.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.genderListDisplayTable.setItem(0,1, tempWidget)
                    
                    tempWidget = QtGui.QTableWidgetItem( genderDefinitions[charNum][1] )
                    tempWidget.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.genderListDisplayTable.setItem(0,2, tempWidget)
                
        
        # if we got a new output path update that
        if outputPath is not None :
            print ("Updating output path: " + str(outputPath))
            
            self.outputFilePathDisplay.setText(outputPath)
        
        # if we got a new setting for whether or not to search directories, update that
        if searchDirectories is not None :
            print ("Updating search directories check box: " + str(searchDirectories))
            
            self.searchDirsToggle.setCheckState(searchDirectories)
        
        # if we got a new list of files to process, update that
        if filesToProcessList is not None :
            print ("Updating list of files to process: " + str(filesToProcessList))
            
            self.filesToProcessDisplay.clear()
            
            self.filesToProcessDisplay.addItems(filesToProcessList)
        
        # if we got a new setting for whether or not to process file names, update that
        if doProcessFileNames is not None :
            print ("Updating process file names checkbox: " + str(doProcessFileNames))
            
            toSet = QtCore.Qt.Checked if doProcessFileNames else QtCore.Qt.Unchecked
            self.processNamesToggle.setCheckState(toSet)

# this class exists to make sure the list of files to process
# accepts drag and drop input
class FilesList (QtGui.QListWidget) :
    """
    This is a list of files that will accept drag and droped files.
    """
    
    def __init__(self, method_for_file_handling=None, parent=None):
        
        super(QtGui.QListWidget, self).__init__(parent)
        
        self.setAcceptDrops(True)
        self.file_handling_method = method_for_file_handling
    
    def set_file_handling_method (self, method_for_file_handling) :
        
        self.file_handling_method = method_for_file_handling
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            
            files = [ ]
            for url in event.mimeData().urls():
                files.append(str(url.toLocalFile()))
            self.file_handling_method(files)
            
            self.emit(QtCore.SIGNAL("dropped"))
        else:
            event.ignore()

def temp_run_ui ( ) :
    
    tempApp   = QtGui.QApplication(sys.argv)
    tempGui   = GenderedGUI()
    tempModel = GenderSwapGUIModel(tempGui)
    tempGui.setModel(tempModel)
    
    sys.exit(tempApp.exec_())


def main () :
    return 0

if __name__ == "__main__":
    main()