import pandas as pd
import numpy as np
import pandas_ta as pdta

from dq.base_scanner import BaseScanner


class MyDailyScanner(BaseScanner):

    def add_indi(self):
        
        def create_indi(symbol_name, dataset):

            # SMA
            dataset['MA1'] = pdta.sma(dataset['CLOSE'], 10)

            # WMA
            dataset['MA2'] = pdta.wma(dataset['CLOSE'], 50)

            # EMA
            dataset['MA3'] = pdta.ema(dataset['CLOSE'], 200)

            # RSI
            dataset['RSI_S'] = pdta.rsi(dataset['CLOSE'], 10)
            dataset['RSI_M'] = pdta.ema( pdta.rsi(dataset['CLOSE'], 28), 10 )

            # MACD
            df_macd_s = pdta.macd(dataset['CLOSE'], 12, 26, 9)
            dataset['MACD_S'] = df_macd_s.iloc[:, 0]
            dataset['MACD_HIST_S'] = df_macd_s.iloc[:, 1]
            dataset['MACD_SIGNAL_S'] = df_macd_s.iloc[:, 2]

            # ATR
            dataset['ATR'] = pdta.atr(dataset['HIGH']
                                      , dataset['LOW']
                                      , dataset['CLOSE']
                                      , 20)

            # NATR (Normalized Average True Range)
            dataset['NATR'] = pdta.natr(dataset['HIGH']
                                      , dataset['LOW']
                                      , dataset['CLOSE']
                                      , 20)
            dataset['NATR'] = dataset['NATR']

            # Slow Stochastics
            df_slow_s = pdta.stoch(dataset['HIGH']
                                   , dataset['LOW']
                                   , dataset['CLOSE']
                                   , 9, 3, 3, 'wma')
            dataset['STOCHK_S'] = df_slow_s.iloc[:, 0]
            dataset['STOCHD_S'] = df_slow_s.iloc[:, 1]

            # Slow Stochastics
            df_slow_m = pdta.stoch(dataset['HIGH']
                                   , dataset['LOW']
                                   , dataset['CLOSE']
                                   , 36, 12, 12, 'wma')
            dataset['STOCHK_M'] = df_slow_m.iloc[:, 0]
            dataset['STOCHD_M'] = df_slow_m.iloc[:, 1]

            dataset.fillna(0.0, inplace=True) # fill ค่า NaN ด้วยค่า 0.0
    
        #==============================================================================
        for symbol_name in self.symbols.keys():
            create_indi(symbol_name, self.symbols[symbol_name])

            
    def eval_condition(self, symbol_name, dataset):
        result = False

        predict_result = np.where((dataset.RSI_S > 45)
                                 , 1, 0)
        if predict_result[-1] == 1:
            result = True

        return result

