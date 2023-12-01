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
        self.__fn__ = __fn__

    def __call__(self, *args, **kwargs):
        """
        Function:

        Test the function processing time.

        Optional:

        - `args`:
            - Type: any
            - What: The arguments to pass to the function
        - `kwargs`:
            - Type: any
            - What: The keyword arguments to pass to the function
        """
        start = time.time()
        out = self.__fn__(*args, **kwargs)
        print(f"{self.__fn__.__qualname__}: {round(time.time() - start,4)}s")
        return out

    def __repr__(self):
        return f"<timed {self.__fn__.__module__}.{self.__fn__.__qualname__} object at {hex(id(self))}>"
