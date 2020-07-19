# pylint: disable=W0614
import sys
import json
import random
from helper import *

from itertools import combinations


def generateInt():
    return random.randint(1,99999999)


def generateStr():
   choices = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_+-={}|[]\:\";'<>?,./~`"
   return ''.join(random.choice(choices) for i in range(random.randint(1,999)))


def generateList():
    return random.sample(range(0, 9999), random.randint(1,100))


def jsonRandomTyped(jsonInput: dict, key_set: list):
    ''' Mutates values of each combination in the input to random values according to input value types '''
    output = []

    for subset in key_set:
        mutatedJson = {}
        for key in subset:
            # find value type and generate random value according to that
            val = jsonInput[key]
            if type(val) == int:
                # generate random int
                val = generateInt()

            elif type(val) == str:
                # generate random string
                val = generateStr()

            elif type(val) == list:
                # generate random list
                val = generateList()

            else:
                sys.exit("Unexpected type:", type(val), val)

            mutatedJson[key] = val

        output.append(mutatedJson)
    return output

def fuzzJSON(sampleInputFile, binary):

    print("Fuzzing the JSON formatted sample input...")

    key_set = []

    jsonInput = sampleInputFile.read()
    jsonInput = json.loads(jsonInput)

    choices = list(jsonInput.keys())

    for i in range(1, len(choices) + 1):
        for combs in combinations(choices, i):
            key_set.append(combs)

    mutations = jsonRandomTyped(jsonInput, key_set)
    for i in mutations:
        sendInputAndCheck(binary,json.dumps(i),"Found vulnerability in JSON!")

if __name__ == "__main__":
    # for testing
    print(generateStr())