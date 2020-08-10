# pylint: disable=W0614
import sys
import json
import random
from helper import *
from itertools import combinations
import copy


def brokenJson(jsonInput: dict, key_set: list, maxPower: int):
    # similar to generateStr() except this has a higher chance of having the characters {}"
    choices = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890::::::{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"{}"'
    maxPower = 2 ** maxPower
    output = "{" + "\"" + generateStr(0) + "\": "+ ''.join(random.choice(choices) for i in range(maxPower)) + "}"

    return output


def jsonInJson(jsonInput: dict, key_set: list):
    output = {}
    jsonStr = json.dumps(jsonInput)
    for key in jsonInput.keys(): 
        output[key] = jsonStr * 20

    return output


def jsonRandomTyped(jsonInput: dict, key_set: list):
    ''' Mutates values of each combination in the input to random values according to input value types '''
    output = []

    for i in range(6):
        for subset in key_set:
            mutatedJson = copy.deepcopy(jsonInput)
            for key in subset:
                # find value type and generate random value according to that
                val = jsonInput[key]
                val = valGenerateTyped(val, i + 2)

                mutatedJson[key] = val

            output.append(mutatedJson)
    return output


def fuzzJSON(sampleInputFile, binary, lock):

    print("Fuzzing the JSON formatted sample input...\n", end="")

    key_set = []

    sampleInputFile.seek(0)
    jsonInput = sampleInputFile.read()
    jsonInput = json.loads(jsonInput)

    choices = list(jsonInput.keys())

    for i in range(1, len(choices) + 1):
        for combs in combinations(choices, i):
            key_set.append(combs)

    for i in range(10):
        for j in range(10):
            if sendInputAndCheck(binary, brokenJson(jsonInput, key_set, j), lock):
                return True, "Found vulnerability in JSON!"

    for i in range(10):
        badJson = generateBadJson(i).replace('\\"',"\"")
        if sendInputAndCheck(binary, badJson, lock):
            return True, "Found vulnerability in JSON!"

    if sendInputAndCheck(binary, json.dumps(jsonInJson(jsonInput, key_set)), lock):
        return True, "Found vulnerability in JSON!"

    mutations = jsonRandomTyped(jsonInput, key_set)
    for i in mutations:
        if sendInputAndCheck(binary, json.dumps(i), lock):
            return True, "Found vulnerability in JSON!"
    return False


if __name__ == "__main__":
    # for testing
    print(generateBadJson(10))
    fuzzJSON(open("./binaries/json2.txt", "r"), "./binaries/json2", "")
