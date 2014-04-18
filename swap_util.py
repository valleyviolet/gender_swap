#!/usr/bin/env python
"""
This is a set of utility functions to support the gender swap tool.

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

import os
import re
import sys

from constants import *

def process_one_file (file_path, output_path,
                      gender_defs, gender_ordering,
                      process_file_names=False) :
    """
    It is assumed that the inputs have been validated for
    existance and minimal suitability of type.
    
    This method can only process .txt and .rtf files.
    There are some known issues with formating tags around the
    syntax in .rtf files, especially where rich text formatting
    spans the syntax.
    """
    
    file_name = os.path.basename(file_path)
    
    # open the input sheet
    print ("Opening sheet to set genders: " + file_path)
    input_sheet_file = open(file_path, "r")
    
    # parse the rest of the input sheet to set the genders
    input_lines   = input_sheet_file.readlines()
    in_text_temp  = ""
    # build this into one string
    for in_line in input_lines :
        in_text_temp = in_text_temp + in_line
    gendered_text = parse_ungendered_sheet(in_text_temp, gender_defs, gender_ordering)
    
    # figure out the path of the new sheet in the output directory
    output_sheet_name = parse_file_name (file_name, gender_defs, gender_ordering) if process_file_names else file_name
    out_sheet_path    = os.path.join(output_path, output_sheet_name)
    
    # save the resulting gendered character in the output file
    print ("Saving gendered character sheet to: " + out_sheet_path)
    out_sheet_file    = open(out_sheet_path, "w")
    out_sheet_file.write(gendered_text)
    
    # close the files we've opened since we're done with them
    input_sheet_file.close()
    out_sheet_file.close()
    
    print ("Finished saving and closing new sheet.")

def parse_file_name (fileName, genderDefinitions, genderOrdering) :
    """
    given a file name and a set of genderDefinitions (as created
    by parse_genderlist_file), if possible create a gendered
    file name.
    
    File names are expected to be in the form:
    
            ##.gendered text a.gendered text b.whatever text you like.rtf
            (.txt files are also ok)
    
    Where the number of gendered text entries is the same as the possible
    genders listed in the first line of the sheet and they are arranged
    in the same order.
    
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
    
    # check to see if the name matches the general pattern we expect
    
    # if the first thing in the name isn't a digit that's one of our character numbers, stop
    charNumber = nameSections[0]
    if not(charNumber.isdigit() and int(charNumber) in genderDefinitions) :
        print ("Unable to gender file name due to missing or invalid character number.")
        return nameToReturn
    charNumber = int(charNumber)
    
    # now pull the ordering information for this character
    tempOrdering = genderOrdering[charNumber]
    
    # if the file extention isn't txt or rtf, stop
    fileExtension = nameSections[-1]
    if not ((fileExtension == "txt") or (fileExtension == "rtf")) :
        print ("Unable to gender file name due to invalid file extension.")
        return nameToReturn
    
    # check how many gendered sections we're expecting
    numGenderOptions = len(tempOrdering.keys())
    
    # if we don't have at least (the number expected genders + 2) sections (character number.<gendered sections>.file extension), stop
    if len(nameSections) < (numGenderOptions + 2) :
        print ("Unable to gender file name due to formatting inconsistency, " +
               "expected more sections delimited by periods.")
        return nameToReturn
    
    # select the gender specific part of the name
    genderIndex  = get_gender_index(genderDefinitions[charNumber], tempOrdering)
    nameToReturn = nameSections[0] + "." + nameSections[genderIndex + 1]
    
    # add the rest of the file name back onto our gendered section
    for index in range(numGenderOptions + 1, len(nameSections)) :
        nameToReturn = nameToReturn + '.' + nameSections[index]
    
    print ("Successfully gendered file name, resulting in: " + nameToReturn)
    
    return nameToReturn

def get_gender_index (genderDefinition, genderOrdering) :
    """
    given a gender definition for the character and the gender ordering
    for the character determine the appropriate index to use for that gender
    """
    
    found       = False
    genderToUse = genderDefinition[1]
    indexToUse  = -1
    
    for index in sorted(genderOrdering.keys()) :
        if genderOrdering[index] == genderToUse :
            indexToUse = index
            found      = True
    
    if indexToUse < 0 :
        print("WARNING: Unable to find selected gender for character " + genderDefinition[0]
              + " in list of possible genders for this character.")
    
    return indexToUse

