#!/usr/bin/env python3
# pylint: disable=W0614
from pwn import *
import sys
import subprocess
import os
from csvHelpers import *
from jsonHelpers import *
from type_checker import checkCSV, checkJSON

# TODO: how do we stop 'core' file being created when vulnerability in binary found...

# this is to silent pwntool logs
context.log_level = 'error'

def runCSVFuzzer(sampleInput, binary):
    checkBufferOverflowLines(sampleInput, binary)
    checkBufferOverflowColumns(sampleInput, binary)

def runJSONFuzzer(sampleInput, binary):
    fuzzJSON(sampleInput, binary)

if __name__ == "__main__":

    # First check the correct number of arguments are given.
    if len(sys.argv) != 3:
        sys.exit("Usage: ./fuzzer.py program sampleinput.txt")

    # We begin by opening the sample input file for reading, and extract the contents.
    try:
        sampleInput = open(sys.argv[2], 'r')
    except:
        print("Error:", sys.exc_info()[0])
        sys.exit("Usage: ./fuzzer.py program sampleinput.txt")

    # We also know the binary will be the first argument given.
    binary = sys.argv[1]

    # Next we want to determine the format of the sample input's contents.
    isCSV = isJSON = isXML = False

    # We first check if it is in csv format.
    if checkCSV(sampleInput):
        isCSV = True
        print("Is a CSV file...")

    # Once this is complete, we also need to reset the file pointer to the
    # beginning of the file for future reading/writing.
    sampleInput.seek(0)

    # Next we check if it is in json format.
    if checkJSON(sampleInput):
        isJSON = True
        print("Is a JSON file...")

    # Once this is complete, we also need to reset the file pointer to the
    # beginning of the file for future reading/writing.
    sampleInput.seek(0)

    # TODO: Also check if XML format (however not requried for midpoint)

    # Now we can begin fuzzing the binary.
    # To begin, we first fuzz the binary with input from '/dev/urandom'.
    urandomFuzzer(binary)

    # Next, we can try bit flipping the sample input.
    bitFlip(sampleInput, binary)

    # If we determined the file is in CSV format, we can further fuzz the sample CSV
    # input.
    if isCSV:
        runCSVFuzzer(sampleInput, binary)
    if isJSON:
        runJSONFuzzer(sampleInput,binary)

    print("No vulnerabilities found :(")
