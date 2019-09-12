import xml.etree.ElementTree as ET
import os
import sys
import re

allowed_symbols = "\"!#$%&'()*+,-./:;<=>?@[\]^_`{}~"

class Translator:
    def __init__(self,field,value,spec_num):
        self.field = field
        self.value = value
        self.spec_num = spec_num

    def spec_loader(self):
        # Load desired FIX spec XML per message
        spec_num = self.spec_num.split("8=FIX.")[1].split(".")
        to_replace = os.path.basename(__file__)
        cwd = sys.argv[0].replace(to_replace,'')
        # Correct working directory path
        if cwd == '':
            cwd = '.' 
        try:
            self.tree_path = cwd+"/spec/FIX"+spec_num[0]+spec_num[1]+".xml"
        except:
            print("Something went wrong")

    def exceptions(self):
        # Change fields/values for certain fields
        if self.field == "27":
            self.value = "S"

    def xml_lookup(self):
        tree = ET.parse(self.tree_path)
        self.field_lookup = tree.find('fields/field[@number="%s"]'% self.field).attrib['name']
        try:
            tree.find('fields/field[@number="%s"]/value'% self.field).tag
        except:
            self.value_lookup = self.value
        else: 
            self.value_lookup = tree.find('fields/field[@number="%s"]/value[@enum="%s"]'% (self.field,self.value)).attrib['description']
            if self.field == "27":
                self.value = "!!!"
                self.value_lookup = "CHECK MANUALLY"
    
    def printer(self):
        print("[",self.field,"]",self.field_lookup," \t\t= \t\t [",self.value,"]",self.value_lookup,"\n")

def parser():
    # User input into 2-dimensional list (split by message, then by field)
    raw_fix = input("Enter raw FIX\n").split("8=FIX.")
    changing_fix = [i for i in raw_fix if i]
    changing_fix = ["8=FIX." + i for i in changing_fix]
    fix_lists = [i.split("\x01") for i in changing_fix]
    print("\n\t      \t\t\t|\n\t  FIELD\t\t\t|\t\t\t\tVALUE\n\t      \t\t\t|\n\t     \t\t\t|")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    for i in fix_lists:
        del i[-1]
        spec_num = i[0]
        for j in i: 
            k = j.split("=")
            if k[0]:
                field = k[0]
            if k[1]:
                value = k[1]
            to_translate = Translator(field,value,spec_num)
            to_translate.spec_loader()
            to_translate.exceptions()
            to_translate.xml_lookup()
            to_translate.printer()

def main():
    while True:
        parser()

if __name__ == "__main__":
    main()
