# wrapper function to allow either default arguments
# or user-specified named arguments.
from plato.core.decorator.impl.column import Column as ColumnImpl

def column(function=None, automatically_call=False, data_context=False):
    if function:
        return ColumnImpl(function, automatically_call, data_context)
    else:        
        def column_wrapper(function):
            return ColumnImpl(function, automatically_call, data_context)
        return column_wrapper
