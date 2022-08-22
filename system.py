from typing import Protocol
from abc import abstractmethod
from dataclasses import dataclass

import numpy as np

import water
import crops

class Planner(Protocol):
    G: water.Groundwater
    S: water.Surfacewater
    crops: np.ndarray
    portfolio: np.ndarray
    
    @abstractmethod
    def plan(self, inputs: np.ndarray) -> np.ndarray:
        pass

@dataclass
class CentralPlanner:
    G: water.Groundwater = water.Groundwater()
    S: water.Surfacewater = water.Surfacewater()
    crops: np.ndarray = np.array([crops.Fallow(), 
                                  crops.Annual(),
                                  crops.Perennial()], dtype=np.dtype(crops.Crop))
    portfolio: np.ndarray = np.array([50, 25, 25], dtype='I')
    
    def id(self, name: str) -> int:
        name = str.upper(name)
        for i in range(0, len(self.crops)):
            if self.crops[i].name == name:
                return i
        raise KeyError(name)

    def crop(self, name: str):
        id = self.id(name)
        return self.crops[id]
             
    def total_area(self) -> int:
        return np.sum(self.portfolio)
    
    def is_new(self, id: int, outputs: np.ndarray) -> bool:
        return self.portfolio[id] < (outputs[:,0] == id).sum()
    
    def crop_outputs(self, id: int, inputs: np.ndarray, new: bool = False) -> np.ndarray:
        crop = self.crops[id]
        demand = crop.water_demand(eto=inputs[0], kc=inputs[1])
        surface, ground = water.bid(d=demand, p=inputs[2], s=self.S, g=self.G)
        portion_water: float = (surface[0] + ground[0] + inputs[2]) / demand if 0 < demand else 1
        marginal_revenue = crop.mr(p=inputs[3], q=crop.production(portion_water), r=inputs[4])
        marginal_cost = crop.mc(new=new, wc=surface[1] + ground[1], r=inputs[4])
        return np.array([id, demand, surface[0], ground[0], inputs[2], marginal_revenue, marginal_cost, crop.npv(marginal_revenue, marginal_cost)])
    
    def plan(self, inputs: np.ndarray):
        '''
        This will loop over each unit of land committing it to production of the highest npv crop, given the available water and other factors.
        
        Arguments:
            inputs: np.ndarray[shape=(assets x [ETo, kc, precip, price, discount_rate]), dtype=float]
        Returns:
            outputs: np.ndarray[shape=(total_area x [id, demand, sw, gw, precip, mr, mc, npv]), dtype=float]
        '''
        outputs = np.full((self.total_area(), 8), np.nan) # area x [id, d, sw, gw, p, mr, mc, npv]
        for n in range(0,5): #self.total_area()):
            # choices: shape = assets x [id, demand, sw, gw, precip, mr, mc, npv] 
            choices = np.full((len(self.crops), 8), np.nan)
            for c in range(0, len(self.crops)):
                new = self.is_new(c, outputs)
                choices[c,:] = self.crop_outputs(c, inputs[c,:], new)
            maxnpv = choices[:,7].max()
            if maxnpv <= 0:
                fallow = self.id(name=crops.Names.FALLOW.name)
                outputs[n,:] = choices[fallow,:]
            else:
                maxes = choices[choices[:,7] == maxnpv]
                if maxes.shape[0] > 1:
                    np.random.shuffle(maxes)
                    maxes = maxes[0,:]
                outputs[n,:] = maxes
            self.S.deliver(q=outputs[n,2])
            self.G.pump(q=outputs[n,3])
        return outputs