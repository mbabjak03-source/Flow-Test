# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 07:18:05 2026

@author: matej.babjak
"""

# given: Input i s1 total burnable propellant mass, transient ofs and the losses in transients

import CoolProp as cp


# =========================
# === EXTERNAL INPUTS ===
# =========================

lox_tank_pressure       = 3.0e5   # Pa  (e.g., ~3 bar)
lpp_tank_pressure       = 3.0e5   # Pa
lox_bulk_temperature    = 93.0    # K
lpp_bulk_temperature    = 109.0   # K  (assumed liquid methane)
LOX_FLUID = "Oxygen"
LPP_FLUID = "Propane"   

'''

# Tank conditions (Pa, K)

num_engines                = 12
num_of_ignitions    = 1      # number of static fires per engine before liftoff
static_hotfire_duration    = 1.5    # s, duration per static fire per engine
engine_total_mdot          = 28  

top_off_lox = 20

top_off_lpp = 20

startup_total_loss   = 10      # kg per startup event (ox+fuel)
startup_of           = 1       # O/F during startup transient

chilldown_total_loss = 7     # kg per chilldown event (ox+fuel)
chilldown_of         = 7       # O/F during chilldown (often ox-dominated)

shutdown_total_loss  = 3      # kg per shutdown event (ox+fuel)
shutdown_of          = 2       # O/F during shutdown transient

lox_unburnable_volume = 30.0     # L
lpp_unburnable_volume = 29.0     # L

boiloff_ox = 18

boiloff_fuel = 10

leakage_ox = 1 
leakage_fuel = 1

'''

try:
    from CoolProp.CoolProp import PropsSI
except Exception:
    import CoolProp.CoolProp as _CP
    PropsSI = _CP.PropsSI

stage_nominal_of = 2.3
stage_burnable_mass = 59000.0
stage_residuals_target = 300.0
stage_reserve = 100.0



def split_by_of(total_mass: float, of: float):
    """
    Split a total propellant mass into LOX and fuel components using O/F.
    total_mass = m_ox + m_fuel;  OF = m_ox/m_fuel
    """
    m_ox = total_mass * of / (1.0 + of)
    m_fuel = total_mass - m_ox
    return m_ox, m_fuel




lox_burnable_mass, lpp_burnable_mass = split_by_of(stage_burnable_mass, stage_nominal_of)

lox_reserve_mass, lpp_reserve_mass = split_by_of(stage_reserve, stage_nominal_of)


L_to_m3 = 1e-3


rho_lox = PropsSI('D', 'T', lox_bulk_temperature, 'P', lox_tank_pressure, LOX_FLUID)
rho_lpp = PropsSI('D', 'T', lpp_bulk_temperature, 'P', lpp_tank_pressure, LPP_FLUID)


lox_unburnable_mass = lox_unburnable_volume * L_to_m3 * rho_lox
lpp_unburnable_mass = lpp_unburnable_volume * L_to_m3 * rho_lpp

# =========================
# === Residuals (reserve + unburnable) ===
# =========================

lox_residuals = lox_reserve_mass + lox_unburnable_mass
lpp_residuals = lpp_reserve_mass + lpp_unburnable_mass
stage_residuals = lox_residuals + lpp_residuals

# =========================
# === Pre-liftoff mass losses ===
# Definition: sum of chilldown + startup + static hotfire losses
# =========================

# Startup losses (prelaunch)

if num_of_ignitions <=1:
        
    startup_pre_ox, startup_pre_fuel = split_by_of(startup_total_loss, startup_of)
    startup_pre_ox   *= num_engines * num_of_ignitions
    startup_pre_fuel *= num_engines * num_of_ignitions
    
    chill_pre_ox, chill_pre_fuel = split_by_of(chilldown_total_loss, chilldown_of)
    chill_pre_ox   *= num_engines * num_of_ignitions
    chill_pre_fuel *= num_engines * num_of_ignitions
    
    hotfire_total = engine_total_mdot * static_hotfire_duration * num_engines 
    hotfire_total = engine_total_mdot * static_hotfire_duration * num_engines * num_of_ignitions
    hotfire_ox, hotfire_fuel = split_by_of(hotfire_total, stage_nominal_of)
    
    lox_mass_expelled_before_liftoff =  startup_pre_ox + chill_pre_ox + hotfire_ox
    lpp_mass_expelled_before_liftoff =  startup_pre_fuel + chill_pre_fuel + hotfire_fuel
    propellant_mass_expelled_before_liftoff  = lox_mass_expelled_before_liftoff + lpp_mass_expelled_before_liftoff
    
    
    
    
    shutdown_flight_ox, shutdown_flight_fuel = split_by_of(shutdown_total_loss, shutdown_of)
    shutdown_flight_ox   *= num_engines * num_of_ignitions
    shutdown_flight_fuel *= num_engines * num_of_ignitions
    
    lox_mass_expelled_after_liftoff =  shutdown_flight_ox + boiloff_ox + leakage_ox
    lpp_mass_expelled_after_liftoff =  shutdown_flight_fuel + boiloff_fuel + leakage_fuel
    propellant_mass_expelled_after_liftoff  = lox_mass_expelled_after_liftoff + lpp_mass_expelled_after_liftoff
    
    
    
    
else:
    lox_mass_expelled_before_liftoff =  0
    lpp_mass_expelled_before_liftoff =  0
    propellant_mass_expelled_before_liftoff  = lox_mass_expelled_before_liftoff + lpp_mass_expelled_before_liftoff
    
    startup_flight_ox, startup_flight_fuel = split_by_of(startup_total_loss, startup_of)
    startup_flight_ox   *= num_engines * num_of_ignitions
    startup_flight_fuel *= num_engines * num_of_ignitions
    
    chill_ox, chill_pre_fuel = split_by_of(chilldown_total_loss, chilldown_of)
    chill_ox   *= num_engines * num_of_ignitions
    chill_fuel *= num_engines * num_of_ignitions
    
    shutdown_flight_ox, shutdown_flight_fuel = split_by_of(shutdown_total_loss, shutdown_of)
    shutdown_flight_ox   *= num_engines * num_of_ignitions
    shutdown_flight_fuel *= num_engines * num_of_ignitions
    
    lox_mass_expelled_after_liftoff =  chill_ox + startup_flight_ox +  shutdown_flight_ox + boiloff_ox + leakage_ox
    lpp_mass_expelled_after_liftoff =  chill_fuel + shutdown_flight_fuel + boiloff_fuel + leakage_fuel
    propellant_mass_expelled_after_liftoff  = lox_mass_expelled_after_liftoff + lpp_mass_expelled_after_liftoff
    

lox_mass_liftoff = lox_burnable_mass + lox_mass_expelled_after_liftoff
lpp_mass_liftoff = lpp_burnable_mass + lpp_mass_expelled_after_liftoff
prop_mass_liftoff = lox_mass_liftoff+lpp_mass_liftoff


lox_mass_autosequence = lox_mass_liftoff +lox_mass_expelled_before_liftoff - top_off_lox
lpp_mass_autosequence = lpp_mass_liftoff +lpp_mass_expelled_before_liftoff - top_off_lpp
prop_mass_autosequence = lox_mass_autosequence+lpp_mass_autosequence