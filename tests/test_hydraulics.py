from cmath import inf
from src.hydraulics import Hydraulic, Orifice, Volume
import pytest
from pytest import mark


@mark.orifice
class TestOrifice:
    

    def test_mass_flow_rate_out(self):
        
        #Arrange
        valve = Orifice(location='rudder', bulk_modulus=10.0, state=True, conductance=1.0)
        Pin = 1000.0
        Pout = 1.0
        
        #Act
        flow_rate = valve.get_mass_flow_rate(Pin, Pout)
        
        #Assert
        assert flow_rate == pytest.approx(-999.0)
        assert valve.flow_rate == flow_rate
        

    def test_mass_flow_rate_in(self):
        
        #Arrange
        valve = Orifice(location='rudder', bulk_modulus=10.0, state=True, conductance=1.0)
        Pin = 1.0
        Pout = 1000.0
        
        #Act
        flow_rate = valve.get_mass_flow_rate(Pin, Pout)
        
        #Assert
        assert flow_rate == pytest.approx(999.0)
        assert valve.flow_rate == flow_rate
        
        
    def test_valve_open(self):
        
        #Arrange
        valve = Orifice(location='rudder', bulk_modulus=10.0)
        
        #Act
        state = valve.open_valve()
        
        #Assert
        assert state == True
        assert valve.state == True
    
        
    def test_valve_close(self):
        
        #Arrange
        valve = Orifice(location='rudder', bulk_modulus=10.0, state=True, conductance=1.0)
        
        #Act
        state = valve.close_valve()
        
        #Assert
        assert state == False
        assert valve.state == False
        



@mark.volume     
class TestVolume:
    testdata = [
    (
        Volume('rudder',bulk_modulus=10, pressure=1000, volume=100), 
        Orifice('rudder', bulk_modulus=10), 
        Volume('rudder', bulk_modulus=10, pressure=0, volume=1),
        1000.0
     ),
    (
        Volume('rudder',bulk_modulus=10, pressure=1000, volume=100), 
        Orifice('rudder', bulk_modulus=10, state=True, conductance=1), 
        Volume('rudder', bulk_modulus=10, pressure=0, volume=1),
        999.0
    ),
    (
        Volume('rudder',bulk_modulus=10, pressure=1000, volume=100), 
        Orifice('rudder', bulk_modulus=10, state=True, conductance=1), 
        Volume('rudder', bulk_modulus=10, pressure=0, volume=inf),
        999.0
     ),
    ]
       
    @mark.parametrize("volume1, orifice12, volume2, expected", testdata) 
    def test_high_to_low_pressure_diff_calculation(self, volume1, orifice12, volume2, expected):
        
        #Arrange
        orifice12.get_mass_flow_rate(volume1.pressure, volume2.pressure)
        
        #Act
        delta_p = volume1.get_pressure(delta_t=0.01, mass_flow_rates=[orifice12.flow_rate])
        
        #Assert
        assert volume1.pressure == pytest.approx(expected)
        
 
    testdata = [
    (
        Volume('rudder',bulk_modulus=10, pressure=1000, volume=100), 
        Orifice('rudder', bulk_modulus=10), 
        Volume('rudder', bulk_modulus=10, pressure=0, volume=1),
        0.0
     ),
    (
        Volume('rudder',bulk_modulus=10, pressure=1000, volume=100), 
        Orifice('rudder', bulk_modulus=10, state=True, conductance=1), 
        Volume('rudder', bulk_modulus=10, pressure=0, volume=1),
        100.0
    ),
    ]
           
    @mark.parametrize("volume1, orifice12, volume2, expected", testdata) 
    def test_low_to_high_pressure_diff_calculation(self, volume1, orifice12, volume2, expected):
        
        #Arrange
        orifice12.get_mass_flow_rate(volume2.pressure, volume1.pressure)
        
        #Act
        delta_p = volume2.get_pressure(delta_t=0.01, mass_flow_rates=[orifice12.flow_rate])
        
        #Assert
        assert volume2.pressure == pytest.approx(expected)
