import xml.etree.ElementTree as ET
import re

tree = ET.parse('FIX5spec.xml')
root = tree.getroot()

raw_fix = input("Enter FIX: \n")
'''delim_fix=raw_fix.split('^A')'''
delim_fix = re.split('[\s^A]',raw_fix)
while True:
    try:
        delim_fix.remove('')
    except ValueError:
        break

flags_num = len(delim_fix)

print(delim_fix)
print("There are",flags_num,"FIX tags")

'''x = input("Enter FIX field for example: \n")
number = tree.find('fields/field[@number="%s"]'% x).attrib['name']
print(number)'''

class fix_block:
    def __init__(self,field,value):
        self.field = FLAG
        self.value_bool = 0
        self.value = VALUE

eg1 = fix_block()
eg1.field = input("Enter example FIX field: ")
try:
    tree.find('fields/field[@number="%s"]/value'% eg1_block.field).tag
except:
    pass
else:
    eg1.value = input("Enter example FIX value: ")

'''def my_func():
    while True:
        try:
            tree.find('fields/field[@number="%s"]/value'% fix_block.flag).tag
            value_translation = input('Enter value example: ')
            break
        except AttributeError:
            break

fix_block.flag = input('Enter a flag eg :')
eg1 = fix_block()
eg1.flag = fix_block.flag

flag_translation = tree.find('fields/field[@number="%s"]'% eg1.flag).attrib['name']
value_translation = tree.find('fields/field[@number="%s"]/value[@enum="%s"]'% (eg1.flag,eg1.value)).attrib['description']'''
print("\n Field\t\t\t\t Value\n\n",eg1.field,"\t\t\t",eg1.value)
