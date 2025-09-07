

rof_S1 = 2.2
rof_S2 = 2.1

rho_ox = 1050
 
m_prop_S1 = 100

m_ox_S1 = m_prop_S1*(rof_S1/(1+rof_S1))
m_ox_S2 = m_prop_S1*(rof_S2/(1+rof_S2))

m_fu_S1 = m_prop_S1 - m_ox_S1
#m_fu_S2 = m_prop_S2 - m_ox_S2

v_ox_tank_S1 = m_ox_S1/rho_ox