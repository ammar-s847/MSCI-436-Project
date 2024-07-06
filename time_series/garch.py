import pandas as pd
import numpy as np
from types import Tuple
from arch import arch_model 
from arch.univariate import GARCHResults


def train_garch_model(data: pd.Series) -> GARCHResults: 
    '''Fits a GARCH model to the given data.''' 
    model = arch_model(data, vol='Garch', p=1, q=1) 
    result = model.fit(disp='off') 
    return result

def load_garch_model(ticker: str) -> GARCHResults:
    '''Retrieves a trained GARCH model from disk.'''
    with open(f'{ticker}_garch_model.pkl', 'rb') as pkl_file:
        model = GARCHResults.load(pkl_file)
    return model


