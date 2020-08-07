# pylint: disable=W0614
import sys
import xml.etree.ElementTree as ET
import random
from helper import *
import copy
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

    xmlstr = ET.tostring(root).decode()
    if sendInputAndCheck(binary, xmlstr, lock):
        return True, "Found vulnerability in XML!"
    return False

def update_all_tags_attributes(root,new_attribute,repeat):
    root_copy = copy.deepcopy(root)
    list_of_found_tags = recursive_find_all_tags(root_copy,[])

    for i in list_of_found_tags:
        attributes_list_for_this_tag = i.attrib.keys()
        for attr in attributes_list_for_this_tag:
            i.set(attr,new_attribute * repeat)
    return root_copy

# this is a more generic one compared to addForgedURLS
def randomized_attributes(sampleInputFile, binary, lock):
    # similar to addForgedURLS() but this time, for all tags that have an attribute, change the attribute
    # "%s", "%p", "%x","A", "*", "1","a9", "lol"
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.read()

    root = ET.fromstring(sampleInput)

    listOfNewAttrs = ["%s", "%p", "%x","A", "*", "1","a9", "lol"]

    for i in listOfNewAttrs:
        # this can also check for buffer overflows in the attributes
        new_updated_root = update_all_tags_attributes(root, i,1000)
        xmlstr = ET.tostring(new_updated_root).decode()
        if sendInputAndCheck(binary, xmlstr, lock):
            return True, "Found vulnerability in XML by fuzzing the attributes!"    
    return False

def copyChildInfinitelyMany(sampleInputFile, binary, lock):
    print("Fuzzing the XML.. Duplicating child tags...\n", end="")
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.read()

    root = ET.fromstring(sampleInput)

    a = root.find(".")
    # need to copy the original one to avoid doing 2^n
    tmp = copy.deepcopy(a)
    # for each iteration, append to the root the children of it
    for _ in range(100):
        b = copy.deepcopy(tmp)
        a.append(b)
        xmlstr = ET.tostring(a).decode()
        if sendInputAndCheck(binary, xmlstr, lock):
            return True, "Found vulnerability in XML!"    
    return False


# try inputting large sizes with all sorts of char injects

# try lots of new lines

# try making any found links incredibly long with both regular and special chars

# try inputting a lot of random tags from a set list

# go ham with attributes
