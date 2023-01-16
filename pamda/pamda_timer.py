from pamda.pamda_curry import curry_obj
from functools import update_wrapper
import time

class pamda_timer:
    def __init__(self, __fn__):
        """
        Function:

        Initialize a pamda_timer object. 
        - Note: This object is used for bare minimum in script timing purposes.

        Required:

        - `fn`:
            - Type: function | method
            - What: The name of the process being timed
        """
        if not __fn__.__dict__.get("__isCurried__"):
            __fn__ = curry_obj(__fn__)
        if __fn__.__arity__ != 0:
            raise Exception("The function being timed must have an arity of 0. Consider thunkifying the function first.")
        self.__fn__ = __fn__
        update_wrapper(self, __fn__)

    def __call__(self):
        """
        Function:

        Test the timer by running the function being timed.
        """
        start = time.time()
        out = self.__fn__()
        print(f"{self.__fn__.__qualname__}: {round(time.time() - start,4)}s")
        return out

    def __repr__(self):
        return f"<timed {self.__fn__.__module__}.{self.__fn__.__qualname__} object at {hex(id(self))}>"