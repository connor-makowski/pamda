from pamda.pamda_core import pamda_core

class pamda_core_curried:
    def __init__(self, pamda, *args, **kwargs):
        no_curry=['read_csv','read_json','write_csv','write_json', 'warn', 'vprint', 'exception']
        for method in pamda.getMethods(pamda):
            if method in no_curry:
                setattr(self, method, getattr(pamda, method))
            else:
                setattr(self, method, pamda.curry(getattr(pamda, method)))


pamda_uncurried=pamda_core()
pamda=pamda_core_curried(pamda=pamda_uncurried)
