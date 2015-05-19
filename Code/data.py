__author__ = 'Ian'


import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

#Define sets of regular expression to analyze tags with normal forms, colons, and special characters
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


#List of common attribute in the new data structure to be ingest into MongoDB for further analysis
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

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


def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        old_name = m.group()

        if old_name not in expected and old_name in mapping.keys():
            #substitude the old name with the improved name in the list
            name = re.sub(street_type_re, mapping[old_name], name)
            #print old_name, "=>", name

    return name

def shape_element(element):

    node = {}

    if element.tag == "node" or element.tag == "way" :

        #loop through attribute key
        for key in element.attrib.keys():
            val = element.attrib[key]

            node["type"] = element.tag

            #create element in new data structure from information in original XML data set
            if key in CREATED:
                if not "created" in node.keys():
                    node["created"] = {}
                node["created"][key] = val
            elif key == "lat" or key == "lon":
                if not "pos" in node.keys():
                    node["pos"] = [0.0, 0.0]
                old_pos = node["pos"]
                if key == "lat":
                    new_pos = [float(val), old_pos[1]]
                else:
                    new_pos = [old_pos[0], float(val)]
                node["pos"] = new_pos
            else:
                node[key] = val

            #loop through the address tags, check against mapping list, and update bad names if applicable
            for tag in element.iter("tag"):
                tag_key = tag.attrib['k']
                tag_val = tag.attrib['v']

                if problemchars.match(tag_key):
                    continue

                elif tag_key.startswith("addr:"):

                    new_tag_val = update_name(tag_val, mapping)

                    if not "address" in node.keys():
                        node["address"] = {}


                    addr_key = tag.attrib['k'][len("addr:") : ]

                    if lower_colon.match(addr_key):
                        continue

                    else:
                        node["address"][addr_key] = new_tag_val

                #remove colons from keys name with ":"
                elif lower_colon.match(tag_key):

                    tag_val = re.sub(":", " ", tag_val)
                    node[tag_key] = tag_val

                else:
                    node[tag_key] = tag_val

        for tag in element.iter("nd"):
            if not "node_refs" in node.keys():
                node["node_refs"] = []
            node_refs = node["node_refs"]
            node_refs.append(tag.attrib["ref"])
            node["node_refs"] = node_refs

        return node

    else:
        return None


def process_map(file_in, pretty = False):

    file_out = "{0}.json".format(file_in)
    data = []

    #loop through every element in XML file, process and check data, create new data structure, and export to JSON
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def main():


    data = process_map('kathmandu_nepal.osm', False)

    #pprint.pprint(data)


if __name__ == "__main__":
    main()