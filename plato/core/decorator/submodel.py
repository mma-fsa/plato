from plato.core.decorator.impl.submodel import SubModel as SubModelImpl

def submodel(factory_function=None, data_context=None):
    def submodel_wrapper(factory_function):
        return SubModelImpl(factory_function, data_context)
    return submodel_wrapper