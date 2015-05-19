__author__ = 'Ian'

import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):

        tag_list = {}

        #loop through each line in the XML file and analysis the tags
        for (event, node) in ET.iterparse(filename, ["start"]):

            tag = node.tag

            #insert net new tag to tag list
            if tag not in tag_list.keys():
                tag_list[tag] = 0

            #count 1 to exisitng or net new tags
            tag_list[tag] = tag_list[tag] + 1

        return tag_list


def main():

    filename = "kathmandu_nepal.osm"
    pprint.pprint(count_tags(filename))


if __name__ == "__main__":
    main()