from copy import deepcopy
from typing import Protocol
from dataclasses import dataclass, field

import numpy as np

import water
import crops
import system

def crop_cycle(s: water.Surfacewater, g: water.Groundwater, crop: crops.Crop, new: bool, inputs: np.ndarray):
    demand = crop.water_demand(eto=inputs[0], kc=inputs[1])
    surface, ground = water.bid(d=demand, p=inputs[2], s=s, g=g)
    portion_water = (surface[0] + ground[0] + inputs[2]) / demand if 0 < demand < 1 else 1
    marginal_revenue = crop.mr(p=inputs[3], q=crop.production(portion_water), r=inputs[4])
    marginal_cost = crop.mc(new=new, wc=surface[1] + ground[1], r=inputs[4])
    return np.array([demand, surface[0], ground[0], inputs[2], marginal_revenue, marginal_cost, crop.npv(marginal_revenue, marginal_cost)])
    
# def central_planner(resources: system.CentralPlanner, inputs: np.ndarray):
#     '''
#     This will loop over each unit of land committing it to production of the highest npv crop, given the available water and other factors.
    
#     Arguments:
#         inputs: np.ndarray[shape=(assets x [ETo, kc, precip, price, discount_rate]), dtype=float]
#     Returns:
#         outputs: np.ndarray[shape=(total_area x [id, demand, sw, gw, precip, mr, mc, npv]), dtype=float]
#     '''
#     outputs = np.zeros((resources.total_area(), 8)) # area x [id, d, sw, gw, p, mr, mc, npv]
#     for n in range(0, resources.total_area()):
#         # choices: shape = assets x [id, demand, sw, gw, precip, mr, mc, npv] 
#         choices = np.zeros((len(resources.assets), 8))
#         for c in range(0, len(resources.assets)):
#             d = water.demand(ETo=inputs[c,0], kc=inputs[c,1])                         # demand
#             s, g = water.bid(d=d, p=inputs[c,2], s=resources.S, g=resources.G)  # surface and groundwater quantities and prices
#             portion_water = (s[0] + g[0] + inputs[c,2]) / d if 0 < d < 1 else 1       # 1 if demand = 0 or precip > demand, 
#             new = True if resources.portfolio[c] < np.sum(outputs[:,0]) else False  # new if new_area for crop c
#             mr = resources.assets[c].mr(p=inputs[c,3], q=resources.assets[c].production_fx(portion_water), r=inputs[c,4])
#             mc = resources.assets[c].mc(new=new, wc=s[1]+g[1], r=inputs[c,4])
#             nb = resources.assets[c].npv(mr=mr, mc=mc)
#             choices[c,:] = np.array([c, d, s[0], g[0], inputs[c,2], mr, mc, nb])
#         maxnpv = choices[:,7].max()
#         if maxnpv <= 0:
#             fallow = resources.id(name=crops.Names.FALLOW.name)
#             outputs[n,:] = choices[fallow,:]
#         else:
#             maxes = choices[choices[:,7] == maxnpv]
#             if maxes.shape[0] > 1:
#                 np.random.shuffle(maxes)
#                 maxes = maxes[0,:]
#             outputs[n,:] = maxes
#     return outputs
        
        


    # def update_portfolio(self, surfacewater: float, inputs: np.ndarray):
    #     '''
    #     q: float ~ surfacewater availability
    #     inputs: np.ndarray ~ shape = (id x [eto, kc, p, price, r])  
    #     '''
    #     cp = deepcopy(self) # plan
    #     cp.S.supply(surfacewater) # plan  
    #     outputs = np.zeros((self.total_area(), 7)) # area x [id, d, sw, gw, p, mc, mr, nb]
    #     for n in range(0, self.total_area()):
    #         for i in range(0, len(self.assets)):
    #             d = water.demand(ETo=inputs[i,0], kc=inputs[i,1])
    #             s, g = water.available(d=d, p=inputs[i,2], s=cp.S, g=cp.G)
    #             w = (s[0] + g[0] + inputs[i,2]) / d if d > 0 else 1  # portion demanded water    
    #             q = cp.assets[j].production_fx(w)
    #             mr = cp.assets[] 
                    

    
    # def choice(self, q: float, input: np.ndarray, plan: np.ndarray)
    #     for i in range(0, len(self.assets)):
    #         pass 
            
            
        #choices = np.permutation(len(self.assets)) # randomize access to water
        
    
       

# @dataclass
# class Resouces:
#     '''
#     Keeps track of system level resources.
#     '''
#     def __init__(self, G: Groundwater, S: Surfacewater,
#                  total_area: int, choices: np.ndarray, initial_allocation: np.ndarray):
#         self.G = G
#         self.S = S
#         self._choices = choices
#         self._choices.flags.writeable = False
#         self._total_area = total_area
    
#     @property
#     def choices(self) -> np.ndarray:
#         '''
#         Returns np.ndarray(shape=)
#         '''        
#         return self._choices
    
#     @property
#     def total_area(self) -> int:
#         return self._total_area
    

        
#     total_area: int  
#     choices: np.ndarray
#     allocation: np.ndarray
#     groundwater: Groundwater
#     surfacewater: Surfacewater
#     _portfolio: np.ndarray = field(init=False)
    
#     def __post_init__(self):
#         self.choices.flags.writeable = False
#         self._portfolio = self._portfolio_init_()
    
#     def _portfolio_init_(self) -> np.ndarray:
#         n: int = 0
#         portfolio = np.empty(self.total_area, dtype='I')
#         for i in range(0, len(self.allocation)):
#             portfolio[n: n + self.allocation[i]] = i
#             n += self.allocation[i]
#         return portfolio
    
#     @property
#     def portfolio(self):
#         return self._portfolio
    
#     @portfolio.setter
#     def portfolio(self, portfolio: np.ndarray):
#         self._portfolio = portfolio
#         ids, counts = np.unique(portfolio)
#         for i in ids:
#             #self.allocation[i] = 
#             pass
#         return [(self.investments[ids[i]].name, counts[i]) for i in range(0, len(ids))]
    
#     def display_allocation(self):
#         return [(self.choices[i].name, self.allocation[i]) for i in range(0, len(self.choices))]
            
#     def central_planner(self, crop_inputs: np.ndarray, surfacewater: float):
#         allocation: np.ndarray = np.zeros(self.total_area, dtype='I')
#         for i in range(0, self.total_area):
#             pass