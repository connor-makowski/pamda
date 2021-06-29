import sys
if sys.version_info[0] == 3:
    from pamda.pamda import pamda
    from pamda.pamda_curried import pamda_curried
    from pamda.pamdata import pamdata
    from pamda.pamda_error import pamda_error
    from pamda.pamda_utils import pamda_utils, curry_class
    from pamda.pamda_class import pamda_class
    from pamda.pamdata_class import pamdata_class
elif sys.version_info[0] < 3:
    from pamda import pamda
    from pamda_curried import pamda_curried
    from pamdata import pamdata
    from pamda_error import pamda_error
    from pamda_utils import pamda_utils, curry_class
    from pamda_class import pamda_class
    from pamdata_class import pamdata_class
