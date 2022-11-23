import types, threading
from functools import update_wrapper
import type_enforced


class curry_obj:
    def __init__(
        self,
        __fn__,
        *__args__,
        __flips__=[],
        __fnExecute__=None,
        __isThunk__=False,
        __isTypeEnforced__=False,
        **__kwargs__,
    ):
        update_wrapper(self, __fn__)
        self.__fn__ = __fn__
        self.__fnExecute__ = (
            __fnExecute__ if __fnExecute__ is not None else __fn__
        )
        self.__args__ = __args__
        self.__kwargs__ = __kwargs__
        self.__isCurried__ = True
        self.__isThunk__ = __isThunk__
        self.__isTypeEnforced__ = __isTypeEnforced__
        self.__flips__ = __flips__
        self.__fnArity__ = self.__getFnArity__()
        self.__arity__ = self.__getArity__(__args__, __kwargs__)
        self.__thread__ = None
        self.__thread_results__ = None

    def __call__(self, *args, **kwargs):
        new_args = self.__args__ + args
        new_kwargs = dict(**self.__kwargs__, **kwargs)
        self.__arity__ = self.__getArity__(new_args, new_kwargs)
        if self.__arity__ < 0:
            self.__exception__("Too many arguments were supplied")
        if self.__arity__ == 0:
            if len(self.__flips__) > 0:
                new_args = self.__unflipArgs__(new_args)
            if (not self.__isThunk__) or (len(args) + len(kwargs) == 0):
                results = self.__fnExecute__(*new_args, **new_kwargs)
                if self.__thread__ != None:
                    self.__thread_results__ = results
                return results
        return curry_obj(
            self.__fn__,
            *new_args,
            __flips__=self.__flips__,
            __isThunk__=self.__isThunk__,
            __isTypeEnforced__=self.__isTypeEnforced__,
            __fnExecute__=self.__fnExecute__,
            **new_kwargs,
        )

    def __repr__(self):
        return f"<curried {self.__fn__.__module__}.{self.__fn__.__qualname__} object at {hex(id(self))}>"

    def __getArity__(self, args, kwargs):
        return self.__fnArity__ - (len(args) + len(kwargs))

    def __getFnArity__(self):
        if not isinstance(self.__fn__, (types.MethodType, types.FunctionType)):
            self.__exception__(
                "A non function was passed as a function and does not have any arity. See the stack trace above for more information."
            )
        extra_method_input_count = (
            1 if isinstance(self.__fn__, (types.MethodType)) else 0
        )
        return self.__fn__.__code__.co_argcount - extra_method_input_count

    def thunkify(self):
        self.__isThunk__ = True
        return self

    def flip(self):
        if self.__arity__ < 2:
            self.__exception__(
                "To `flip` a function, it  must have an arity of at least 2 (take two or more inputs)"
            )
        self.__flips__ = [len(self.__args__)] + self.__flips__
        return self

    def __unflipArgs__(self, args):
        args = list(args)
        for flip in self.__flips__:
            arg = args.pop(flip + 1)
            args.insert(flip, arg)
        return tuple(args)

    def __exception__(self, message, depth=0):
        pre_message = (
            f"({self.__fn__.__module__}.{self.__fn__.__qualname__}_curried): "
        )
        raise Exception(pre_message + message)

    def typeEnforce(self):
        if not self.__isTypeEnforced__:
            self.__fnExecute__ = type_enforced.Enforcer(self.__fnExecute__)
            self.__isTypeEnforced__ = True
        return self

    def asyncRun(self, daemon=False):
        if not self.__isThunk__ and self.__arity__ == 0:
            self.__exception__(
                f"To `asyncRun` a Function, it must be a thunk with arity 0"
            )
        if self.__thread__ is not None:
            self.__exception__(
                "`asyncRun` has already been executed on this thunk"
            )
        self.__thread__ = threading.Thread(target=self)
        self.__thread__.setDaemon(daemon)
        self.__thread__.start()
        return self

    def asyncWait(self):
        if self.__thread__ == None:
            self.__exception__(
                f"To `asyncWait` a Function, it must be `asyncRun` first"
            )
        self.__thread__.join()
        return self.__thread_results__
