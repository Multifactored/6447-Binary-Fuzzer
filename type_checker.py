import csv
import json
import xml.dom.minidom as XML


'''
# NOTE: This passes for non-CSV files...
# Given the sample input file, determines if it has the same format as a CSV file.
def checkCSV(sampleInput):
    try:
        # The Sniffer function reads through the file and checks to see if it is
        # a valid csv format.
        csv.Sniffer().sniff(sampleInput.read())

    # If an exception is raised, then this means it was not a valid csv format.
    except:
        print("Not a CSV file...")
        return False

    return True
'''

# NOTE: This uses the assumption that a CSV file has equal number of commas on each
# line, having more than 1 line and at least 1 comma.
# Given the sample input file, determines if it has the same format as a CSV file.
def checkCSV(sampleInput):
    sampleInput.seek(0)
    # First we read the file and split each line.
    lines = sampleInput.readlines()

    # We then count the number of times a comma appears on the first line.
    commas = lines[0].count(",")

    # We then check whether there is a comma on this line, as well as whether there
    # is only one line in the file.
    if commas == 0 or len(lines) == 1:
        print("Not a CSV file...")
        return False

    # If it passes the initial check, then we can read through each line of the file
    # and check the number of commas is equal for each line.
    for line in lines:
        if line.count(",") != commas:
            print("Not a CSV file...")
            return False

    return True

# Given the sample input file, determines if it has the same format as a JSON file.
def checkJSON(sampleInput):
    sampleInput.seek(0)
    try:
        # First we need to read the file and store its contents in a variable.
        fileContents = sampleInput.read().strip()

        # Then, the loads function attempts to decode the file's contents as
        # json format.
        json.loads(fileContents)

    # If an exception is raised, then it is not valid json format.
    except:
        print("Not a JSON file...")
        return False

    return True

# Given the sample input file, determines if it has the same format as a XML file.
def checkXML(sampleInput):
    sampleInput.seek(0)
    try:
        # Attempt to parse the file and see if it's XML
        XML.parseString(sampleInput.read().strip())
    except:
        print("Not an XML file...")
        return False

    return True