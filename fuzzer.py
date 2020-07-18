#!/usr/bin/env python3
from pwn import *   # pylint: disable=W0614
import sys
import subprocess
import os

from type_checker import checkCSV, checkJSON

# Silences the pwntool logs
context.log_level = 'error'

# File to store bad inputs
BAD_INPUT_FILE = "bad.txt"

# Fuzzes the binary with input from '/dev/urandom'
def urandomFuzzer(pathToBinary):

    print("Fuzzing the binary with '/dev/urandom'...")

    # We pass in the output from /dev/urandom into the binary 200 times
    for _ in range(0,200):
        command = "cat /dev/urandom | " + pathToBinary
        retval = subprocess.call(command, shell=True, stdout=open(os.devnull, 'wb'))
        
        # If this input resulted in an error, we want to write it to 'bad.txt'
        # TODO: this won't print the exact cat command used into bad.txt
        if retval != 0:
            print("Found vulnerability from '/dev/urandom'!")
            res = open(BAD_INPUT_FILE, "w+")
            res.write(command)
            res.close()
            sys.exit()

# Flips random bits in the sample input and passes this into the binary
def bitFlip(sampleInputFile, binary):

    print("Flipping random bits in sample input...")

    # First we have to read the file and store it as a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.read()
    
    # We then randomly flip bits in the sample input 1000 times
    for _ in range(0, 1000):

        # We first convert the sample input into a bytearray
        b = bytearray(sampleInput, 'UTF-8')

        # Then we search through the entire bytearray created, and randomly
        # flip some of the bits
        for i in range(0, len(b)):
            if random.randint(0, 20) == 1:
                b[i] ^= random.getrandbits(7)

        # Once we have flipped the bits, we want to decode this back into a string
        # that can be passed in as input to the binary
        mutatedInput = b.decode('ascii')
        
        # We now send this mutated input into the binary
        p = process(binary)
        p.sendline(mutatedInput)
        p.proc.stdin.close()

        # After it has finished running, we check the exit status of the process.
        # If this input resulted in an error, we want to write it to 'bad.txt' and 
        # exit the fuzzer
        exit_status = p.poll(block=True)
        p.close()
        if exit_status != 0:
            print("Found vulnerability from bit flip!")
            res = open(BAD_INPUT_FILE, "w+")
            res.write(mutatedInput)
            res.close()
            sys.exit()

# Attempts to overflow the number of lines of input passed into the binary
def checkBufferOverflowLines(sampleInputFile, binary):

    print("Looking for buffer overflow in number of lines...")
    
    # First we read the first line of the file and store it in a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.readline()

    # We then attempt to overflow the number of lines in the input 1000 times
    for i in range(1, 1000):

        # We simply duplicate the first line of the file 'i' times in our sample
        # input
        mutatedInput = (sampleInput * i)
        
        # We now send this mutated input into the binary
        p = process(binary)
        p.sendline(mutatedInput)
        p.proc.stdin.close()

        # After it has finished running, we check the exit status of the process.
        # If this input resulted in an error, we want to write it to 'bad.txt' and 
        # exit the fuzzer
        exit_status = p.poll(block=True)
        p.close()
        if exit_status != 0:
            print("Found vulnerability from buffer overflow of lines!")
            res = open(BAD_INPUT_FILE, "w+")
            res.write(mutatedInput)
            res.close()
            exit()

# TODO: implement function to overflow number of columns in input passed to binary
# For example: aaa........,bbbb.........,cccc.....,ddd...................
def checkBufferOverflowColumns(sampleInput, binary):

    #print("Looking for buffer overflow in number of columns...")
    
    #p = process(binary)
    #return p.poll()
    return

def runCSVFuzzer(sampleInput, binary):
    checkBufferOverflowLines(sampleInput, binary)
    checkBufferOverflowColumns(sampleInput, binary)


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

    print("No vulnerabilities found :(")