def parse_genderlist_file (genderData) :
    """
    takes the text lines of a gender list and returns a dictionary in the form:
    
        {
            character number (int):   ["character name", pronoun_set_constant],
        }
    
    FUTURE: When the pronoun sets are externally configurable detecting which
    gender was selected will need to be handled differently.
    """
    
    genderDict  = { }
    genderOrder = { }
    
    # parse the information for each line since the file should be one char per line
    for line in genderData :
        
        # split the line and handle the easy stuff
        [name, number, gendersList, genderText] = line.split(":")
        name        = name.strip()
        number      = int(number.strip())
        
        # parse the list of possible genders for this characer into useful ordering info
        gendersList   = gendersList.split('/')
        temp_ordering = { }
        for index in range(len(gendersList)) :
            temp_ordering[index] = gendersList[index].strip() # strip off whitespace
            # check to see if this is a set we know about
            temp_found = False
            for gender_key in POSSIBLE_PRONOUN_SETS.keys() :
                if temp_ordering[index] == gender_key :
                    temp_found = True
            if temp_found is False :
                print("Unable to find defined gender (" + temp_ordering[index]
                      + ") in list of genders understood by this program: " + str(POSSIBLE_PRONOUN_SETS.keys()))
                print("Sheet processing may be incomplete or yield unexpected results.")
        # add this characters ordering info to our overall ordering info
        genderOrder[number] = temp_ordering
        
        # figure out the gender selected for this character
        genderText  = genderText.strip().lower()
        genderConst = None
        genderConst = FEMALE_GENDER       if (genderText == "female") or (genderText[0] == "f") else genderConst
        genderConst = MALE_GENDER         if (genderText == "male")   or (genderText[0] == "m") else genderConst
        genderConst = NEUTRAL_THEY_GENDER if genderText.find("they") >= 0                       else genderConst
        genderConst = NEUTRAL_ZE_GENDER   if genderText.find("ze")   >= 0                       else genderConst
        if genderConst is None :
            print "Unable to parse selected gender for character as a gender understood by this program."
        
        # warn if data is being overwritten
        if number in genderDict :
            print ("WARNING: The character number " + str(number)
                   + " is present multiple times in this list of gender data. "
                   + "Only the last entry for this number will be used.")
        
        # set the gender information for this character in our dictionary
        genderDict[number] = [name, genderConst]
    
    return genderDict, genderOrder

def parse_ungendered_sheet (inputText, genderDefinitions, genderOrdering) :
    """
    takes a character sheet in the form of a string,
    a gender definition dictionary, and a gender ordering for this character
    (the last two are in the form returned from parse_genderlist_file)
    
    then parses the character sheet to specify the genders of all the
    characters as defined in the dictionary.
    
    Returns the gender-specific version of the character sheet
    text as an array of strings (in a form similar to the
    input).
    """
    
    # gendered word markup looks like: [02: her/his]
    #genderedWordPattern = r"\[(\d+):\s*([^/]*)/([^\]]*)]"
    genderedWordPattern = r"\[(\d+):\s*([^\]]*)]"
    
    def cleanup_gender_fn (matchInfo,
                           genderDefs=genderDefinitions,
                           genderOrder=genderOrdering,
                           printWarnings=True) :
        """
        this function will be used when calling re.sub to replace
        each match with the appropriate gendered text
        """
        
        toReturn           = ""
        characterNumber    = int(matchInfo.group(1)) #guaranteed to be digits
        genderedOptions    = matchInfo.group(2).split('/')
        
        # if there's a "[" in the gendered text, something's gone wrong
        if printWarnings and (matchInfo.group(2).find("[") >= 0) :
            print("Unexpected [ character found inside phrase: " + matchInfo.group(0))
            print("This may indicate a serious mark up text formatting error.")
        
        if characterNumber in genderDefs.keys() :
            
            # check if we have the number of genered text options we expect
            # based on the genders this character could be
            expectedNumOptions = genderOrder[characterNumber].keys()
            if (len(genderedOptions) != len(expectedNumOptions)) and printWarnings :
                print("The gendered phrase (" + matchInfo.group(0) + ") does not have the expected "
                      + "number of possible gender options for this character (" + str(len(expectedNumOptions)) + ").")
                print("Parsing for this phrase may not be accurate.")
            
            # get the index we want based on the character's gender
            tempIndex = get_gender_index (genderDefs[characterNumber], genderOrder[characterNumber])
            
            # pull the gendered term
            toReturn = genderedOptions[tempIndex].strip()
            
            # if we're printing warnings, check the appropriateness of the various terms
            if printWarnings :
                
                for index in range(len(genderedOptions)) :
                    term = genderedOptions[index].strip()
                    if index in genderOrder[characterNumber].keys() :
                        expectedGender = genderOrder[characterNumber][index].strip()
                        check_gendered_term (term, expectedGender, matchInfo.group(0))
            
        else :
            
            toReturn = matchInfo.group(0)
            if printWarnings :
                print ("Warning, unable to find character number " + str(characterNumber)
                       + " in character list. The following phrase will not be processed: " + toReturn)
        
        return toReturn
    
    outputText = re.sub(genderedWordPattern, cleanup_gender_fn, inputText, flags=re.DOTALL)
    
    return outputText

def check_gendered_term (term, expectedGender, fullPhraseForPrinting=None) :
    """
    check the gendered term given and print a warning
    if it does not match the expected gender
    """
    
    for gender_key in sorted(POSSIBLE_PRONOUN_SETS.keys()) :
        
        if (gender_key != expectedGender) and (term in POSSIBLE_PRONOUN_SETS[gender_key]) :
            
            message = "WARNING: "
            message = (message + "In the phrase \"" + fullPhraseForPrinting + "\", t") if (fullPhraseForPrinting is not None) else (message + "T")
            message = (message +"he term \"" + term + "\" was given as a " + expectedGender + " term but is" + 
                       " more commonly considered " + gender_key + ". You may wish to check if this is a typo.")
            print (message)

if __name__ == "__main__":
    main()