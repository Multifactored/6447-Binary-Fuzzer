# pylint: disable=W0614
from helper import *

# Attempts to overflow the number of lines of input passed into the binary
def checkBufferOverflowLines(sampleInputFile, binary):
    print("Looking for buffer overflow in number of lines...")
    # First we read the first line of the file and store it in a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.readline()

    # We then attempt to overflow the number of lines in the input 10,000 times
    for i in range(1, 10000):
        # We simply duplicate the first line of the file 'i' times in our sample
        # input
        mutatedInput = (sampleInput * i)
        sendInputAndCheck(binary,mutatedInput,"Found vulnerability from buffer overflow of lines!")
    return

def checkBufferOverflowColumns(sampleInputFile, binary):
    print("Looking for buffer overflow in the columns...")
    # First we read the first line of the file and store it in a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.readline()
    columnValues = sampleInput.strip().split(",")
    modifiedValues = []
    for _ in range(0,len(columnValues)):
        modifiedValues.append("z")
    # fuzz using the original values
    print("Fuzzing Columns with original input")
    fuzzColumns(binary,columnValues)
    # fuzz using modified columnValues
    print("Fuzzing Columns with modified input values")
    fuzzColumns(binary,modifiedValues)

# For example: aaa........,bbbb.........,cccc.....,ddd...................
def fuzzColumns(binary,columnValues):
    columnValues = list(columnValues)
    for _ in range(1,1000):
        # increase length of each element per iteration
        columnValues = [e + "i" for e in columnValues]
        mutatedInput = ",".join(columnValues)
        sendInputAndCheck(binary,mutatedInput,"Found vulnerability from buffer overflow in columns!")
    return
