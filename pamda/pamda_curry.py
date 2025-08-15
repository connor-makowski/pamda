import types, threading, ctypes
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
        self.__get_fn_arg_default_keys__()

    def __call__(self, *args, **kwargs):
        new_args = self.__args__ + args
        new_kwargs = dict(**self.__kwargs__, **kwargs)
        # Create a comprehensive set of assigned variable names to determine arity
        assigned_vars = set(
            self.__fn_arg_default_keys__
            + self.__fn_arg_keys__[: len(new_args)]
            + list(new_kwargs.keys())
        )
        arity = self.__fnArity__ - len(assigned_vars)
        if arity < 0:
            self.__exception__("Too many arguments were supplied")
        elif arity == 0:
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

    def __get__(self, instance, owner):
        def bind(*args, **kwargs):
            if instance is not None and self.__arity__ == self.__fnArity__:
                return self.__call__(instance, *args, **kwargs)
            else:
                return self.__call__(*args, **kwargs)

        return bind

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

    def __get_fn_arg_default_keys__(self):
        """
        Get the default values of the passed function or method and store them in `self.__fn_defaults__`.
        """
        self.__fn_var_keys__ = list(self.__fn__.__code__.co_varnames)
        self.__fn_arg_keys__ = self.__fn_var_keys__[
            : self.__fn__.__code__.co_argcount
        ]
        if self.__fn__.__defaults__ is not None:
            self.__fn_arg_default_keys__ = self.__fn_arg_keys__[
                -len(self.__fn__.__defaults__) :
            ]
        else:
            self.__fn_arg_default_keys__ = []
        if self.__fn__.__kwdefaults__ is not None:
            self.__fn_arg_default_keys__.extend(
                list(self.__fn__.__kwdefaults__.keys())
            )

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

    def __exception__(self, message):
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
        self.__thread_completed__ = False
        self.__thread__ = threading.Thread(target=self)
        self.__thread__.setDaemon(daemon)
        self.__thread__.start()
        return self

    def asyncWait(self):
        if self.__thread__ == None:
            self.__exception__(
                f"To `asyncWait` a Function, it must be `asyncRun` first"
            )
        if not self.__thread_completed__:
            self.__thread__.join()
            self.__thread_completed__ = True
        return self.__thread_results__

    def asyncKill(self):
        if self.__thread__ == None:
            self.__exception__(
                f"To `asyncKill` a Function, it must be `asyncRun` first"
            )
        if self.__thread_completed__:
            return self.__thread_results__

        thread_id = self.__thread__.ident
        if thread_id is None:
            self.__exception__(
                f"Cannot `asyncKill` a Function that does not have a thread id"
            )

        # Use ctypes to set the async exception
        try:
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread_id), ctypes.py_object(SystemExit)
            )
        except:
            self.__exception__(
                f"Failed to `asyncKill`: Something failed when seting the Exit state for thread id ({thread_id})"
            )
        if res == 0:
            self.__exception__(
                f"Failed to `asyncKill`: Thread id not found ({thread_id})"
            )
        elif res == 1:
            # Success, thread killed join the thread to clean up resources
            self.__thread_completed__ = True
            self.__thread__.join()
            return self.__thread_results__
        elif res > 1:
            # Something is wrong, set it back to 0
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            self.__exception__(
                f"Failed to `asyncKill`: ctypes returned multiple results for thread id ({thread_id}). This should not happen. Returned thread state back to normal."
            )
