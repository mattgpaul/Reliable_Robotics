# Imports
import time
from cmath import inf
from dataclasses import dataclass



# Initial Conditions

# Accumulator 1 Volume
V1 = 100

# Pressure in acculator 1
P1 = 1000

# Acculator 2 Volume
V2 = 1

# Pressure in accumulator 2
P2 = 0

# Volume in accumulator 3 (assumed to be infinite)
V3 = inf

# Pressure in accumulator 3
P3 = 0

# Conductance between V1 and V2
G1 = 0

# Conductance between V2 and V3
G2 = 0

# Bulk Modulus of the fluid
BETA = 10

# Time [start, end, interval] (seconds)
timeslot = [0, 10, 0.01]

# Simulated events

@dataclass
class Valve:
    """Class to handle the creation, state, and actuation of the valves in the system
    """
    state: bool
    volume: float
    pressure: float
    flow_rate: float = 0
    
    def open_valve(self):
        self.state = 1
        
    
    def close_valve(self):
        self.state = 0
    
    
        

##################### Necessary Functions #########################
def mass_flow_rate(G: float, Pa: float, Pb: float):
    """Calulcate the mass flow rate for a given instance in time
    """
    
    Q = G * (Pa - Pb)   # Calculate the mass flow rate from the pressure differential and conductance
    return Q

def delta_pressure(deltat: float, Q: list, Beta: float, V: float):
    """Calculate the change in pressure between 2 states in a volume element
    """
    Pdelta = deltat * (Beta / V) * sum(Q)   # Calculate the rate of change of pressure between 2 Volume Elements
    return Pdelta


    
       
def parse_logs():
    """Print to console the necessary information to be viewed by the Test Conductor
    """
    pass


# Simulation specific functions (not related to the system)
def activate_event(event: dict, t: float):
    """Activate an event based on time requested by the user.
    """
    if t in event['TIME']:
        time_index = [i for i, val in enumerate(event['TIME']) if val == t][0]
        event_acuator = event['CMD'][time_index]()
        
        print(f"{t:.2f}: event {event['NAME'][time_index]}")
    else:
        return False
    

################################ Simulation ##########################################
accumulator = Valve(state=G1, volume=V1, pressure=P1)
cylinder = Valve(state=G2, volume=V2, pressure=P2)
tank = Valve(state=0, volume=V3, pressure=P3)

events = {
    'TIME':[1.0, 4.0, 8.0],
    'CMD': [accumulator.open_valve, accumulator.close_valve, cylinder.open_valve],
    'NAME': ['fill_on','fill_off','drain_on']
}

timestamp = timeslot[0]

while timestamp <= timeslot[1]:
    print(f"{timestamp:.2f}: accumulator {accumulator.pressure} cylinder {cylinder.pressure}")
    
    if timestamp > timeslot[0] and timestamp <= 8.0:
        # Run the activate event function before calculating
        activate_event(events, timestamp)
        
        # Adjust Accumulator
        accumulator.flow_rate = mass_flow_rate(accumulator.state, accumulator.pressure, cylinder.pressure)
        
        # Hardcoded a -1 multiplier to account for pressure leaving, not entering, the accumulator
        accumulator.pressure += delta_pressure(timeslot[2], [accumulator.flow_rate, cylinder.flow_rate], BETA, accumulator.volume)*-1
        
        # Adjust Cylinder
        cylinder.flow_rate = mass_flow_rate(cylinder.state, cylinder.pressure, accumulator.pressure)
        cylinder.pressure += delta_pressure(timeslot[2], [cylinder.flow_rate, accumulator.flow_rate], BETA, cylinder.volume)
        
    elif timestamp > timeslot[0] and timestamp > 8.0:
        
        # Adjust Cylinder (another hardcoded -1 multiplier for fluid leaving)
        cylinder.flow_rate = mass_flow_rate(cylinder.state, cylinder.pressure, tank.pressure)
        cylinder.pressure += delta_pressure(timeslot[2], [cylinder.flow_rate, tank.flow_rate], BETA, cylinder.volume)*-1
        
        # Adjust Tank
        tank.flow_rate = mass_flow_rate(tank.state, tank.pressure, cylinder.pressure)
        tank.pressure += delta_pressure(timeslot[2], [tank.flow_rate, cylinder.flow_rate], BETA, tank.volume)
    
    timestamp = round(timestamp + timeslot[2], 2)
    time.sleep(timeslot[2])


