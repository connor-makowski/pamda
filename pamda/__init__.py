import sys
if sys.version_info[0] == 3:
    from pamda.pamda import pamda, pamda_uncurried
    from pamda.pamda_core import pamda_core
elif sys.version_info[0] < 3:
    from pamda import pamda, pamda_uncurried
    from pamda_core import pamda_core
