# Imports
from src.hydraulics import Orifice, Volume
from cmath import inf
import time
from typing import Dict, Any

# Setup

# TODO: Turn this into a function (or something like it) such that each test case can start with the same initializations. Or utilize pytest

# Instantiate accumulator, cylinder, and tank
accumulator = Volume(
    location='rudder',
    bulk_modulus=10,
    pressure=1000,
    volume=100
)

cylinder = Volume(
    location='rudder',
    bulk_modulus=10,
    pressure=0,
    volume=1
)

tank = Volume(
    location='rudder',
    bulk_modulus=10,
    pressure=0,
    volume=inf
)

# Instantiate fill and drain valves

fill = Orifice(
    location='rudder',
    bulk_modulus=10,
)

drain = Orifice(
    location='rudder',
    bulk_modulus=10
)

# Test Cases
tests = {}
tests['CASE_0'] = {
    'TIME': [1.0, 4.0, 8.0],
    'CMD': [fill.open_valve, fill.close_valve, drain.open_valve],
    'NAME': ['fill_on', 'fill_off', 'drain_on']
}

tests['CASE_1'] = {
    'TIME': [2.0, 3.0, 5.0],
    'CMD': [fill.open_valve, fill.close_valve, drain.open_valve],
    'NAME': ['fill_on', 'fill_off', 'drain_on']
}

tests['CASE_2'] = {
    'TIME': [7.0, 7.5, 8.0],
    'CMD': [fill.open_valve, fill.close_valve, drain.open_valve],
    'NAME': ['fill_on', 'fill_off', 'drain_on']
}


# Simulation Functions
def get_system_status(timestamp: float, delta_t: float):
    # Adjust flow rates
    accumulator_flow = fill.get_mass_flow_rate(accumulator.pressure, cylinder.pressure)
    cylinder_flow = [
        fill.get_mass_flow_rate(cylinder.pressure, accumulator.pressure),
        drain.get_mass_flow_rate(cylinder.pressure, tank.pressure)
    ]
    tank_flow = drain.get_mass_flow_rate(tank.pressure, cylinder.pressure)
    # Adjust Pressures
    accumulator.get_pressure(delta_t, [accumulator_flow])
    cylinder.get_pressure(delta_t, cylinder_flow)
    tank.get_pressure(delta_t, [tank_flow])
    print(f"{timestamp:.2f}: accumulator {accumulator.pressure:.2f} cylinder {cylinder.pressure:.2f}")


def get_event(event: Dict[Any, Any], timestamp: float):
    if timestamp in event['TIME']:
        index = event['TIME'].index(timestamp)
        event['CMD'][index]()
        print(f"{t:.2f}: event {event['NAME'][index]}")


# Simulation
if __name__ == '__main__':
    for test_case in tests:
        t_start = 0.0
        t_end = 10.0
        t_interval = 0.01
        t = t_start
        while t <= t_end:
            get_event(tests[test_case], round(t, 2))
            get_system_status(t, t_interval)
            t += t_interval
            time.sleep(t_interval)
