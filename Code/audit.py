__author__ = 'Ian'


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "kathmandu_nepal.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#List of common street identifiers
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

#Mapping between bad and standardized names
mapping = { 'Gali':'Galli',
            'galli':'Galli',
            'Marg':'Marga',
            'marg':'Marga',
            'Marg-1':'Marga',
            'marg-1':'Marga',
            'marga':'Marga',
            'Maarga':'Marga',
            'M.':'Marga',
            'Path':'Path',
            'path':'Path',
            'Rd':'Road',
            'Rd.':'Road',
            'road':'Road',
            'ROAD':'Road',
            'SADAK':'Sadak',
            'sadak':'Sadak',
            'tole':'Tole',
            'chowk':'Chowk'
            }

def audit_street_type(street_types, street_name):

    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        #loop through all node / way and create a list of street name types for analysis
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping, counter):

    m = street_type_re.search(name)

    if m:
        old_name = m.group()

        if old_name not in expected and old_name in mapping.keys():
            #substitude the old name with the improved name in the list
            name = re.sub(street_type_re, mapping[old_name], name)
            print old_name, "=>", name
            counter += 1


    return name, counter


def main():

    st_types = audit(OSMFILE)
    counter = 0

    #loop through each element in the XML file
    for st_type, ways in st_types.iteritems():
        for name in ways:

            #
            better_name, counter = update_name(name, mapping, counter)

    print counter


if __name__ == '__main__':
    main()