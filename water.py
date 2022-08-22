import math
from dataclasses import dataclass
from typing import Callable

import scipy.integrate as integrate

from utilities import exponential

@dataclass
class Groundwater:
    active: bool = True
    deficit: float = 0.0 # state
    max_deficit: float = math.inf
    sustainable_yield: float = 0.0
    pump_cost_function: Callable[[float], float] = exponential(base=1, r=0)
    
    def pump(self, q: float):
        self.deficit = self.deficit + q if self.active else 0
    
    def recharge(self, excess_yield: float = 0):
        self.deficit -= self.sustainable_yield + excess_yield if self.active else 0
        
    def bid(self, q: float):
        if self.active and q > 0:
            qs = min(q, -self.deficit) if self.deficit < 0 else 0
            qp = 0 if qs > q else min(q - qs, self.max_deficit - self.deficit)
            cost = self.pump_cost_function(0) * qs + integrate.quad(lambda x: self.pump_cost_function(x), max(self.deficit, 0), self.deficit + qp)[0]
            return qs+qp, cost
        else:
            return 0, 0

@dataclass
class Surfacewater:
    available: float = 0
    unit_cost: float = 1

    def supply(self, q: float):      
        self.available = q

    def deliver(self, q: float):
        self.available -= q

    def bid(self, q: float):
        sw = self.available if self.available < q else q
        return sw, self.unit_cost * sw

def demand(ETo: float, kc: float) -> float:
    '''
    Computes water demand (ETc) for crop c.
    
    Arguments:
        ETo: float - reference ET.
        kc: float - crop coefficient.
    '''
    return ETo * kc

def bid(d: float, p: float, s: Surfacewater, g: Groundwater):
    D = d - p
    if D > 0:
        sw = s.bid(D)
        gw = D - sw[0] if sw[0] < D else 0
        return sw, g.bid(gw)
    else:
        return (0,0), (0,0)