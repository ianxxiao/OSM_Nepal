__author__ = 'Ian'

#this script counts the number of OSM users who contributed to the tags such as "node", "way", and "relation"

import xml.etree.ElementTree as ET
import pprint
import re

def get_user(element):

    #extract the user attribute value in each node tag
    user = element.attrib["user"]

    return user


def process_map(filename):
    users = set()


    #loop through each line in the XML file
    for _, element in ET.iterparse(filename):

        #only extract the users for element with node, way, and relation type
        if element.tag =="node" or element.tag =="way" or element.tag =="relation":
            users.add(get_user(element))
            element.clear()

    return users


def main():

    users = process_map('kathmandu_nepal.osm')
    pprint.pprint(users)


if __name__ == "__main__":
    main()