#!/usr/bin/env python3
from pwn import *   # pylint: disable=W0614
import sys
import subprocess
import os

from type_checker import checkCSV, checkJSON

# this is to silent pwntool logs
context.log_level = 'error'

# this will fuzz the binary with /dev/null for 200 times
# if error found, will return True
# all error messages (when process return value != 0) will be stored in ERRORDETAILS
def urandomFuzzer(pathToBinary):
    for _ in range(0,200):
        command = "cat /dev/urandom | " + pathToBinary
        retval = subprocess.call(command,
                                 shell=True,
                                 stdout=open(os.devnull, 'wb'),
                                 stderr=open(ERRORDETAILS,'a+')
                                )
        if retval != 0:
            return True
    return False


def checkBufferOverflowLines(sampleInput, badInput, binary):
    ''' check overflow by overflowing num of lines '''
    sampleInput.seek(0)
    inputToBeSent = sampleInput.readline()
    overflow = False
    i = 1
    print("Looking for buffer overflow...")
    while True: # consider limiting this so it wouldn't go to 19234782349821734 lines
        try:
            p = process(binary)
            p.sendline((inputToBeSent * i).strip())
            i += 1
        except:
            print("Caught error:", sys.exc_info()[0])
            overflow = True
            break

    if overflow:
        print("Found buffer overflow!")
        res = open(badInput,"w+")
        res.write((inputToBeSent * i))
        res.close()

    return overflow

# overflow the columns
# aaa........,bbbb.........,cccc.....,ddd...................
# def checkBufferOverflowColumns(sampleInput):
#     p = process(sys.argv[1])
#     return p.poll()


def runCSVFuzzer(sampleInput, badInput, binary):
    checkBufferOverflowLines(sampleInput, mutatedInput, binary)
    # checkBufferOverflowColumns(sampleInput)


if __name__ == "__main__":
    # First check the correct number of arguments are given.
    if len(sys.argv) != 3:
        # NEED TO MAKE SURE PROGRAM IS A PATH,NOT JUST THE BINARY NAME
        # ./csv1 instead of csv1

        sys.exit("Usage: ./fuzzer.py program sampleinput.txt")

    # We begin by opening the sample input file for reading, and extract the contents.
    try:
        sampleInput = open(sys.argv[2], 'r')
    except:
        print("Error:", sys.exc_info()[0])
        sys.exit("Usage: ./fuzzer.py program sampleinput.txt")

    # file to store errors
    ERRORDETAILS = "errors.txt"
    INPUT_THAT_BREAKS = "bad.txt"
    # Next we want to determine the format of the sample input's contents.

    # init flags
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

    # TODO: CHECK XML, not required for midpoint

    # Initially try fuzzing the following:
    # repeat 100 (cat /dev/urandom | program)
    # Then if this fails, move onto specialised fuzzes based on the sampleinput format
    # (could also try bit flipping)

    binary = sys.argv[1]

    if urandomFuzzer(binary):
        print("Found a crash from /dev/urandom input .... saving to " + ERRORDETAILS)


    # We would want to loop the following code, repeating for each new mutated input
    mutatedInput = sampleInput.read()

    # Run the program using pwntools, passing your mutated input as an argument.

    if isCSV:
        runCSVFuzzer(sampleInput, INPUT_THAT_BREAKS, binary)

    p = process(binary)
    p.send(mutatedInput)
    print("Current input is:\n{}".format(mutatedInput))

    # If we got a crash, write the bad input to bad.txt
    # TODO: we need a harness to check whether the program crashed...
    # (note how when running csv1 with json1.txt, it states it stopped with exit code 0,
    # so I think we can use pwntools as the harness and check for the exit code)
    if False:
        print("Found bad input.")
        result = open(INPUT_THAT_BREAKS, "w+")
        result.writelines([mutatedInput])
        result.close()
        exit()

    p.close()

    '''
    # Example byteflip function
    def byteflip(input):
        b = bytearray(json, 'UTF-8')

        for i in range(0, len(b)):
            if random.randint(0, 20) == 1:
                b[i] ^= random.getrandbits(7)

        return b.decode('ascii)

    # How to call the byte flip function
    for i in range(0, 100000):
        yield byteflip(input)
    '''