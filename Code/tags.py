__author__ = 'Ian'


import xml.etree.ElementTree as ET
import pprint
import re


#OVERALL OBJECTIVE: OUTPUT COUNTS BY TAG QUALITY BUCKET BY "LOWER", "LOWER_COLON", "PROBLEMCHARS", AND "OTHER"

#Define sets of regular expression to analyze tags with normal forms, colons, and special characters
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":

        #use .attrib() to return the dictionary of attributes and access the "k"
        key = element.attrib['k']

        #check against each pre-defined regular expression and count towards the appropriate bucket
        if lower.search(key):
            keys["lower"] = keys["lower"] + 1
        elif lower_colon.search(key):
            keys["lower_colon"] = keys["lower_colon"] + 1
        elif problemchars.search(key):
            keys["problemchars"] = keys["problemchars"] + 1
        else:
            keys["other"] = keys["other"] + 1

        pass

    return keys



def process_map(filename):

    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

    #loop through each line in the XML file and analysis the tags
    for _, element in ET.iterparse(filename):

        #determine the tag type
        keys = key_type(element, keys)

        #clear the memory
        element.clear()

    return keys


def main():

    keys = process_map('kathmandu_nepal.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    main()