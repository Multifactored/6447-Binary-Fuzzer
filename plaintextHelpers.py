# pylint: disable=W0614
import sys
import json
import random
from helper import *

from itertools import combinations


def randInput(sampleCombs, sampleInput):
    '''
    For each combination, create a random string for the lines left out
    i.e.
    sample = ["first", "second"]
    output = [({random_str}, {random_str}) ("first", {random_str}), ({random_str}, "second"), ("first", "second")]
    
    The set of outputs will be generated 14 times, each time the abovementioned {random_str} is generated,
    it will increase in length exponentially, from 2^0 to 2^14 in length.
    '''
    output = []

    for i in range(15):
        for currComb in sampleCombs:
            index = 0
            while index < len(sampleInput):
                currWord = []
                indexComb = 0
                while index < len(sampleInput):
                    if indexComb >= len(currComb):
                        currWord.append(generateStr(i))
                    elif sampleInput[index] != currComb[indexComb]:
                        currWord.append(generateStr(i))
                        index += 1
                        continue
                    else:
                        currWord.append(sampleInput[index])

                    index += 1
                    indexComb += 1

                output.append("\n".join(currWord) + "\n")

    return output


def typedInput(sampleCombs, sampleInput):
    ''' Mutates input, according to its type, ie int gets mutated to another int, str to str, etc. '''
    
    for currComb in sampleCombs:
        pass


def makeCombination(sampleChoices):
    outputComb = []

    for i in range(0, len(sampleChoices) + 1):
        for comb in combinations(sampleChoices, i):
            outputComb.append(comb)

    return outputComb


def fuzzPlaintext(sampleInput, binary):

    print("Attempting to fuzz the plaintext sample input...\n", end="")

    sampleInput.seek(0)
    sampleChoices = [line.strip() for line in sampleInput]
    sampleCombs = makeCombination(sampleChoices)

    mutations = []

    mutations = randInput(sampleCombs, sampleChoices)
    for i in mutations:
        sendInputAndCheck(binary, i, "Found vulnerability in plaintext!")


if __name__ == "__main__":
    sampleInput = open("./binaries/plaintextTest.txt", "r")
    fuzzPlaintext(sampleInput, "./binaries/plaintext1")
