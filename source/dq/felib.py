import pandas as pd
import numpy as np
import pandas_ta as pdta


class FELib:
    """
    Simple Feature Engineering Library
    """

    @staticmethod
    def iif(condition, resultTrue, resultFalse):
        return np.where(condition, resultTrue, resultFalse)

    @staticmethod
    def llv(series, period):
        try:
            if type(series) == np.ndarray:
                series = pd.Series(series)
            series = series.fillna(0)
            result = series.rolling(period, min_periods=1).min()
            result = np.nan_to_num(result)
        except Exception as e:
            raise e
        return result

    @staticmethod
    def hhv(series, period):
        try:
            if type(series) == np.ndarray:
                series = pd.Series(series)
            # series = series.fillna(0)
            result = series.rolling(period, min_periods=1).max()
            result = np.nan_to_num(result)
        except Exception as e:
            raise e
        return result

    @staticmethod
    def ma(series, period):
        try:
            if type(series) == np.ndarray:
                series = pd.Series(series)
            series = series.fillna(0)
            result = series.rolling(period, min_periods=1).mean()
            result = np.nan_to_num(result)
        except Exception as e:
            raise e
        return result

    @staticmethod
    def stdev(series, period):
        try:
            if type(series) == np.ndarray:
                series = pd.Series(series)
            series = series.fillna(0)
            result = series.rolling(period, min_periods=1).std(skipna=True)
            result = np.nan_to_num(result)
        except Exception as e:
            raise e
        return result