from pamda.pamda_error import pamda_error
import types

class pamda_utils(pamda_error):
    def hardRound(self, decimal_places, data):
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

    def safeDivide(self, numerator, denominator):
        """
        Function:

        - Forces division to work by enforcing a denominator of 1 if the provided denominator is zero

        Requires:

        - `numerator`:
            - Type: int | float
            - What: The numerator

        - `denominator`:
            - Type: int | float
            - What: The denominator

        Example:

        ```
        p.safeDivide(
            numerator=10,
            denominator=2
        ) #=> 5
        p.safeDivide(
            numerator=10,
            denominator=0
        ) #=> 10
        ```
        """
        if (
            not isinstance(numerator, (float, int)) or
            not isinstance(denominator, (float, int))
        ):
            self.exception('`safeDivide` can only be called on `float` or `int` objects')
        return numerator/denominator if denominator!=0 else numerator

    def safeDivideDefault(self, numerator, denominator, default_denominator=1):
        """
        Function:

        - Forces division to work by enforcing a non zero default denominator if the provided denominator is zero

        Requires:

        - `default_denominator`:
            - Type: int | float
            - What: A non zero denominator to use if denominator is zero
            - Default: 1

        - `numerator`:
            - Type: int | float
            - What: The numerator

        - `denominator`:
            - Type: int | float
            - What: The denominator

        Example:

        ```
        p.safeDivideDefault(
            default_denominator=2,
            numerator=10,
            denominator=5
        ) #=> 2
        p.safeDivideDefault(
            default_denominator=2,
            numerator=10,
            denominator=0
        ) #=> 5
        ```
        """
        if (
            not isinstance(numerator, (float, int)) or
            not isinstance(denominator, (float, int)) or
            not isinstance(default_denominator, (float, int))
        ):
            self.exception('`safeDivideDefault` can only be called on `float` or `int` objects')
        if default_denominator==0:
            self.exception('`safeDivideDefault` `default_denominator` can not be 0')
        return numerator/denominator if denominator!=0 else numerator/default_denominator

    def getMethods(self, object):
        """
        Function:

        - Returns the callable methods of a class (dunder-excluded) as a list of strs

        Requires:

        - `object`:
            - Type: any
            - What: Any python object
            - Default: 1

        Example:

        ```
        class MyClass:
            def A(self):
                pass

            def B(self):
                pass


        p.getMethods(MyClass) #=> ['A', 'B']
        ```
        """
        return [fn for fn in dir(object) if callable(getattr(object, fn)) and not fn.startswith("__")]

class curry_class(pamda_utils):
    def __init__(self, fn, *args, isThunk=False, **kwargs):
        self.fn=fn
        self.args=args
        self.kwargs=kwargs
        self.isThunk=isThunk
        self.fnArity=self.getFnArity()
        self.arity=self.getArity(args, kwargs)

    def __call__(self, *args, **kwargs):
        new_args=self.args+args
        new_kwargs=dict(**self.kwargs, **kwargs)
        self.arity=self.getArity(new_args, new_kwargs)
        if self.arity<0:
            self.exception('Too many arguments were supplied')
        if self.arity==0:
            if not self.isThunk:
                return self.fn(*new_args, **new_kwargs)
            if len(args)+len(kwargs)==0:
                return self.fn(*new_args, **new_kwargs)
        return curry_class(self.fn, *new_args, isThunk=self.isThunk, **new_kwargs)

    def getArity(self, args, kwargs):
        return self.fnArity-(len(args) + len(kwargs))

    def getFnArity(self):
        if not isinstance(self.fn, (types.MethodType, types.FunctionType)):
            self.exception('A non function was passed as a function and does not have any arity. See the stack trace above for more information.')
        extra_method_input_count=1 if isinstance(self.fn, types.MethodType) else 0
        return self.fn.__code__.co_argcount-extra_method_input_count

    def thunkify(self):
        self.isThunk=True
        return self
