'This is a oversimplified propellant mass calculator with inaccurate or intentionally wrong values used to test the integration into Flow'
import math as m
# missing variables are defined as input in flow

'Orbital speed required'
# Input: LEO altitude
g = 9.81
mu = 3.986004418e14      # Earths standard gravitational parameter
r = 6371000 + h          # orbital radius
dv_orbital = m.sqrt(mu/r)

'Approximate dv losses'
dv_gravitational = 1400
dv_drag = 250
dv_steering = 150

dv_total = dv_orbital +dv_gravitational +dv_drag +dv_steering


dv_S1 = 0.42*dv_total
dv_S2 = 0.58*dv_total

S1_isp =  s1_isp_input
S2_isp = 310

MR_S1 = (m.e)**(dv_S1/(g*S1_isp))
MR_S2 = (m.e)**(dv_S2/(g*S2_isp))

m_dry_S2 = 900
m_dry_S1 = 3900

m_wet_S2 = MR_S2*(m_payload + m_dry_S2 )
m_wet_S1 = MR_S1*(m_wet_S2 + m_dry_S1)

m_prop_S2 = m_wet_S2 - m_payload - m_dry_S2

m_prop_S1_output = m_wet_S1 - m_wet_S2 - m_dry_S1
m_prop_S1_input = m_prop_S1_output

s1_isp_output = 265








