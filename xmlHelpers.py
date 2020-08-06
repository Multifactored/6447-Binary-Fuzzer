# pylint: disable=W0614
import sys
import xml.etree.ElementTree as ET
import random
from helper import *

from itertools import combinations

# TODO

def recursive_find_all_tags(root,result):
    for _ in root:
        result.append(_)
        recursive_find_all_tags(_,result)
    return result

def addForgedURLS(sampleInputFile, binary, lock):
    print("Fuzzing the XML formatted sample input...\n", end="")
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.read()

    root = ET.fromstring(sampleInput)
    
    list_of_found_tags = recursive_find_all_tags(root,[])
    all_tags_with_href = []

    for i in list_of_found_tags:
        try:
            if(i.attrib['href']):
                all_tags_with_href.append(i)
        except:
            pass
    # print(all_tags_with_href)
    for i in all_tags_with_href:
        i.set('href',"%s" * 100)


    # NEED TO ADD MORE VARIATIONS, THIS IS JUST FOR XML1
    xmlstr = ET.tostring(root).decode()
    if sendInputAndCheck(binary, xmlstr, lock):
        return True, "Found vulnerability in XML!"
    return False

# try having near infinite sub elements <div> <div> <div> <div>...</div></div></div></div>

# try inputting large sizes with all sorts of char injects

# try lots of new lines

# try making any found links incredibly long with both regular and special chars

# try inputting a lot of random tags from a set list

# go ham with attributes
