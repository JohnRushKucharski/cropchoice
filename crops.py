import math
from enum import Enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Protocol

import utilities

def unit_production(max_production: float = 1, no_production_threshold: float = 0, fx: Callable[[float], float] = utilities.unit_sigmoid(k=1)):
    '''
    Returns a function that transforms a portion of demanded water supplied into units of production.
    
    Arguments:
        max_production: float - maximum units of production when water demands are met, 1 by default.
        no_production_threshold: float - a portion of water demand met below which production is zero, 0 by default.
        fx: Callable[[float], float] = function that transforms portion water to portion of maximum production, utilities.unit_sigmoid(k=1) by default.
    '''
    def f(x: float):
        '''
        Expects x is portion of demanded water on domain [0, 1].
        '''
        return 0 if x < no_production_threshold else fx(x) * max_production
    return f

class Names(Enum):
    '''
    Crop names + name for fallowed land.
    '''
    FALLOW = 0
    '''Fallowed land.'''
    ANNUAL = 1
    '''Generic name for annual crops (i.e. alfalfa).'''
    PERENNIAL = 2
    '''Generic name for perennial crops (i.e. almonds).'''

@dataclass
class UnitCost:
    startup_cost: float = 0
    non_water_cost: float = 1
    
class Crop(Protocol):
    name: str
    
    @staticmethod
    def water_demand(eto: float, kc: float) -> float:
        pass
    
    @abstractmethod
    def production(self, water: float) -> float:
        pass
    
    @abstractmethod
    def factor(self, r: float) -> float:
        pass
    
    @abstractmethod
    def mr(self, p: float, q: float, r: float) -> float:
        pass
    
    @abstractmethod
    def mc(self, new: bool, wc: float, r: float) -> float:
        pass
    
    @staticmethod
    @abstractmethod
    def npv(mr: float, mc: float) -> float:
        pass
    
@dataclass
class Perennial:
    name: str = Names.PERENNIAL.name
    unit_costs: UnitCost = UnitCost()
    production_fx: Callable[[float], float] = unit_production(max_production=1, no_production_threshold=0)
    life = math.inf
    
    @staticmethod
    def water_demand(eto: float, kc: float) -> float:
        '''
        Computes water demand (ETc) for crop c.
        
        Arguments:
            eto: float - reference ET.
            kc: float - crop coefficient.
        '''
        return eto * kc
    
    def production(self, water: float):
        return self.production_fx(water)
    
    def factor(self, r: float) -> float:
        return 1/r if math.isfinite(self.life) else (1 - (1 / (1 + r)**self.life)) / r

    def mr(self, p: float, q: float, r: float):
        return p * q * self.factor(r)
    
    def mc(self, new: bool, wc: float, r: float):
        annuity = (self.unit_costs.non_water_cost + wc) * self.factor(r)
        return self.unit_costs.startup_cost + annuity if new else annuity
    
    @staticmethod
    def npv(mr: float, mc: float):
        return mr - mc

@dataclass
class Annual:
    name: str = Names.ANNUAL.name
    unit_costs: UnitCost = UnitCost()
    production_fx: Callable[[float], float] = unit_production(max_production=1, no_production_threshold=0)
    
    @staticmethod
    def water_demand(eto: float, kc: float) -> float:
        '''
        Computes water demand (ETc) for crop c.
        
        Arguments:
            eto: float - reference ET.
            kc: float - crop coefficient.
        '''
        return eto * kc
    
    def production(self, water: float) -> float:
        return self.production_fx(water)
    
    def factor(self, r: float) -> float:
        return 1 / (1 + r)

    def mr(self, p: float, q: float, r: float) -> float:
        return p * q * self.factor(r)
    
    def mc(self, new: bool, wc: float, r: float) -> float:
        annuity = (self.unit_costs.non_water_cost + wc) * self.factor(r)
        return self.unit_costs.startup_cost + annuity if new else annuity
    
    @staticmethod
    def npv(mr: float, mc: float) -> float:
        return mr - mc
    
@dataclass
class Fallow:
    name: str = Names.FALLOW.name
    
    def water_demand(self, eto: float=0, kc: float=0) -> float:
        return 0
    
    def production(self, water: float=1) -> float:
        return 0
    
    def factor(self, r: float=0) -> float:
        return 0
    
    def mr(self, p:float=0, q:float=0, r:float=0) -> float:
        return 0
    
    def mc(self, new:bool=False, wc:float=0, r:float=0) -> float:
        return 0
    
    @staticmethod
    def npv(mr:float=0, mc:float=0) -> float:
        return 0