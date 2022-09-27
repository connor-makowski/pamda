import sys

if sys.version_info[0] == 3:
    from pamda.pamda import *
elif sys.version_info[0] < 3:
    from pamda import *
