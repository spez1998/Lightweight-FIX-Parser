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
import os

def spec_loader(spec_block):
    # Load a supplied FIX specification and tell the user which version is loaded
    try:    
        fix_spec_raw = [spec_block[1],spec_block[2]]
        fix_spec_file_num = ''.join(fix_spec_raw)
        print('FIX Specification',spec_block[1],".",spec_block[2],"detected.")
        return fix_spec_file_num
    except IndexError:
        print("\nBad input. Please try again.")
        main()

def time_convert(raw_time):
    # Convert UTC timestamps into readable format
    process_time = datetime.strptime(raw_time,'%Y%m%d-%H:%M:%S')
    neat_time = process_time.strftime('%H:%M:%S on %d/%m/%Y')
    return neat_time

def translator(raw_fix,delim_fix):
    while True:
        try:
            delim_fix.remove('')
        except ValueError:
            break
    to_replace = os.path.basename(__file__)
    cwd = sys.argv[0].replace(to_replace,'')
    # Format working directory properly
    if cwd == '':
        cwd = '.'
    fix_spec_file_num = spec_loader(delim_fix[0].split('.'))
    # Load spec
    try:
        tree = ET.parse("{}/spec/FIX{}.xml".format(cwd,fix_spec_file_num))
    except:
        print("Spec not supported. Please try again.\n")
    else:
        root = tree.getroot()
        print(fields_num,"FIX tag(s) detected.\n")
        y = 0
        print("\n\t      \t\t|\n\t  FIELD\t\t|\t\t\t\tVALUE\n\t      \t\t|\n\t      \t\t|")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        for i in delim_fix:
            block_split = delim_fix[y].split('=')
            field = block_split[0]
            value = block_split[1]
            if field == '52':
                value = time_convert(value)
            field_trans = tree.find('fields/field[@number="%s"]'% field).attrib['name']
            # Find predefined values for fields
            try:
                tree.find('fields/field[@number="%s"]/value'% field).tag
            # Error condition if field doesn't have predefined value; just load user input as value
            except:
                value_trans = value
            else:
                value_trans = tree.find('fields/field[@number="%s"]/value[@enum="%s"]'% (field,value)).attrib['description']
            # Multi-message separation
            if field == "8":
                print("----------------------------------------------------------------------------------------\n")
            print("[",field,"]",field_trans," \t= \t","[",value,"]",value_trans,"\n")
            y += 1

def repeater():
    try:
        repeat = input("Parse more FIX? y/n\n")
    except EOFError:
        # Prettier error msg
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
            print("\nUser interrupt detected. Exiting...\n") # Looks nicer
            if os.name == "posix":
                sys.exit(0)
        else:
            delim_fix = re.split('[|\n\s^A]',raw_fix)
            translator(raw_fix, delim_fix)
            repeater()
         
if __name__ == "__main__":
    main()
