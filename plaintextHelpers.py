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
            while index < len(sampleInput) - 1:
                currWord = []
                indexComb = 0
                while index < len(sampleInput):
                    if indexComb >= len(currComb):
                        currWord.append(generateStr(i))
                    elif sampleInput[index] != currComb[indexComb]:
                        currWord.append(generateStr(i))
                    else:
                        currWord.append(sampleInput[index])
                        indexComb += 1

                    index += 1
                output.append("\n".join(currWord) + "\n")

    # delete every 4th, duplicate of sample input
    del output[3::4]
    return output


def typedInput(sampleCombs, sampleInput):
    ''' Mutates input, according to its type, ie int gets mutated to another int, str to str, etc. '''
    output = []

    for i in range(15):
        for currComb in sampleCombs:
            index = 0

            while index < len(sampleInput):
                currWord = []
                indexComb = 0
                while index < len(sampleInput):
                    if indexComb >= len(currComb):
                        currWord.append(sampleInput[index])
                    elif sampleInput[index] != currComb[indexComb]:
                        currWord.append(sampleInput[index])
                    else:
                        currWord.append(valGenerateTyped(sampleInput[index], i))
                        indexComb += 1

                    index += 1

                output.append("\n".join(currWord) + "\n")

    return output


def makeCombination(sampleChoices):
    outputComb = []

    for i in range(0, len(sampleChoices) + 1):
        for comb in combinations(sampleChoices, i):
            outputComb.append(comb)

    return outputComb


def fuzzPlaintext(sampleInput, binary,lock):

    print("Attempting to fuzz the plaintext sample input...\n", end="")

    sampleInput.seek(0)
    sampleChoices = [line.strip() for line in sampleInput]
    sampleCombs = makeCombination(sampleChoices)

    mutations = []

    print("Attempting random plaintext fuzzing")
    mutations = randInput(sampleCombs, sampleChoices)
    for i in mutations:
        if sendInputAndCheck(binary, i,lock):
            return True , "Found vulnerability in plaintext!"
    
    print("Attempting random-typed plaintext fuzzing")
    mutations = typedInput(sampleCombs, sampleChoices)
    for i in mutations:
        if sendInputAndCheck(binary, i,lock):
            return True , "Found vulnerability in plaintext!"
    return False

if __name__ == "__main__":
    sampleInput = open("./binaries/plaintext2.txt", "r")
    sampleInput.seek(0)
    fuzzPlaintext(sampleInput, "./binaries/plaintext2")
