import time
from pathlib import Path
from enum import IntEnum
import os

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = Path(ROOT_DIR/ "logs")
LOG_FILES = ['nfa.log','dfa.log', 'general.log']
class LogMessage(IntEnum):
    NFA = 0
    DFA = 1
    GENERAL = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

class StateViolation(Exception):
    pass

class AlphabetViolation(ValueError):
    pass

class SetFormatError(ValueError):
    pass
    

def powerset(set):
    """
    Returns all subsets of a set by recursively yielding (iteratively returning) the each item in addition to each
    other item in the set iteratively within the helper function, then returning the entire set as a whole
    in the outer function
    """

    # the recursive helper function which yields (a recursive passing of data) all combinatiions of
    # subsets
    
    def helper(set):
        if len(set) <= 1:
            yield set
            yield []
        else:
            for item in helper(set[1:]):
                yield [set[0]]+item
                yield item

    # return the powerset in list format
    return [item for item in helper(set)]
    

"""
function used for logging, not neccesary for using the rest of the program, only for testing
"""
def log(message, type = LogMessage.GENERAL, file = None):
    if file is None:
        filename = Path(LOGS_DIR / LOG_FILES[type])
    else:
        filename = Path(LOGS_DIR / file)
    try:
        with open (filename, 'a') as f:
            f.write(str(time.strftime("%H:%M:%S:")) + '\t\t\t\t' + str(message) +'\n')
    except Exception as e:
        path = Path(LOGS_DIR / LOG_FILES[LogMessage.GENERAL])
        try:
            with open (path, 'a') as p:
                p.write(str(time.strftime("%H:%M:%S:")) + '\t\t\t\t' + str(message) +'\n')
        except Exception as e:
            print(e)
    

