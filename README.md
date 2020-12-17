# COMP3900 Major Project | Binary Fuzzer
Developed by @Multifactored, @DionEarle, @jjamme, @mattimmanuel01

This program analyses and tests compiled binaries to determine if a possible vulnerability exists. It performs this through passing in malformed or abnormal input and testing if it crashes, before returning the malformed input used if a crash is made.

It currently supports binaries that take as input:
* Plaintext
* JSON
* XML 
* CSV

## Usage of the Project

Usage: `./fuzzer /path/to/binary /path/to/sampleinput`

## Contact
* Wisley Chau : multifactored@gmail.com
>add more here

## Brief Documentation

/binaries - Contains the sample binaries we tested the project on, separated by language.

/writeup - Contains the actual detailed documentation.

fuzzer - The main python program.
- type_checker.py - checks the type of the binary that's passed in, then redirects it to the appropriate handler
