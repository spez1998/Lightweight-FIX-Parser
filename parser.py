# Liquidnet Lightweight FIX Parser
# Written by Sujit Malde July 2019 
# Free to use under GNU GPL 3.0

# !!!!!!!!! READ ME !!!!!!!!!
# This tool takes a FIX message as input (either via manual input to CLI or via piped command) and outputs a readable, verbose version.
# Terminology used is defined as follows. For a FIX message in the format:
# X=Y(D)X=Y(D)X=Y(D)...
# X = field, Y = value, (D) = delimiter (commonly ASCI code 0x01, could also be | or space)

import xml.etree.ElementTree as ET # XML parsing library
import argparse
import re # String manipulation library
from datetime import datetime
import sys

def flags():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", help="display translated FIX in rows and columns", action="store_true")
    parser.add_argument("-v", "--verbose", help="dispaly verbose FIX fields and values", action="store_true")
    parser.parse_args()

def spec_loader(spec_block):
    try:    
        fix_spec_raw = [spec_block[1],spec_block[2]]
        fix_spec_file_num = ''.join(fix_spec_raw)
        print('FIX Specification',spec_block[1],".",spec_block[2],"detected.")
        return fix_spec_file_num
    except IndexError:
        print("\nBad input. Please try again.")
        main()

def time_convert(raw_time):
    process_time = datetime.strptime(raw_time,'%Y%m%d-%H:%M:%S') # Parses FIX UTC timestamp as datetime object
    neat_time = process_time.strftime('%H:%M:%S on %d/%m/%Y') # Rearranges parsed timestamp into something more readable
    return neat_time

def translator(raw_fix,delim_fix):
    while True:
        try:
            delim_fix.remove('') # Remove all whitespaces from list. They remain due to delimiters present at the end of messages and cause issues unless removed.
        except ValueError:
            break

    fix_spec_file_num = spec_loader(delim_fix[0].split('.')) # Global variable for FIX spec file name
    try:
        tree = ET.parse('./spec/FIX{}.xml'.format(fix_spec_file_num)) # Reading the correct XML file
    except:
        print("Spec not supported. Please try again.\n")
    else:
        root = tree.getroot()
        fields_num = len(delim_fix) # For debugging
        print(delim_fix) # For debugging
        print("There are",fields_num,"FIX tags.\n")
        y = 0 # Initialise counter for loop
        print("\nFIELD\t\t\t\t\t VALUE\n\n") # Initialise 'table'
        for i in delim_fix:
            block_split = delim_fix[y].split('=') # Take each block and split into field and value
            field = block_split[0] # Each element in list assigned easy to use variable name
            value = block_split[1]
            if field == '52':
                value = time_convert(value) # To make timestamp easy to read
            field_trans = tree.find('fields/field[@number="%s"]'% field).attrib['name'] # Find the name of the field from the XML
            try:
                tree.find('fields/field[@number="%s"]/value'% field).tag # Check for the existence of predefined values for a field in the XML
            except: # The program throws an error when no predefined values are present
                value_trans = value # If an error is thrown, i.e. if a predefined value doesn't exist, simply passes user input to output
            else:
                value_trans = tree.find('fields/field[@number="%s"]/value[@enum="%s"]'% (field,value)).attrib['description'] # Finds predefined value
            print(field_trans,"\t\t=\t\t",value_trans,"\n") # Prints field and value with formatting
            y += 1 # Increments counter so that the loop performs the above actions for every block in the list

def repeater():
    try:
        repeat = input("Parse more FIX? y/n\n")
    except EOFError:
        print("\nstdin limit reached. Please launch the program again to continue using.\n")
        sys.exit(0)
    else:   
        if repeat == 'n':
            sys.exit(0)

def main():
    while True:
        try:
            raw_fix = input("\n\nEnter FIX: \n\n")
        except KeyboardInterrupt:
            print("\nUser interrupt detected. Exiting...\n")
            sys.exit(0)
        else:
            delim_fix = re.split('[|\s^A]',raw_fix)
            translator(raw_fix, delim_fix)
            repeater()

 
         
if __name__ == "__main__":
    main()

