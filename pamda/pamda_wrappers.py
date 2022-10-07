import types
from pamda.pamda_curry import curry_obj


def typed_curry_wrap(clsFnMethod):
    if isinstance(clsFnMethod, staticmethod):
        return staticmethod(curry_obj(clsFnMethod.__func__).typeEnforce())
    elif isinstance(clsFnMethod, classmethod):
        return classmethod(curry_obj(clsFnMethod.__func__).typeEnforce())
    elif isinstance(clsFnMethod, (types.FunctionType, types.MethodType)):
        return curry_obj(clsFnMethod).typeEnforce()
    else:
        for key, value in clsFnMethod.__dict__.items():
            if hasattr(value, "__call__") or isinstance(
                value, (classmethod, staticmethod)
            ):
                setattr(clsFnMethod, key, typed_curry_wrap(value))
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
