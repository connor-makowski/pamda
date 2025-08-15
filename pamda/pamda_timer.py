import time
from functools import update_wrapper
from type_enforced.utils import Partial


class PamdaTimer:
    def __init__(
        self,
        __fn__,
        units="ms",
        iterations=1,
        print_call=True,
        print_time_stats=False,
    ):
        """
        Function:

        Initialize a pamda_timer object.
        - Note: This object is used for bare minimum in script timing purposes.

        Required:

        - `fn`:
            - Type: function | method
            - What: The name of the process being timed

        Optional:

        - `units`:
            - Type: str
            - What: The units for the time measurement. Can be "s" (seconds), "ms" (milliseconds), or "us" (microseconds). Default is "ms".
        - `iterations`:
            - Type: int
            - What: The number of iterations to run the function when getting time statistics. Default is 1.
        - `print_call`:
            - Type: bool
            - What: Whether to print the function call time when this object is called. Default is True.
        - `print_time_stats`:
            - Type: bool
            - What: Whether to print a simple output line for get_time_stats after all iterations run. Default is False.
        """
        update_wrapper(self, __fn__)
        self.__fn__ = __fn__
        self.units = units
        self.iterations = iterations
        self.print_call = print_call
        self.print_time_stats = print_time_stats
        assert (
            isinstance(self.iterations, int) and self.iterations > 0
        ), "Iterations must be a positive integer."
        if units not in ["s", "ms", "us"]:
            raise ValueError("Invalid units. Use 's', 'ms', or 'us'.")
        if units == "s":
            self.__divisor__ = 1
        elif units == "ms":
            self.__divisor__ = 1000
        elif units == "us":
            self.__divisor__ = 1000000

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
        time_taken = time.time() - start
        if self.print_call:
            print(
                f"{self.__fn__.__qualname__}: {(time_taken * self.__divisor__):.4f}{self.units}"
            )
        return out

    def __repr__(self):
        return f"<timed {self.__fn__.__module__}.{self.__fn__.__qualname__} object at {hex(id(self))}>"

    def get_time_stats(self, *args, **kwargs):
        """
        Function:

        Get the time statistics of the function given the number of iterations (specified during initialization).

        Optional:

        - `args`:
            - Type: any
            - What: The arguments to pass to the function
        - `kwargs`:
            - Type: any
            - What: The keyword arguments to pass to the function

        Returns:
            - A dictionary containing the average, minimum, maximum, and total time taken by the function.
        """
        timing_history = []

        for _ in range(self.iterations):
            start = time.time()
            self.__fn__(*args, **kwargs)
            time_taken = time.time() - start
            timing_history.append(time_taken)

        avg_time = sum(timing_history) / len(timing_history)
        min_time = min(timing_history)
        max_time = max(timing_history)
        if self.iterations == 1:
            stdev_time = 0
        else:
            stdev_time = (
                sum((x - avg_time) ** 2 for x in timing_history)
                / len(timing_history)
            ) ** 0.5

        output = {
            "module": self.__fn__.__module__,
            "function": self.__fn__.__qualname__,
            "unit": self.units,
            "iterations": self.iterations,
            "avg": avg_time * self.__divisor__,
            "min": min_time * self.__divisor__,
            "max": max_time * self.__divisor__,
            "std": stdev_time * self.__divisor__,
        }
        if self.print_time_stats:
            print(
                f"{output['function']}: {output['avg']:.3f} ± {output['std']:.3f} {output['unit']} over {output['iterations']} iterations"
            )
        return output


def pamda_timer(
    fn, units="ms", iterations=1, print_call=True, print_time_stats=False
):
    """
    Function:
    Create a pamda_timer object.
    A wrapper function to create a pamda_timer object with the specified parameters.

    Optional:

    - `units`: str, the units for the time measurement (default is "ms")
    - `iterations`: int, the number of iterations to run the function when getting time statistics (default is 1)
    - `print_call`: bool, whether to print the function call time when this object is called (default is True)
    - `print_time_stats`: bool, whether to print the time statistics when get_time_stats is called (default is False)
    """
    return PamdaTimer(
        fn,
        units=units,
        iterations=iterations,
        print_call=print_call,
        print_time_stats=print_time_stats,
    )


pamda_timer = Partial(
    pamda_timer,
    units="ms",
    iterations=1,
    print_call=True,
    print_time_stats=False,
)
