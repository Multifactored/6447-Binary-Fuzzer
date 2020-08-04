# pylint: disable=W0614
from pwn import *
import os
import sys
import subprocess

# Fuzzes the binary with input from '/dev/urandom'
def urandomFuzzer(binary):

    print("Fuzzing the binary with '/dev/urandom'...")

    # We pass in the output from /dev/urandom into the binary 100 times
    for _ in range(0,100):

        # To get this input, we use the bultin function 'urandom', which returns
        # random bytes from an OS-specific randomness source.
        mutatedInput = str(os.urandom(10000))
        sendInputAndCheck(binary,mutatedInput,"Found vulnerability from '/dev/urandom'!")

# Flips random bits in the sample input and passes this into the binary
def bitFlip(sampleInputFile, binary):

    print("Flipping random bits in sample input...")

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

        sendInputAndCheck(binary,mutatedInput,"Found vulnerability from bit flip!")

def sendInputAndCheck(binary,mutatedInput,description):

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
        print(description)
        res = open("bad.txt", "w+")
        res.write(mutatedInput)
        res.close()
        os._exit(1)
