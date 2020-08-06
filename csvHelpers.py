# pylint: disable=W0614
from helper import *

# Attempts to overflow the number of lines of input passed into the binary
def checkBufferOverflowLines(sampleInputFile, binary,lock):
    print("Looking for buffer overflow in number of lines...\n", end="")
    # First we read the first line of the file and store it in a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.readline()

    # We then attempt to overflow the number of lines in the input 100 times
    for i in range(1, 100):
        # We simply duplicate the first line of the file i * 10 times in our sample
        # input
        mutatedInput = (sampleInput * i * 10)
        if sendInputAndCheck(binary,mutatedInput,"Found vulnerability from buffer overflow of lines!",lock):
            return True
    return False

def checkBufferOverflowColumns(sampleInputFile, binary,lock):
    print("Looking for buffer overflow in the columns...\n", end="")
    # First we read the first line of the file and store it in a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.readline()
    columnValues = sampleInput.strip().split(",")
    modifiedValues = []
    for _ in range(0,len(columnValues)):
        modifiedValues.append("z")
    # fuzz using the original values
    print("Fuzzing Columns with original input\n", end="")
    fuzzColumns(binary,columnValues,lock)
    # fuzz using modified columnValues
    print("Fuzzing Columns with modified input values\n", end="")
    fuzzColumns(binary,modifiedValues,lock)

# For example: aaa........,bbbb.........,cccc.....,ddd...................
def fuzzColumns(binary,columnValues,lock):
    columnValues = list(columnValues)
    for _ in range(1,100):
        # increase length of each element by 10 per iteration
        columnValues = [e + "x" * 10 for e in columnValues]
        mutatedInput = ",".join(columnValues)
        if sendInputAndCheck(binary,mutatedInput,"Found vulnerability from buffer overflow in columns!",lock):
            return True
    return False
