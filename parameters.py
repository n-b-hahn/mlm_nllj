import numpy as np
# Physical parameters of the model

# Atmospheric thermodynamics (from Iribarne and Godson, 2. edition, 1981)
Rd = 287.05  # J /kg /K
Rv = 461.51  # J /kg /K
cpd = 1005.0  # J /kg /K
cpv = 1850.0  # J /kg /K
cl = 4218.0  # J /kg /K
lv0 = 2501.0e3  # J /kg, enthalpy of vaporization at 0 C

eps1 = Rd / Rv
eps2 = Rv / Rd - 1.0

g = 9.81  # m /s^2, Earth's gravitational acceleration

T_00 = 288.15 # K, mean sea level temperature
#T_00 = 288.15 * 1.1  #test temperature
p_00 = 101325.0  # Pa, mean sea level pressure
rho_00 = p_00 / (Rd * T_00)

# Environment. Some values from Mellado et al. (2017),
divergence = -1.0e-6  # m /s, large-scale divergence
s_00 = cpd * T_00  # reference liquid-water static energy
gamma_T = 3.0e-3  # K /m, static temperature gradient
#gamma_T = 3.0e-3 * 1.1 #test gradient
gamma_s = cpd * gamma_T  # J /kg /m
q_00 = 10.0e-3  # kg /kg, reference total-water specific humidity
#q_00 = 10.0e-3 * 1.1 #test specific humidity
gamma_q = -1.0e-6  # kg /kg /m, gradient of total-water specific humidity
#gamma_q = -1.0e-6 * 1.1 #test gradient
# Wind
u_g = 10 # m /s, reference u wind speed
gamma_u = 0
v_g = 10 # m /s, reference v wind speed
gamma_v =0
C= 0.001 # Drag coefficent 10^-3
#C= 0.030# Drag coefficent test
# Forcing. Some values from Mellado et al. (2017), https://doi.org/10.1002/qj.3095
F_s0 = 200.0 / rho_00  # (J /kg) m /s, surface energy kinematic flux
F_q0 = 0.2e-4  # (kg /kg) m /s, surface moisture kinematic flux
Tdiurnal = 3600.0 * 24.0  # s, diurnal period

# Coriolis
Omega = 7.2921e-5   # s^-1, Coriolis parameter
phi = 53 #grad nö4rdliche Breite
#phi = 78 #test nördliche Breite
f = 2.*Omega*np.sin(phi*np.pi/180.)
print((2*np.pi)/f)