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