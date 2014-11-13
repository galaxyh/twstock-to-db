import math
import numpy as np
import pandas as pds

def moving_avg(data, window):
    ts = pds.Series(data)
    return pds.rolling_mean(ts, window)

if __name__ == '__main__':
    # Here is the test code
    data = np.arange(10, 101, 10)
    ma = moving_avg(data, 5)
    print ma