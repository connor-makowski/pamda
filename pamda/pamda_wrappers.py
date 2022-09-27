import types
from pamda.pamda_curry import curry_obj


def curry_wrap(clsFnMethod):
    if isinstance(clsFnMethod, staticmethod):
        return staticmethod(curry_obj(clsFnMethod.__func__))
    elif isinstance(clsFnMethod, classmethod):
        return classmethod(curry_obj(clsFnMethod.__func__))
    elif isinstance(clsFnMethod, (types.FunctionType, types.MethodType)):
        return curry_obj(clsFnMethod)
    else:
        for key, value in clsFnMethod.__dict__.items():
            if hasattr(value, "__call__") or isinstance(
                value, (classmethod, staticmethod)
            ):
                setattr(clsFnMethod, key, curry_wrap(value))
        return clsFnMethod


def staticmethod_wrap(clsFnMethod):
    if isinstance(clsFnMethod, (types.FunctionType, types.MethodType)):
        return staticmethod(clsFnMethod)
    else:
        for key, value in clsFnMethod.__dict__.items():
            if hasattr(value, "__call__"):
                setattr(clsFnMethod, key, staticmethod_wrap(value))
        return clsFnMethod


def classmethod_wrap(clsFnMethod):
    if isinstance(clsFnMethod, (types.FunctionType, types.MethodType)):
        return classmethod(clsFnMethod)
    else:
        for key, value in clsFnMethod.__dict__.items():
            if hasattr(value, "__call__"):
                setattr(clsFnMethod, key, classmethod_wrap(value))
        return clsFnMethod
