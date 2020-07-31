# === Script variables  ===
TIME_LIMIT = 10     # Default time limit

# === Imports ===
import pytest

import warnings

import json
import os
from pathlib import Path

import functions as fnc

from func_timeout import func_timeout as fto
from func_timeout.exceptions import FunctionTimedOut

from datetime import datetime

# === Debug function ===
def DEBUG(*args, **kwargs):
    """
    Debug function.
    """
    print(*args, **kwargs)


# === Test function ===
def get_cases(f, sep="---"): 
    """
    Extracts inputs and outputs for each test/verification case within f, where f is a folder.

    Params
    ======
    f: str
        The folder containing the cases to be extracted.
    sep: str
        The substring separating comments from the input from the output in each case file. 

    Returns 
    =======
    cases: []
        Array of dictionaries containing each case

        Each case is a dictionary with the following fields:
         - "filename": The name of the file
         - "comments": Any comments in the folder
         - "inputs": The inputs
         - "outputs": The expected outputs

    Raises
    ======
    AssertionError:
        If the given path is not a folder.
    """
    # Initialise path
    p = Path(f)

    # Assert that target folder is a folder
    assert p.is_dir()

    # List of cases in the folder
    cases = []

    # Loop through all cases within the folder
    for f in p.iterdir():

        # Open each case file
        with open(f) as fr:

            # Obtain the contents of the case file
            contents = fr.read()

            # The case files are structured such that it has COMMENTS, followed by the separator substring, followed by the INPUTS, followed by the separator substring, and finally followed by the OUTPUTS

            # Instantiate case dictionary
            c = {}

            # Separate the contents by the separator, and then clean each individual element of newline/whitespace
            contents = contents.split(sep)
            contents = [c.strip() for c in contents]

            # Populate dictionary
            c["filename"] = f.with_suffix("").name
            c["inputs"] = contents[0]
            c["outputs"] = contents[1]

            if len(contents) == 3:
                c["comments"] = contents[2]

            # Add dictionary to list of cases
            cases.append(c)

    # After all cases have been looped through, return cases
    return cases


def run_test(f, dcstr=[], dcix=[], raise_errors=True):
    """
    Runs the test required for all cases within the folder. Any cases within dcstr and dcix are ignored.

    Params
    ======
    f: str
        The name of the test folder.
    dcstr: []
        Array of strings. 

        If the element of dcstr is an exact match with any of the case file names, the case is ignored.
    dcix: []
        Array of integers.

        Less reliable 'ignore' method. This ignores the 0-indexed element of the collected cases. 
    raise_errors: bool
        Whether any errors gathered while testing the cases should be returned. If false, only whether a case succeeded or failed is returned.
    """
    # === Ensure that dcstr and dcix are lists ===
    # Check if dcstr is a list
    if type(dcstr) == type([]):

        # If it is a list, we identify if all elements are of type 'str'

        # Filter out all non-string types
        other_types = [type(x) for x in dcstr]
        other_types = list(set(other_types))
        other_types = list(filter(lambda x: x != type(""), other_types))

        # If there are non-string types, raise an exception
        if other_types:

            raise Exception(f"dcstr must be a list of strings. Elements of type {other_types} found.")

    # If it's not a list, check if it's a string
    elif type(dcstr) == type(""):

        # Set it to a list of string
        dcstr = [dcstr] 

    # If it is neither a string or a list, we reject it. 
    else: 

        raise Exception(f"dcstr must be a string or a list of strings, not a {str(type(dcstr))}.")

    # We do the same check for dcix
    if type(dcix) == type([]):

        # If it is a list, we identify if all elements are of type 'str'

        # Filter out all non-string types
        other_types = [type(x) for x in dcix]
        other_types = list(set(other_types))
        other_types = list(filter(lambda x: x != type(1), other_types))

        # If there are non-string types, raise an exception
        if other_types:

            raise Exception(f"dcstr must be a list of integers. Elements of type {other_types} found.")

    # If it's not a list, check if it's a string
    elif type(dcix) == type(1):

        # Set it to a list of string
        dcix = [dcix] 

    # If it is neither a string or a list, we reject it. 
    else: 

        raise Exception(f"dcix must be an integer or a list of integers, not a {str(type(dcix))}.")

    # === Get cases from the folder ===
    cases = None

    try: 
        # Obtain cases 
        cases = get_cases(f)
    
    except AssertionError:
        raise Exception(f"The path '{f}' is not a valid folder.")

    # Ensure there are cases to run through
    if not cases:
        raise Exception(f"There are no test cases in '{f}'.")

    # === Loop through each case ===
    for cx, c in enumerate(cases): 
        
        # If cx is in dcix, ignore this case
        # If the name of the case is in dcstr, we ignore the case
        if cx in dcix or c["filename"] in dcstr: 
            continue 

        # Print out test case
        print(f"({f}) test case {cx} '{c['filename']}': ", end="")

        # Instantiate fnc arguments
        fnc.set_inputs(c["inputs"])
        
        # Get start time
        start_time = datetime.now()

        # Run function
        try: 
            fto(
                TIME_LIMIT,
                fnc.main,
                (c["inputs"], )
            )

        # If the function times out, add it as an error
        except FunctionTimedOut as e:
            c["errors"] = e 

        # For any other exception, we also add it as an error
        # The reason we separate FunctionTimedOut from Exception is because FunctionTimedOut is not considered an Exception by the program
        except Exception as e:
            c["errors"] = e

        # Here, we check if there are errors
        if "errors" in c.keys():

            # If there are errors, print the error out
            print(c["errors"])

        else:

            # If there are no exceptions, we check that the answer is correct
            try: 

                assert "\n".join(fnc.fptr.get_answers()) == c["outputs"]

                print("Success")

            except Exception as e:
                
                # There are, as of now, no errors
                # We set the errors to the assertion error
                c["errors"] = e
                
                # Print the error
                print(e)

    # Finally, we raise all errors so py.test recognises that this test case failed
    for c in cases:
        if "errors" in c.keys():
            raise c["errors"]


# === Run test ===
def test_test_values(): 
    """
    Runs test on test values.
    """
    run_test("test_cases")


def test_ver_values(): 
    """
    Runs test on verification values.
    """
    run_test("verification_cases")