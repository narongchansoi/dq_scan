import os
import pandas as pd
import numpy as np


class BaseScanner:
    
    def __init__(self, symbols):
        self.symbols = symbols

    @staticmethod
    def load_data(dataset_path='../datasets/SET'
                    , columns_master=['DATETIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']
                    , datetime_format='%Y%m%d'):
        symbols = {} # key is symbol name, value is dataframe  
        
        with os.scandir(dataset_path) as entries:
            for entry in entries:
                if '.csv' in entry.name:
                    data_symbol = pd.read_csv(f"{dataset_path}/{entry.name}")

                    if 'Ticker' in data_symbol.columns:
                        data_symbol.drop(['Ticker'], axis=1, inplace=True)

                    if data_symbol.columns[-1].upper() != 'VOLUME':
                        columns_master.remove('VOLUME')

                    data_symbol.columns = columns_master
                    data_symbol['DATETIME'] = pd.to_datetime(data_symbol['DATETIME'])
                    symbols[entry.name.replace('.csv', '')] = data_symbol
        
        return symbols

    def add_indi(self):
        def create_indi(symbol_name, dataset):
            """
            Sample code:

            dataset['MA1'] = pdta.sma(dataset['CLOSE'], 10)
            dataset['MA2'] = pdta.wma(dataset['CLOSE'], 50)
            dataset['MA3'] = pdta.ema(dataset['CLOSE'], 200)
            dataset['RSI_S'] = pdta.rsi(dataset['CLOSE'], 10)
            dataset['RSI_M'] = pdta.ema( pdta.rsi(dataset['CLOSE'], 28), 10 )
            df_macd_s = pdta.macd(dataset['CLOSE'], 12, 26, 9)
            dataset['MACD_S'] = df_macd_s.iloc[:, 0]
            dataset['MACD_HIST_S'] = df_macd_s.iloc[:, 1]
            dataset['MACD_SIGNAL_S'] = df_macd_s.iloc[:, 2]
            """
            
            dataset.fillna(0.0, inplace=True) # fill ค่า NaN ด้วยค่า 0.0
    
        #==============================================================================
        for symbol_name in self.symbols.keys():
            create_indi(symbol_name, self.symbols[symbol_name])
    
    def eval_condition(self, symbol_name, dataset):
        result = False
        predict_result = None
        """
        Sample code:
        
        predict_result = np.where((dataset.MA1 > dataset.MA2)
                                 , 1, 0)
        """
        if predict_result[-1] == 1:
            result = True

        return result

    def scan(self, info=False):
        if len(self.symbols) == 0:
            raise Exception('symbols has not been initialized')
        
        scan_results = []

        for symbol_name in self.symbols.keys():
            result = self.eval_condition(symbol_name, self.symbols[symbol_name])
            scan_results.append({'SYMBOL': symbol_name, 'SCAN_RESULT': result})
            
        if info == True:
            first_df = list(self.symbols.values())[0]
            all_columns = first_df.columns
            last_col_index = 0
            if 'VOLUME' in all_columns:
                last_col_index = list(all_columns).index('VOLUME')
            else:
                last_col_index = list(all_columns).index('CLOSE')
            
            # convert scanned results to dataframe
            symbol_columns = ['SYMBOL', 'SCAN_RESULT']
            for col_index in range(last_col_index + 1, len(all_columns)):
                symbol_columns.append(all_columns[col_index])

            df_result = pd.DataFrame(scan_results, columns=symbol_columns)

            start_col_idx = last_col_index + 1 #len(columns_master)
            end_col_idx = len(first_df.columns)

            i = 0
            for symbol in scan_results:
                df_result.iloc[i, 2:len(df_result.columns)] = self.symbols[symbol['SYMBOL']].iloc[-1, start_col_idx:end_col_idx]
                i += 1
                
        else:
            df_result = pd.DataFrame(scan_results)
            
        return df_result
        