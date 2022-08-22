import numpy as np
from typing import List, Callable

def exponential(base: float = 1, r: float = 0) -> Callable[[float], float]:
    '''
    Returns an exponential function with a base of 1 and growth rate of r.
    '''
    def f(x: float):
        return base * (1 + r) ** x
    return f

def unit_sigmoid(k: float = 1) -> Callable[[float], float]:
    '''
    Returns a sigmoid (logistic) function on the domain and range of [0, 1].
    
    Arguments:
        k: float - controls shape (~"steepness") of function.
    '''
    def f(x: float):
        return 0 if x <= 0 else 1 / (1 + ((1 / x) - 1)**k) if x < 1 else 1
    return f

def expected_value(ts: List[float], d: float = 0) -> float:
    '''
    Returns the expected value of time series.
    
    Arguments:
        ts: List[float] - a timeseries (or any array of values for d = {0, 1}).
        d: float - a constant rate of depreciation of information from k, k - 1 for k in len(ts).

    Notes:
        [1] The arithematic mean is return for d = 0 (no discounting of information).
        [2] The last value in ts is returned for d = 1 (perfect discounting of information).
    '''
    def partial_weight(t: int):
        return (1 - d)**t
    f = np.vectorize(partial_weight)
    w = f(np.arange(len(ts) - 1, -1, -1))
    return np.dot(w / np.sum(w), ts)