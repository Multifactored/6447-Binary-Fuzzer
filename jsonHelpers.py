import sys
import json
import random

from itertools import combinations


def generateInt():
    return random.randint(1,99999999)


def generatStr():
    pass


def generateList():
    pass


def jsonRandomTyped(jsonInput: dict, key_set: list):
    ''' Mutates values of each combination in the input to random values according to input value types '''
    mutatedJson = {}
    output = []

    for subset in key_set:
        for key in subset:
            # find value type and generate random value according to that
            val = jsonInput[key]
            if type(val) == int:
                # generate random int
                val = generateInt()

            elif type(val) == str:
                # generate random string
                pass

            elif type(val) == list:
                # generate random list
                pass

            else:
                sys.exit("Unexpected type:", type(val), val)

            mutatedJson[key] = val
        
        output.append(mutatedJson)
    return


if __name__ == "__main__":
    key_set = []

    jsonInput = open(sys.argv[1], "r").read()
    jsonInput = json.loads(jsonInput)
    
    choices = list(jsonInput.keys())

    for i in range(1, len(choices) + 1):
        for combs in combinations(choices, i):
            key_set.append(combs)

    print(key_set)

    mutations = jsonRandomTyped(jsonInput, key_set)

    print(mutations)