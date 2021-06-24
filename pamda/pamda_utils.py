from pamda.pamda_error import pamda_error

class pamda_utils(pamda_error):
    def hardRound(self, data, decimal_places=0):
        """
        Function:

        - Rounds to a set number of decimal places regardless of floating point math in python

        Requires:

        - `data`:
            - Type: int | float
            - What: The number to round

        Optional:

        - `decimal_places`:
            - Type: int
            - What: The number of decimal places to round to
            - Default: 0
            - Notes: Negative numbers accepted (EG -1 rounds to the nearest 10)

        Example:

        ```
        data=12.345
        p.hardRound(
            data=data,
            decimal_places=1
        ) #=> 12.3
        p.hardRound(
            data=data,
            decimal_places=-1
        ) #=> 10

        ```
        """
        if not isinstance(data, (float, int)):
            self.exception('`hardRound` can only be called on `float` or `int` objects')
        return int(data*(10**decimal_places)+0.5)/(10**decimal_places)

    def safeDivide(self, numerator, denominator, default_denominator=1):
        """
        Function:

        - Forces division to work by enforcing a non zero default denominator if the provided denominator is zer

        Requires:

        - `numerator`:
            - Type: int | float
            - What: The numerator

        - `denominator`:
            - Type: int | float
            - What: The denominator

        Optional:

        - `default_denominator`:
            - Type: int | float
            - What: A non zero denominator to use if denominator is zero
            - Default: 1

        Example:

        ```
        data=12.345
        p.safeDivide(
            numerator=10,
            denominator=2
        ) #=> 5
        p.safeDivide(
            numerator=10,
            denominator=0,
            default_denominator=1
        ) #=> 10
        ```
        """
        if (
            not isinstance(numerator, (float, int)) or
            not isinstance(denominator, (float, int)) or
            not isinstance(default_denominator, (float, int))
        ):
            self.exception('`safeDivide` can only be called on `float` or `int` objects')
        if default_denominator==0:
            self.exception('`safeDivide` `default_denominator` can not be 0')
        return numerator/denominator if denominator!=0 else numerator/default_denominator
