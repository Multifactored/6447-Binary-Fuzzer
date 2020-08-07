# pylint: disable=W0614
from pwn import *
import os
import sys
import subprocess

# Fuzzes the binary with input from '/dev/urandom'


def urandomFuzzer(binary, lock):

    print("Fuzzing the binary with '/dev/urandom'...\n", end="")

    # We pass in the output from /dev/urandom into the binary 100 times
    for _ in range(0, 100):

        # To get this input, we use the builtin function 'urandom', which returns
        # random bytes from an OS-specific randomness source.
        mutatedInput = str(os.urandom(10000))
        if sendInputAndCheck(binary, mutatedInput, lock):
            return True, "Found vulnerability from '/dev/urandom'!"
    return False

# Flips random bits in the sample input and passes this into the binary


def bitFlip(sampleInputFile, binary, lock):

    print("Flipping random bits in sample input...\n", end="")

    # First we have to read the file and store it as a string
    sampleInputFile.seek(0)
    sampleInput = sampleInputFile.read()

    # We then randomly flip bits in the sample input 500 times
    for _ in range(0, 500):

        # We first convert the sample input into a bytearray
        b = bytearray(sampleInput, 'UTF-8')

        # Then we search through the entire bytearray created, and randomly
        # flip some of the bits
        for i in range(0, len(b)):
            if random.randint(0, 20) == 1:
                b[i] ^= random.getrandbits(7)

        # Once we have flipped the bits, we want to decode this back into a string
        # that can be passed in as input to the binary
        mutatedInput = b.decode('ascii').strip()

        if sendInputAndCheck(binary, mutatedInput, lock):
            return True, "Found vulnerability from bit flip!"
    return False


def sendInputAndCheck(binary, mutatedInput, lock):
    # this is to silence pwntool logs
    context.log_level = 'error'

    p = process(binary)
    p.sendline(mutatedInput)
    p.proc.stdin.close()

    exit_status = p.poll(block=True)
    p.close()

    # After it has finished running, we check the exit status of the process.
    # If this input resulted in an exit status less than 0 (and also didn't abort),
    # this means there was an exception, so we want to write it to 'bad.txt'
    # and exit the fuzzer.
    if exit_status < 0 and exit_status != -6:
        lock.acquire()
        res = open("bad.txt", "w+")
        res.write(mutatedInput)
        res.close()
        return True
    return False

def endTime(start):
    end = time.time()
    difference = end - start
    difference = time.localtime(difference).tm_sec
    print("Elapsed Time: " + str(difference) + " seconds")
    
def generateInt():
    return random.randint(-99999999, 99999999)


def generateStr(maxPower):
    choices = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-={}|[]\\:\";'<>?,./~`"
    maxPower = 2 ** maxPower
    return ''.join(random.choice(choices) for i in range(maxPower))


def generateList():
    return random.sample(range(0, 9999), random.randint(1, 100))


def valGenerateTyped(val, i):
    # find value type and generate random value according to that
    if type(val) == int:
        # generate random int
        val = generateInt()

    elif type(val) == str:
        # account for the case where something like "1" is passed in
        try:
            val = int(val)
            val = str(generateInt())
        except ValueError:
            # generate random string
            val = generateStr(i)

    elif type(val) == list:
        # generate random list
        val = generateList()

    else:
        sys.exit("Unexpected type:", type(val), val)

    return val
