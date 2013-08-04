gender_swap
===========

A tool for swapping genders in LARP materials using simple markup syntax.

-----------------------

The gender_swap utility is a tool for setting gendered text in multiple files so that it remains consistent. It was created to allow writers of Live Action RolePlaying Games (LARPs) change the genders of multiple characters based on who was cast in those roles.

There are currently two ways to use the utility: it can be run purely via the command line or it includes a GUI that can be used. In order to use the GUI you will need to install PyQt4. The pure command line version should run fine whether or not you have PyQt4 on your system.

The utility can currently handle txt and rtf files. It's not particularly smart about how it handles rtf documents, so there are some known bugs in how formatting spanning the gender text markup can be broken up during processing. 

### Setting Up Your Files

In order to gender the text in your files, you'll need to use some very simple markup language. First you must create a gender-list text file that records the genders the characters will be genered to (the actual genders set in this file may change as you use it). 

The project comes with an example gender-list. Your file can be named whatever you want but it must be a .txt file. For each character whose gender can change, you must assign them a unique character number and have a line in your gender-list in the form:

    Character Name:   Number: Female or Male

The number must be an integer. An example line might look like:

    Joe: 02: Male

In other documents that mention Joe you would need to identify text that depends on his gender. For example:

    Joe was an enterprising young man.

For each instance of gendered text, put this markup with the options for male and female versions of the character:

    [Character Number: Female Text / Male Text]

In our example the sentence might become:

    Joe was an enterprising young [02: woman/man].

You can also replace larger chunks of text. The markup can span multiple lines or even paragraphs. If you're using rtf, the markup can't span formatting like bold, so be careful about that. 

The utility also offers the option to gender the file names themselves (especially handy for character sheet files where the character's name changes). The syntax for this is:

    character number.female text.male text.whatever text you like.rtf or txt

So Joe's sheet file name might look like:

    02.Josephine.Joe.Hunter_sheet.txt

When processed with Joe set to Male in the gender list, it would become:

    02.Joe.Hunter_sheet.txt

### Running the Command Line

The command line version of the utility takes the path to the gender-list, the input directory where the files you want to gender are, and the output directory where you want your freshly gendered files. The command is in the format:

    python -m gender_swap swap -g genderList_201310run.txt -i ./character_sheets -o ./201310genderedSheets

The command line has help to describe the various command line options in more detail. 

### Running the GUI

Start the GUI using the command line call:

    python -m gender_swap gui

You must load a gender list and load the files you wish to process in the GUI and set the output directory before clicking the Process button.

### Liscense

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
