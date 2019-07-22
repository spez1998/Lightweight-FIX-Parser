# Liquidnet Lightweight FIX Parser
# Written by Sujit Malde July 2019 
# Free to use under GNU GPL 3.0

# !!!!!!!!! READ ME !!!!!!!!!
# This tool takes a FIX message as input (either via manual input to CLI or via piped command) and outputs a readable, verbose version.
# Terminology used is defined as follows. For a FIX message in the format:
# X=Y(D)X=Y(D)X=Y(D)...
# X = field, Y = value, (D) = delimiter (commonly ASCI code 0x01, could also be | or space)

import xml.etree.ElementTree as ET # XML parsing library
import re # String manipulation library
from datetime import datetime

tree = ET.parse('FIX5spec.xml') # Parse XML into tree called 'tree'
root = tree.getroot()

def time_convert(raw_time):
    process_time = datetime.strptime(raw_time,'%Y%m%d-%H:%M:%S') # Parses FIX UTC timestamp as datetime object
    neat_time = process_time.strftime('%H:%M:%S on %d/%m/%Y') # Rearranges parsed timestamp into something more readable
    return neat_time

print("Liquidnet Lightweight FIX Parser (written by Sujit Malde 2019)")

raw_fix = input("\n\nEnter FIX: \n") # Get the raw FIX message from the user (works via pipe)
delim_fix = re.split('[|\s^A]',raw_fix) # Remove all common delimiters and place blocks into a list

# Remove all whitespaces from list. They remain due to delimiters present at the end of messages and cause issues unless removed.
while True:
    try:
        delim_fix.remove('')
    except ValueError:
        break

fields_num = len(delim_fix) # For debugging
print(delim_fix) # For debugging
print("There are",fields_num,"FIX tags")

'''new'''
y= 0 # Initialise counter for loop
print("\nField\t\t\tValue\n\n") # Initialise 'table'
for i in delim_fix:
    block_split = delim_fix[y].split('=') # Take each block and split into field and value
    field = block_split[0] # Each element in list assigned easy to use variable name
    value = block_split[1]
    if field == '52':
         value = time_convert(value) # To make timestamp easy to read
    field_trans = tree.find('fields/field[@number="%s"]'% field).attrib['name'] # Find the name of the field from the XML
    try:
        tree.find('fields/field[@number="%s"]/value'% field).tag # Check for the existence of predefined values for a field in the XML
        # The program to throw an error when no predefined values are present
    except:
        value_trans = value # If an error is thrown, i.e. if a predefined value doesn't exist, simply passes user input to output
    else:
        value_trans = tree.find('fields/field[@number="%s"]/value[@enum="%s"]'% (field,value)).attrib['description'] # Finds predefined value
    print(field_trans," = ",value_trans) # Prints field and value with formatting
    y+= 1 # Increments counter so that the loop performs the above actions for every block in the list
    

'''/new'''
'''old'''
'''
eg1 = fix_block()

eg1.field = input("Enter example FIX field: ")

try:
    tree.find('fields/field[@number="%s"]/value'% eg1.field).tag
except:
    pass
else:
    eg1.value = input("Enter example FIX value: ")

fix_block.flag = input('Enter a flag eg :')
eg1 = fix_block()
eg1.flag = fix_block.flag

field_trans = tree.find('fields/field[@number="%s"]'% eg1.field).attrib['name']
value_trans = tree.find('fields/field[@number="%s"]/value[@enum="%s"]'% (eg1.field,eg1.value)).attrib['description']
print("\n Field\t\t\t\t Value\n\n",eg1.field," = ",field_trans,"\t\t",eg1.value," = ",value_trans)
'''
