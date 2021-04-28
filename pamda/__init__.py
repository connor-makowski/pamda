import sys
if sys.version_info[0] == 3:
    from pamda.pamda import pamda, pamdata, pamda_class, pamda_error
elif sys.version_info[0] < 3:
    from pamda import pamda, pamdata, pamda_class, pamda_error
