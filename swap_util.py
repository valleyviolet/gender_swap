#!/usr/bin/env python
"""
This is a set of utility functions to support the gender swap tool.

Copyright Eva Schiffer 2013

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
import re
import sys

EXPECTED_FEMALE_WORDS = set(["she", "her", "hers", "herself"])
EXPECTED_MALE_WORDS   = set(["he",  "him", "his",  "himself"])

def process_one_file (file_path, output_path, gender_defs,
                      process_file_names=False) :
    """
    It is assumed that the inputs have been validated for
    existance and minimal suitability of type.
    This method can only process .txt and .rtf files.
    There are some known issues with formating tags around the
    syntax in .rtf files, especially where rich formatting
    spans the syntax.
    """
    
    file_name = os.path.basename(file_path)
    
    # open the input sheet
    print ("Opening sheet to set genders: " + file_path)
    input_sheet_file = open(file_path, "r")
    
    # parse the input sheet to set the genders
    input_lines   = input_sheet_file.readlines()
    in_text_temp  = ""
    # build this into one string
    for in_line in input_lines :
        in_text_temp = in_text_temp + in_line
    gendered_text = parse_ungendered_sheet(in_text_temp, gender_defs)
    
    # figure out the path of the new sheet in the output directory
    output_sheet_name = parse_file_name (file_name, gender_defs) if process_file_names else file_name
    out_sheet_path    = os.path.join(output_path, output_sheet_name)
    
    # save the resulting gendered character in the output file
    print ("Saving gendered character sheet to: " + out_sheet_path)
    out_sheet_file    = open(out_sheet_path, "w")
    out_sheet_file.write(gendered_text)
    
    # close the files we've opened since we're done with them
    input_sheet_file.close()
    out_sheet_file.close()
    
    print ("Finished saving and closing new sheet.")

def parse_file_name (fileName, genderDefinitions) :
    """
    given a file name and a set of genderDefinitions (as created
    by parse_genderlist_file), if possible create a gendered
    file name.
    
    File names are expected to be in the form:
    
            ##.female text.male text.whatever text you like.rtf
            (.txt files are also ok)
    
    If the file name doesn't appear to follow the pattern
    (there are too many or too few sections separated by '.',
    there isn't a character number at the beginning that
    corresponds to an entry in the genderDefinitions, etc.)
    then the original fileName will be returned.
    """
    
    print ("Attempting to gender file name: " + fileName)
    nameToReturn = fileName
    
    # break the name into sections delineated by .
    nameSections = fileName.split('.')
    #print("nameSections: " + str(nameSections))
    
    # check to see if the name matches the general pattern we expect
    
    # if the first thing in the name isn't a digit that's one of our character numbers, stop
    charNumber = nameSections[0]
    if not(charNumber.isdigit() and int(charNumber) in genderDefinitions) :
        print ("Unable to gender file name due to missing or invalid character number.")
        return nameToReturn
    
    # if the file extention isn't txt or rtf, stop
    fileExtension = nameSections[-1]
    if not ((fileExtension == "txt") or (fileExtension == "rtf")) :
        print ("Unable to gender file name due to invalid file extension.")
        return nameToReturn
    
    # if we don't have at least 4 sections (character number.female text.male text.file extension), stop
    if len(nameSections) < 4 :
        print ("Unable to gender file name due to formatting inconsistency, " +
               "expected more sections delimited by periods.")
        return nameToReturn
    
    # select the gender specific part of the name
    charNumber = int(charNumber)
    shouldUseFemale = genderDefinitions[charNumber][1]
    nameToReturn = nameSections[0] + '.' + nameSections[1] if shouldUseFemale else nameSections[0] + '.' + nameSections[2]
    
    # add the rest of the file name back onto our gendered section
    for index in range(3, len(nameSections)) :
        nameToReturn = nameToReturn + '.' + nameSections[index]
    
    print ("Successfully gendered file name, resulting in: " + nameToReturn)
    
    return nameToReturn

def parse_genderlist_file (genderData) :
    """
    takes the text lines of a gender list and returns a dictionary in the form:
    
        {
            character number (int):   ["character name", isFemale (bool)],
        }
    """
    
    genderDict = { }
    
    for line in genderData :
        
        [name, number, genderText] = line.split(": ")
        name       = name.strip()
        number     = int(number.strip())
        genderText = genderText.strip().lower()
        isFemale   = (genderText == "female") or (genderText[0] == "f")
        
        # warn if data is being overwritten
        if number in genderDict :
            print ("WARNING: The character number " + str(number)
                   + " is present multiple times in this list of gender data. "
                   + "Only the last entry for this number will be used.")
        
        genderDict[number] = [name, isFemale]
        #print "name:      " + name
        #print "number:    " + str(number)
        #print "is female: " + str(isFemale)
    
    return genderDict

def parse_ungendered_sheet (inputText, genderDefinitions) :
    """
    takes a character sheet in the form of a string and
    a gender definition dictionary (in the form returned from
    parse_genderlist_file) and parses the character sheet to
    specify the genders of all the characters as defined in
    the dictionary.
    
    Returns the gender-specific version of the character sheet
    text as an array of strings (in a form similar to the
    input).
    """
    
    # gendered word markup looks like: [02: her/his]
    genderedWordPattern = r"\[(\d+):\s*([^/]*)/([^\]]*)]"
    
    def cleanup_gender_fn (matchInfo, genderDefs=genderDefinitions, printWarnings=True) :
        """
        this function will be used when calling re.sub to replace
        each match with the appropriate gendered text
        """
        
        toReturn = ""
        
        characterNumber = int(matchInfo.group(1)) #guaranteed to be digits
        if characterNumber in genderDefs.keys() :
            
            shouldUseFemale = genderDefs[characterNumber][1]
            femaleTerm      = matchInfo.group(2).strip()
            maleTerm        = matchInfo.group(3).strip()
            toReturn        = femaleTerm if shouldUseFemale else maleTerm
            
            if printWarnings :
                check_gendered_terms(femaleTerm, maleTerm, matchInfo.group(0))
            
        else :
            
            toReturn = matchInfo.group(0)
            print ("Warning, unable to find character number " + str(characterNumber)
                   + " in character list. The following phrase will not be processed: " + toReturn)
        
        return toReturn
    
    outputText = re.sub(genderedWordPattern, cleanup_gender_fn, inputText, flags=re.DOTALL)
    
    return outputText

def check_gendered_terms (femaleTerm, maleTerm, fullPhraseForPrinting=None) :
    """
    check the gendered terms given and print a warning if they
    would be expected to be gendered terms for the opposite gender
    """
    
    if femaleTerm in EXPECTED_MALE_WORDS :
        message = "WARNING: "
        message = (message + "In the phrase \"" + fullPhraseForPrinting + "\", t") if (fullPhraseForPrinting is not None) else (message + "T")
        message = message +"he term \"" + femaleTerm + "\" was given as a female term but is" + \
               " more commonly considered male. You may wish to check if this is a typo."
        print (message)
    
    if maleTerm in EXPECTED_FEMALE_WORDS :
        message = "WARNING: "
        message = (message + "In the phrase \"" + fullPhraseForPrinting + "\", t") if (fullPhraseForPrinting is not None) else (message + "T")
        message = message +"he term \"" + maleTerm + "\" was given as a male term but is" + \
               " more commonly considered female. You may wish to check if this is a typo."
        print (message)

if __name__ == "__main__":
    main()