#!/usr/bin/env python
"""
This is a set of string constants to support the gender swap tool.

Copyright Eva Schiffer 2014

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

# FUTURE some day all of these sets should be configured from an external file

# constants for possible genders this program understands
FEMALE_GENDER         = "female"
MALE_GENDER           = "male"
NEUTRAL_THEY_GENDER   = "neutral they"
NEUTRAL_ZE_GENDER     = "neutral ze"

# the expected pronoun sets for the genders this program understands
EXPECTED_FEMALE_WORDS = set(["she",  "her",  "hers",            "herself"])
EXPECTED_MALE_WORDS   = set(["he",   "him",  "his",             "himself"])
EXPECTED_N_THEY_WORDS = set(["they", "them", "their", "theirs", "themself"])
EXPECTED_N_ZE_WORDS   = set(["ze", "zhe",
                             "zir", "zem" "hir", "mer", "zhim",
                             "zir", "zes", "hir", "zer", "zher",
                             "zirs", "zes", "hirs", "zers", "zhers",
                             "zirself", "hirself", "zemself", "zhimself"])

# a correlation of classifications to expected pronouns this program understands
POSSIBLE_PRONOUN_SETS = {
                            FEMALE_GENDER       : EXPECTED_FEMALE_WORDS,
                            MALE_GENDER         : EXPECTED_MALE_WORDS,
                            NEUTRAL_THEY_GENDER : EXPECTED_N_THEY_WORDS,
                            NEUTRAL_ZE_GENDER   : EXPECTED_N_ZE_WORDS,
                        }

