
from CoolProp.CoolProp import PropsSI

# Suppose these are your design inputs (could be read from a file/CI vars)
P_inlet = 2.5e5     # Pa
T_inlet = 288.15    # K

rho_air = PropsSI("D", "T", T_inlet, "P", P_inlet, "Air")

# Any numeric variables defined here at module (global) scope will be extracted
analysis_air_density = rho_air      # <-- Flow will ingest this as an analysis/model value
