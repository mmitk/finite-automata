import util

try:
    raise util.stateViolation('ERROR')
except util.stateViolation as s:
    print(s)