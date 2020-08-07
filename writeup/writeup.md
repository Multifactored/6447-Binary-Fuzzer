# COMP6447 Fuzzer

---

## **How It Works**

Our implementation of the black box fuzzer relies on both the dumb fuzzing and smart fuzzing approach.

Our fuzzer has 3 main features:

- File-specific fuzzer
- Dumb random byte fuzzer
- Bit-flip fuzzer

To begin, our fuzzer first attempts to determine the file format of the sample input. If a file format is found that matches what the fuzzer is compatible with, file-specific fuzzing will begin tailored to the file type. If no crashes are found, it runs the bit-flip fuzzer, followed by the dumb random byte fuzzer.

For each fuzzing function, we use pwntools to spawn a new process with the given binary, and then send it our mutated input. Then we poll the exit code of this process, and if it wasn't successful, it writes this mutated input that caused the binary to crash to 'bad.txt', and then exits the fuzzer.

**Multithreading**
We speed up this process with our multithreading implementation. When a vulnerability is found, all threads exit gracefully.

## **Possible Improvements**

## **Bug Enumeration Methods**

**Bit-Flipping**

Given a sample input to a binary, our bit-flip function will convert the sample input into a bytearray file and read over it while randomly xor'ing the bits with a random 7-bit integer in the file 500 times.

**CSV**

The CSV-specific section will attempt to find a buffer overflow in 2 ways:

- Overflowing the column count. - This is done by adding a character onto each column's values, incrementing by 1 for each attempt.
- Overflowing the lines - This is done by copying the first line of the sample input and copying it up to 10,000 times.

**JSON**

The JSON-specific section takes the sample input file and manipulates every value for every key combination.

- For every key mapping to an variable, the function will generate a random variable of the same type to replace it. This is to attempt a type based overflow, or buffer overflow.
- For lists, the function will replace it with a variable length list of integers to attempt a buffer overflow.

**XML**

placeholder

**Plaintext**

placeholder
