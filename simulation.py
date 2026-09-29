import numpy as np
from scipy.integrate import solve_ivp, RK23
from equations import *
import globals as gs
from iodata import *
from postprocessing import *

# define total time interval to integrate, in seconds
tfinal = 3600.0 * 24.0 * 3.0  # 3 days

# define time interval to obtain data, in seconds
tinterval = 60.0 * 10.0  # every 10 minutes

# define system of equations as dictionary of dictionaries
system = {}
system["h"] = {"ode": dh_dt, "name": "h", "name_long": "height (m)"}
system["s"] = {"ode": ds_dt, "name": "s", "name_long": "liquid-water static energy (J/kg)"}
system["q"] = {"ode": dq_dt, "name": "q", "name_long": "total-water specific humidity (kg/kg)"}
system["u"] = {"ode": du_dt, "name": "u", "name_long": "zonal wind (m/s)"}
system["v"] = {"ode": dv_dt, "name": "v", "name_long": "meridional wind (m/s)"}
num_vars = len(system)

h_initial = 300.0  # m, boundary-layer height
system["h"]["ics"] = h_initial  # m, boundary-layer height
system["s"]["ics"] = s_env(h_initial * 0.5)  # J /kg, liquid-water static energy
system["q"]["ics"] = q_env(h_initial * 0.5)  # total-water specific humidity
system["u"]["ics"] = u_env(h_initial * 0.5)  # bulk u wind
system["v"]["ics"] = v_env(h_initial * 0.5)  # bulk v wind

# define the surface parametrization you want to use
#gs.sflux_s = Fs_constant
#gs.sflux_q = Fq_constant
gs.sflux_s = Fs_diurnal
gs.sflux_q = Fq_diurnal
gs.sflux_u = Fu_bulk
gs.sflux_v = Fv_bulk
# define the entrainment parametrization you want to use
gs.E = E_free_convection


##################################### No need to change beyond this point
# create array with the checkpointing times (times at which I get data)
times = np.arange(0.0, tfinal, tinterval)
times = np.append(times, tfinal)  # include the final time


# construct initial condition
state = []
for item in system.values():
    state.append(item["ics"])
state = np.array(state)


# construct tendency accordingly to the choice of variables
def tendency(t, state):
    tendency = []
    for item in system.values():
        tendency.append(item["ode"](t, state))
    return np.array(tendency)


# construct indexes for clarity in equations
for idx, item in enumerate(system.values()):
    if item["name"] == "h":
        gs.idx_h = idx
    if item["name"] == "s":
        gs.idx_s = idx
    if item["name"] == "q":
        gs.idx_q = idx
    if item["name"] == "u":
        gs.idx_u = idx
    if item["name"] == "v":
        gs.idx_v = idx
# do simulation
sol = solve_ivp(tendency, [times[0], times[-1]], state, RK23, t_eval=times)
print(sol.message)

# save data
var_names = []
for item in system.values():
    var_names.append(item["name"])

save_netcdf(sol.t, sol.y, var_names, "mlm")

# plot result
var_names = []
for item in system.values():
    var_names.append(item["name_long"])

PlotEvolution(sol.t, sol.y, var_names, "evolution")

# PlotProfiles(sol.t[-1:], sol.y[:,-1:], var_names, "profiles") # just the last
time_indices = [int(np.size(times) / 2), -1]  # one in the middle, and the last
PlotProfiles(
    sol.t[time_indices],
    sol.y[:, time_indices],
    var_names,
    "profiles",
)

diag = compute_diagnostics(sol.t, sol.y)

PlotDiagnostics(
    sol.t,
    {
        "entrainment (m/s)": diag["entrainment (m/s)"],
        "surface-flux (m/s)": diag["surfaceflux (m/s)"],
        "Sum of fluxes (m/s)": diag["Sum of fluxes (m/s)"],
        "coriolis (m/s)": diag["coriolis (m/s)"],
        "v_mag (m/s)": diag["v_mag (m/s)"],
    },
    "diagnostics_magnitude",
)


import surface

C_values = [0.001, 0.001*0.9,0.001* 1.1]
diag_runs = {}

for C_val in C_values:
    surface.C = C_val

    state_sweep = np.array([item["ics"] for item in system.values()])
    sol_sweep = solve_ivp(tendency, [times[0], times[-1]], state_sweep, RK23, t_eval=times)

    diag_runs[f"C={C_val}"] = compute_diagnostics(sol_sweep.t, sol_sweep.y)

PlotDiagnosticsMultiRun(
    times,
    diag_runs,
    ["entrainment (m/s)", "surfaceflux (m/s)", "Sum of fluxes (m/s)", "coriolis (m/s)", "v_mag (m/s)"],
    "diagnostics_Ccompare",
)