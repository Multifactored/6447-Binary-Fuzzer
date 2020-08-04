# pylint: disable=W0614
import sys
import json
import random
from helper import *

from itertools import combinations


def generateStr():
    choices = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-={}|[]\\:\";'<>?,./~`"
    return ''.join(random.choice(choices) for i in range(random.randint(1,999)))


def randInput(sampleCombs, sampleInput):
    '''
    For each combination, create a random string for the lines left out
    i.e.
    sample = ["first", "second"]
    output = [({random_str}, {random_str}) ("first", {random_str}), ({random_str}, "second"), ("first", "second")]
    '''
    output = []

    for currComb in sampleCombs:
        index = 0
        while index < len(sampleInput):
            currWord = []
            indexComb = 0
            while index < len(sampleInput):
                if indexComb >= len(currComb):
                    currWord.append(generateStr())
                elif sampleInput[index] != currComb[indexComb]:
                    currWord.append(generateStr())
                    index += 1
                    continue
                else:
                    currWord.append(sampleInput[index])

                index += 1
                indexComb += 1

            output.append("\n".join(currWord) + "\n")

    return output


def makeCombination(sampleChoices):
    outputComb = []

    for i in range(0, len(sampleChoices) + 1):
        for comb in combinations(sampleChoices, i):
            outputComb.append(comb)

    return outputComb


def fuzzPlaintext(sampleInput, binary):

    print("Attempting to fuzz the plaintext sample input...")

    sampleInput.seek(0)
    sampleChoices = [line.strip() for line in sampleInput]
    sampleCombs = makeCombination(sampleChoices)

    mutations = []

    mutations = randInput(sampleCombs, sampleChoices)
    for i in mutations:
        sendInputAndCheck(binary, i, "Found vulnerability in plaintext!")


if __name__ == "__main__":
    sampleInput = open("./binaries/plaintextTest.txt", "r")
    fuzzPlaintext(sampleInput, "./binaries/plaintext2")
