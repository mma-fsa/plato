import os
from openpyxl.workbook.workbook import Workbook
from plato.util.column_identifier import ColumnIdentifier
from openpyxl.writer import write_only

class XlsxOutput(object):

    def __init__(self, args):
        self.min_ts = int(args['timestep']['min'])
        self.max_ts = int(args['timestep']['max'])
        self.ts_range = range(self.min_ts, self.max_ts + 1)
        self.output_dir = args['output_dir']        
    
    def write(self, storage_repo):

        ordered_keys = storage_repo.keys()
        ordered_keys.sort()
        end_item = object()
        ordered_keys.append(end_item)
        state = None

        for columnIdentifier in ordered_keys:
              
            wb_name = None if columnIdentifier == end_item \
                else self.__get_wb_name(columnIdentifier)                          
            
            if state == None or wb_name != state.wb_name:
                if state != None:
                    self.__write_wb(state.wb_name, state.worksheet_data)                    
                if columnIdentifier == end_item:
                    break
                else:
                    state = XlsxOutputState(wb_name)            
               
            if state.setup_ts_col:
                self.__setup_ts_col(state.worksheet_data['projection'])
                state.setup_ts_col = False
            
            column_name = self.__get_column_name(columnIdentifier)
            column_data = storage_repo[columnIdentifier]            
            
            if self.__is_ts_col(columnIdentifier):
                ws_data = state.worksheet_data['projection']          
                self.__write_ts_col(column_name, column_data, ws_data)
            elif self.__is_scalar_col(columnIdentifier):
                ws_data = state.worksheet_data['scalars']
                self.__write_scalar_col(column_name, column_data,  ws_data)
            else:
                ws_data = []                
                state.worksheet_data[column_name] = ws_data
                args = columnIdentifier.metadata['args'].args                 
                self.__write_tbl(column_name, args, column_data, ws_data)
    
    def __write_wb(self, wb_name, worksheet_data):
                
        dest_wb = Workbook(write_only=True)
                
        for ws_name, ws_data in worksheet_data.iteritems():
            if ws_data == []:
                continue
            
            ws = dest_wb.create_sheet(title=ws_name)            
            ws_data_transposed = zip(*ws_data)
            for row in ws_data_transposed:
                ws.append(row)
        
        dest_wb.save(os.path.join(self.output_dir, wb_name))
        
    def __setup_ts_col(self, ws_data):
        ws_data.append(['time'] + self.ts_range)        
    
    def __write_ts_col(self, name, data, dest):
        
        def create_column_value_fn(data):
            def inner_fn(key):
                try: return data[(key,)]
                except KeyError: return None            
            return inner_fn
        
        # some keys may not exist, create wrapper fn to handle that case
        fn = create_column_value_fn(data)
        
        # ensure that keys are in order
        dest.append([name] + map(fn, self.ts_range))
    
    def __write_scalar_col(self, name, data, dest):
        if dest == []: dest.extend([[], []])                             
        dest[0].append(name)
        dest[1].append(data.values()[0])
    
    def __write_tbl(self, name, args, data, dest):
        keys = data.keys()        
        arg_cols = zip(*keys)
        val_col = map(lambda k: data[k], keys)
        
        i = 1
        for col in arg_cols:
            dest.append([args[i]] + list(col))
            i += 1
            
        dest.append([name] + list(val_col))
                
    def __get_wb_name(self, columnIdentifier):
        return columnIdentifier[0:columnIdentifier.find('#')] + '.xlsx'
    
    def __is_ts_col(self, key):
        return key.metadata['args'].args == ['self', 't']
    
    def __is_scalar_col(self, key):
        return key.metadata['args'].args == ['self']
    
    def __get_column_name(self, columnIdentifier):
        return columnIdentifier[columnIdentifier.find('#') + 1:]
    
    
class XlsxOutputState(object):
    
    def __init__(self, wb_name):
        self.wb_name = wb_name
        self.worksheet_data = {'projection' : [], 'scalars':[]}
        self.setup_ts_col = True
    
    
class FakeArgs(object):
    
    def __init__(self, args):
        self.__args = args
    
    @property
    def args(self):
        return self.__args

if __name__ == "__main__":

    fake_scalar_args = FakeArgs(['self'])
    fake_column_args = FakeArgs(['self', 't'])
    fake_table_args = FakeArgs(['self', 't', 's'])
    
    scalar_column = ColumnIdentifier('model1#scalar_column', None, 
                                     {'args': fake_scalar_args})
    
    col_1 = ColumnIdentifier('model1#col_1', None, {'args':fake_column_args})
    col_2 = ColumnIdentifier('model1#col_2', None, {'args':fake_column_args})
    col_3 = ColumnIdentifier('model1#col_3', None, {'args':fake_column_args})
    col_4 = ColumnIdentifier('model1#col_4', None, {'args':fake_column_args})
    
    tab_1 = ColumnIdentifier('model1#tbl_1', None, {'args':fake_table_args})
    tab_2 = ColumnIdentifier('model1#tbl_2', None, {'args':fake_table_args})
    
    col_11 = ColumnIdentifier('model2#col_1', None, {'args':fake_column_args})
    col_12 = ColumnIdentifier('model2#col_2', None, {'args':fake_column_args})
    col_13 = ColumnIdentifier('model3#col_3', None, {'args':fake_column_args})
    col_14 = ColumnIdentifier('model4#col_4', None, {'args':fake_column_args})
    
    tab_11 = ColumnIdentifier('model2#tbl_1', None, {'args':fake_table_args})
    tab_12 = ColumnIdentifier('model2#tbl_2', None, {'args':fake_table_args})
        
    storage_repo = {
        scalar_column: {tuple(): 100},
        col_1: {(1,): 100, (2,): 200},
        col_2: {(1,): 200, (2,): 300, (3,): 400},
        col_3: {(1,): 0},
        col_4: {},
        tab_1: {(1,2): 300, (3,4): 500},
        tab_2: {(5,7): 800, (1,1): 500, (9,9):1000},
        col_11: {(1,): 100, (2,): 200},
        col_12: {(1,): 200, (2,): 300, (3,): 400},
        col_13: {(1,): 0},
        col_14: {},
        tab_11: {(1,2): 300, (3,4): 500},
        tab_12: {(5,7): 800, (1,1): 500, (9,9):1000},
    }
    
    args = {'timestep': {'min':0, 'max':5}, 'output_dir':'/home/mike/Documents/test'}
    
    XlsxOutput(args).write(storage_repo)
             
    