from pamda.pamda_core import pamda_core

class pamda_core_curried:
    def __init__(self, pamda, *args, **kwargs):
        for method in pamda.getMethods(pamda):
            setattr(self, method, pamda.curry(getattr(pamda, method)))

pamda_uncurried=pamda_core()
pamda=pamda_core_curried(pamda=pamda_uncurried)
