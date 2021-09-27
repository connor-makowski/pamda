import types

class curry_fn:
    def __init__(self, __fn__, *__args__, __flips__=[], __isThunk__=False, **__kwargs__):
        self.__doc__=__fn__.__doc__
        self.__name__=__fn__.__name__+"_curried"
        self.__fn__=__fn__
        self.__args__=__args__
        self.__kwargs__=__kwargs__
        self.__isThunk__=__isThunk__
        self.__flips__=__flips__
        self.__fnArity__=self.__getFnArity__()
        self.__arity__=self.__getArity__(__args__, __kwargs__)

    def __call__(self, *args, **kwargs):
        new_args=self.__args__+args
        new_kwargs=dict(**self.__kwargs__, **kwargs)
        self.__arity__=self.__getArity__(new_args, new_kwargs)
        if self.__arity__<0:
            self.__exception__('Too many arguments were supplied')
        if self.__arity__==0:
            if len(self.__flips__)>0:
                new_args=self.__unflipArgs__(new_args)
            if (not self.__isThunk__) or (len(args)+len(kwargs)==0):
                return self.__fn__(*new_args, **new_kwargs)
        return curry_fn(self.__fn__, *new_args, __flips__=self.__flips__, __isThunk__=self.__isThunk__, **new_kwargs)

    def __repr__(self):
        return f"<curried {self.__fn__.__module__}.{self.__fn__.__qualname__} object at {hex(id(self))}>"

    def __getArity__(self, args, kwargs):
        return self.__fnArity__-(len(args) + len(kwargs))

    def __getFnArity__(self):
        if not isinstance(self.__fn__, (types.MethodType, types.FunctionType)):
            self.__exception__('A non function was passed as a function and does not have any arity. See the stack trace above for more information.')
        extra_method_input_count=1 if isinstance(self.__fn__, types.MethodType) else 0
        return self.__fn__.__code__.co_argcount-extra_method_input_count

    def thunkify(self):
        self.__isThunk__=True
        return self

    def flip(self):
        if self.__arity__<2:
            self.__exception__('To `flip` a function, it  must have an arity of at least 2 (take two or more inputs)')
        self.__flips__=[len(self.__args__)]+self.__flips__
        return self

    def __unflipArgs__(self, args):
        args=list(args)
        for flip in self.__flips__:
            arg=args.pop(flip+1)
            args.insert(flip, arg)
        return tuple(args)

    def __exception__(self, message, depth=0):
        pre_message=f"({self.__fn__.__module__}.{self.__fn__.__qualname__}_curried): "
        raise Exception(pre_message+message)
