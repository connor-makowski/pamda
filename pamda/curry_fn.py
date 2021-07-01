from pamda.utils import error
import types

class curry_fn(error):
    def __init__(self, fn, *args, isThunk=False, **kwargs):
        self.__doc__=fn.__doc__
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
        return curry_fn(self.fn, *new_args, isThunk=self.isThunk, **new_kwargs)

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
