COMP6447 Fuzzer
=========================
Usage: `./fuzzer /path/to/binary /path/to/sampleinput`
----------------------------------------------------
**Overview**
For our implementation of this fuzzer we chose both the dumb fuzzing and smart fuzzing approach.
Our fuzzer has 3 main features:
- Dumb random byte fuzzer
- Bit-flip fuzzer
- File-specific fuzzer

To begin, our fuzzer first attempts to determine the file format of the sample input. After doing so, it runs the dumb random byte fuzzer, followed by the bit-flip fuzzer, and finally the file-specific fuzzer.

For each fuzzing function, we use pwntools to spawn a new process with the given binary, and then send it our mutated input. Then we poll the exit code of this process, and if it wasn't successful, it writes this mutated input that caused the binary to crash to 'bad.txt', and then exits the fuzzer.


**Planned Features/Improvements**
- Currently, our bit-flipping takes up to a minute to run as we are running it 500 times, as we are iterating through the sample file and randomly flipping bits. What we would like to do in the future is to implement multi-threading to cut down on the time required to do this process.
	- The above is also true for the JSON-specific function, as it generates a random value of the same type for every values of every key combination.
- We want to implement a feature to fuzz binaries which take XML files as input, we expect this to be similar in functionality to the JSON-specific fuzzer

## **Bit-Flipping**
Given a sample input to a binary, our bit-flip function will convert the sample input into a bytearray file and read over it while randomly xor'ing the bits with a random 7-bit integer in the file 500 times.

## **CSV**
Right now, the CSV-specific fuzzer will attempt to find a buffer overflow in 2 ways:
- Overflowing the column
	- This is done by adding a character onto each column's values, incrementing by 1 for each attempt.
- Overflowing the lines
	- This is done by copying the first line of the sample input and copying it up to 10,000 times.

## **JSON**
The current implementation for the JSON-specific fuzzer takes the sample input file and manipulates every value for every key combination.
For example, if a key maps to an integer, the function will generate a random integer to replace it, same logic applies for strings. This is to put a value higher than the number of bytes the buffer is allocated or give a string larger than its destination buffer.
For a list, the function will currently replace it with a variable length list of integers to attempt a buffer overflow.