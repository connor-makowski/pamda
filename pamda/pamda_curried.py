from pamda.pamda_class import pamda_class

class pamda_curried_wrapper_class:
    def __init__(self, pamda, *args, **kwargs):
        for method in pamda.getMethods(pamda):
            setattr(self, method, pamda.curry(getattr(pamda, method)))

pamda_curried=pamda_curried_wrapper_class(pamda=pamda_class())
