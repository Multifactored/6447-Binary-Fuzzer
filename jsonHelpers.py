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

    for subset in key_set:
        for key in subset:
            # find value type and generate random value according to that
            if type(jsonInput[key]) == int:
                # generate random int
                val = generateInt()
            elif type(jsonInput[key]) == str:
                # generate random string
                pass
            elif type(jsonInput[key]) == list:
                # generate random list
                pass
            else:
                sys.exit("Unexpected type:", type(jsonInput[key]), jsonInput[key])

            mutatedJson[key] = val
        
        yield mutatedJson


if __name__ == "__main__":
    x = []

    jsonInput = open(sys.argv[1], "r").read()
    jsonInput = json.loads(jsonInput)
    
    choices = list(jsonInput.keys())

    for i in range(1, len(choices) + 1):
        for combs in combinations(choices, i):
            x.append(combs)

    print(x)