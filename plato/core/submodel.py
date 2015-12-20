from plato.core.impl.submodel import SubModel as SubModelImpl

def submodel(factory_function=None, data_context_property=None):
    if factory_function:
        return SubModelImpl(factory_function, data_context_property)
    else:
        def submodel_wrapper(factory_function):
            return SubModelImpl(factory_function, data_context_property)

