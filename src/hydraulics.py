""" Namespace creation for the hydraulic system """

# Imports
from dataclasses import dataclass


# Parent Hydraulic System
@dataclass
class Hydraulic:
    location: str
    bulk_modulus: float
    
    
# Valve System
@dataclass
class Orifice(Hydraulic):
    state: bool = False
    conductance: float = 0.0
    flow_rate: float = 0.0
    
    def get_mass_flow_rate(self, Pin:float, Pout:float):
        pass

    def open_valve(self):
        pass

    def close_valve(self):
        pass



# Reservoir System
@dataclass
class Volume(Hydraulic):
    pressure: float
    volume: float
    

    def get_pressure(self, delta_t:float, mass_flow_rates:list):
        pass
    
    
    