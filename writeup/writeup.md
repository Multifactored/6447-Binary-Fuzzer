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

**Multiprocessing**
We speed up this process with our multiprocessing implementation. We decided to use max_workers=multiprocessing.cpu_count(), the theoretical maximum number of processes we can run at any given moment. When a vulnerability is found from any one of the processes, all the other processes will exit.

## **Possible Improvements**

There are multiple improvements we can make if we want to take the fuzzer further.

- Implement a code coverage fuzzing, so that it generates permutations based on the previous trace file produced. We had a look on implementing this using qemu and gdb but due to limited time and resources, we couldnt get it to work properly.
- Implement an user interface that reports on current progress, elapsed time during execution and general polish.
- Fuzz multiple binaries at once, and fuzzing multiple crashes per execution.
- Check for more file types.

## **Bug Enumeration Methods**

**Bit-Flipping**

Given a sample input to a binary, our bit-flip function will convert the sample input into a bytearray file and read over it while randomly xor'ing the bits with a random 7-bit integer in the file 500 times.

**CSV**

The CSV-specific section will attempt to find a buffer overflow in 2 ways:

- Overflowing the column count. - This is done by adding a character onto each column's values, incrementing by 1 for each attempt.
- Overflowing the lines - This is done by copying the first line of the sample input and copying it up to 10,000 times.

**JSON**

The JSON-specific section does two things in sequential order to find a vulnerability.

The first method takes the sample input file and manipulates every value for every key combination.

- For every key mapping to an variable, the function will generate a random variable of the same type to replace it. This is to attempt a type based overflow, or buffer overflow.
- For lists, the function will replace it with a variable length list of integers to attempt a buffer overflow.

The second method relies on the creation of broken JSON statements, including erroneous data and nested json statements. This is used after the first method in order to catch strange edge cases in which exceptions are not handled properly.

**XML**

The XML-specific section tries to permutate input with four different methods to achieve a segfault. These are listed below:

- The sample input's attribute tags are replaced with possibly vulnerable attributes, including format string and type vulnerabilities. This can either buffer overflow attribute checking functions, or create strange behaviour.
- If there are URLs in sample input, we replace them with a bunch of '%s' to attempt a format string vulnerability to read invalid memory. This technique is a subset of the first one but specifically targets the URLs.
- The fuzzer attempts to copy the root of the sample input and appends it to the root multiple times.
- Finally, it generates long nested tag statements to attempt to overflow the parser processing tags.

**Plaintext**

The plaintext-specific section attempts to find an overflow by sequentially trying both:

- For every line combination we try:
	- Inputting randomly generated strings that increase exponentially in length, up to 2^14
	- Mutating input from the provided input according to its type.
- This is so that we can maximise the visited code paths.