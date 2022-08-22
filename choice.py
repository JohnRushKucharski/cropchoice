# import math
# import random
# from dataclasses import dataclass
# from typing import List, Tuple, Callable

# from water import Groundwater, Surfacewater
# from crops import Names, Investment, Inputs

# import numpy as np

# '''
# Input Data

# The investments module has a dataclass Inputs that is commented out. 
# For speed, inputs should be defined as numpy arrays. xarray would be another option but it is also slow for small size arrays.

# For now I assume the input at any time t will be a 2D (mxn) maxtrix in the form:

#     v1, v2, v3, .., vn-1, vn 
# a | ..
# b |     ..
# c |         ..
# ...
# m |             ..   ...  ..

# where there a m investments and n input variables. 

# A third dimension (mxnxt) might added to hold all inputs across T time periods.
# '''
# @dataclass
# class Planner:
#     '''
#     Allocates investments (between crops, fallow land) given shared land and water endowments.
#     '''
#     total_area: int
#     '''
#     Units are area in production.
#     '''
#     crops: List[Investment] # immutable numpy array object crops.flags.writable=false.
#     allocation: List[int]   # numpy array int position of crop allocation.flags.writable = False
#     groundwater: Groundwater
#     '''
#     Groundwater object shared by crops in total_area.
#     '''
#     surfacewater: Surfacewater
#     '''
#     Surfacewater object shared by crops in total_area.
#     '''
 
#     def water_allocation(self, demand: float):
#         '''
#         Attempts to meet specified water demands by allocating available surfacewater and groundwater resources.
        
#         Returns: 
#             Tuple[Tuple[float, float], Tuple[float, float]]: in the form: ((surfacewater quantity, surface water cost), (groundwater quantity, groundwater price))
        
#         Notes: 
#             [1] Order of allocation is surfacewater then groundwater, 
#             [2] Sum of surfacewater and groundwater quantites equal demand, unless demand exceeds availability
#         '''
#         sw = self.surfacewater.bid(demand)
#         gw = demand - sw[0] if sw[0] < demand else 0
#         return sw, self.groundwater.bid(gw)
    
#     def is_available(self, q_sw: float, q_gw: float, areas):
#         '''
#         True if 
#         '''
#         return True if q_sw <= self.surfacewater.available and q_gw + self.groundwater.deficit <= self.groundwater.max_deficit and np.sum(areas) < self.total_area else False
    
#     def choose(self, npvs, water, areas):
#         sw, gw, mx = 0, 0, np.max(npvs)
#         if mx < 0:
#             return areas
#         indices = np.where(npvs==mx)[0]
#         random.shuffle(indices)
#         for i in indices:
#             if self.is_available(water[i][0], water[i][1], areas):
#                 self.groundwater.pump(water[i][1]) 
#                 self.surfacewater.deliver(water[i][0])
#                 areas[i] += 1
#         return areas

#     def update_areas(self, investments, areas):
#         for i in range(0, len(areas)):
#             investments[i][0].units = areas[i]
#         return areas

#     def central_planner(self, q: float, investments: List[Tuple[Investment, Input]]):
#         I = len(investments)
#         areas = np.zeros(I)
#         # 1. Set surfacewater supply
#         self.surfacewater.supply(q)
#         while np.sum(areas) < self.total_area:           
#             npvs, water = np.zeros(I), np.zeros(I, dtype='f,f')
#             for i in range(0, I):
#                 crop, data = investments[i][0], investments[i][1]
#                 d = unit_demand(ETo=data.eto, kc=data.kc, p=data.prec)
#                 sw, gw = self.water_allocation(demand=d)
#                 water[i] = (sw[0], gw[0])
#                 if crop.name != Names.FALLOW.name and sum(list(water[i])) == 0:
#                     npvs[i] = -1
#                 else:
#                     portion = 1 if d <= 0 else (sw[0] + gw[0]) / d
#                     q = crop.production_fx(portion)
#                     new = True if crop.units < areas[i] else False
#                     npvs[i] = crop.unit_npv(new=new, price=data.price, production=q, water_cost=sw[1]+gw[1], r=data.discount_rate)
#             areas = self.choose(npvs, water, areas)
#             print(f'npvs: {npvs}, water: {water}, areas: {areas}')
#         return self.update_areas(investments, areas)
    
#     def individual_planner(self, surfacewater: float, data: np.ndarray):
#         '''
#         data:
#                     eto, kc, prec, price, discount_rate 
#                 a |
#                 b |
#                         ...
#                 m |
#         '''
#         self.surfacewater.supply(q) # reset surfacewater supply.
#         for i in range(0, self.total_area):
#             pass
#         pass
    
#     def choices(self, q: float, c: int, inputs):
#         choices = np.zeros(len(self.crops), dtype='f,f') # output[i] = (q, npv) where ith crop in crops
#         for i in range(0, len(self.crops)):
#             demand = crops.unit_demand(ETo=inputs[0], kc=inputs[1], p=inputs[2])
#             sw, gw = self.water_allocation(demand=demand)
#             q_prod = self.crops[i].production_fx(1 if demand <= 0 else (sw[0]+gw[0])/demand)
#             npv = self.crops[i].unit_npv(new=False if i == c else True, 
#                                          price=inputs[3], production=q_prod, 
#                                          water_cost=sw[1] + gw[1], r=inputs[4])
#             choices[i] = (sw[0], npv)
#         return choices
                
                

                
        
        
#         # n = len(investments)
#         # areas = np.zeros(n)
#         # for i in range(0, n):
#         #     crop, inputs = investment[i], data[i,:] 
#         #     d = crops.unit_demand(ETo=inputs[0], kc=inputs[1], p=inputs[2])
#         #     s, g = self.water_allocation(demand=d)
#         #     q = crop.production_fx(1 if d <= 0 else (s[0]+g[0])/d)
            
            
            
#     def production(self, sw, investment, inputs):
#         demand = crops.unit_demand(ETo=inputs[0], kc=inputs[1], p=inputs[2])
        
            