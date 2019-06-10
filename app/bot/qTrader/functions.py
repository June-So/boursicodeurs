import numpy as np
import math
from app.utils.fxcmManager import connect_fxcm
# prints formatted price
def formatPrice(n):
    return ("- " if n < 0 else "")+ "{0:.2f}".format(abs(n)) + (" pips") 

# returns the vector containing stock data from a fixed file
def getStockDataVec(key):
    vec = []
    lines = open("data/" + key, "r").read().splitlines()

    for line in lines[1:]:
        vec.append(float(line.split(",")[5]))

    return vec

def getLastCotation(instrument, period, window_size):
    
    instrument = instrument.upper()
    #period = period.upper()

    period = period.lower()
    con_fxcmpy = connect_fxcm()

    df = con_fxcmpy.get_candles(instrument, period=period, number=window_size)
    df.head()
    return df


def getLastCotationVect(instrument, period, window_size, col):
    
    df = getLastCotation(instrument, period, window_size)
    vec = df[col].values.tolist()
        
    return vec


# returns the sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# returns an an n-day state representation ending at time t
def getState(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))

    return np.array([res])
