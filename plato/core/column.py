# wrapper function to allow either default arguments
# or user-specified named arguments.
from plato.core.impl.column import Column as ColumnImpl

def column(function=None, automatically_call=False):
    if function:
        return ColumnImpl(function, automatically_call, None)
    else:        
        def column_wrapper(function):
            return ColumnImpl(function, automatically_call, None)
        return column_wrapper
