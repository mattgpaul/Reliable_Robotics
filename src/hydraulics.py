""" Namespace creation for the hydraulic system """

# Imports
from dataclasses import dataclass
from typing import List


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

    def get_mass_flow_rate(self, Pin: float, Pout: float):
        mass_flow_rate = self.conductance * (Pout - Pin)
        self.flow_rate = mass_flow_rate
        return mass_flow_rate

    def open_valve(self):
        self.state = True
        return True

    def close_valve(self):
        self.state = False
        return False


# Reservoir System
@dataclass
class Volume(Hydraulic):
    pressure: float
    volume: float

    def get_pressure(self, delta_t: float, mass_flow_rates: List[float]):
        new_pressure = ((self.bulk_modulus/self.volume)*delta_t)*sum(mass_flow_rates)
        delta_pressure = self.pressure + new_pressure
        self.pressure = delta_pressure
        return delta_pressure
