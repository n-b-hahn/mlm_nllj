import numpy as np
import matplotlib.pyplot as plt
import globals as gs
import math
from environment import *
from parameters import *
from matplotlib.ticker import MultipleLocator

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

def PlotEvolution(times, states, var_names, filename):
    num_vars = len(var_names)

    #fig, axs = plt.subplots(1, num_vars, figsize=(num_vars * 3.5, 3))
    fig, axs = plt.subplots(1, num_vars , figsize=((num_vars ) * 3.5, 3))
    for iv in range(num_vars):
        axs[iv].plot(times[:] / 3600.0, states[iv, :])
        axs[iv].set_ylabel(var_names[iv])

        axs[iv].set_xlabel("elapsed time (hours)")
        axs[iv].set_xlim([0, None])
        axs[iv].spines["left"].set_position(("axes", -0.01))
        axs[iv].spines["bottom"].set_position(("axes", -0.01))
        if iv == gs.idx_u:
            dy = np.diff(states[iv, :])
            candidates = np.where((dy[:-1] > 0) & (dy[1:] < 0))[0] + 1
            n = len(states[iv, :])
            candidates = candidates[(candidates > 0) & (candidates < n-1)]

            umaxima = [( i, states[iv, :][i]) for i in candidates]
            #print(umaxima)
        if iv == gs.idx_v:
            dy = np.diff(states[iv, :])
            candidates = np.where((dy[:-1] > 0) & (dy[1:] < 0))[0] + 1
            n = len(states[iv, :])
            candidates = candidates[(candidates > 0) & (candidates < n-1)]

            vmaxima = [(i,states[iv, :][i]) for i in candidates]
            #print(vmaxima)


    iu = gs.idx_u
    iv = gs.idx_v
    u = states[iu, :]
    v = states[iv, :]
    V = np.sqrt(u**2 + v**2)

    dy = np.diff(V)
    candidates = np.where((dy[:-1] > 0) & (dy[1:] < 0))[0] + 1
    n = len(V)
    candidates = candidates[(candidates > 0) & (candidates < n - 1)]

    Vmaxima = [(i, V[i]) for i in candidates]
    print(Vmaxima)

    figV, axV = plt.subplots(figsize=(3.5, 3))
    axV.plot(times[:] / 3600.0, V, color="C2")
    axV.set_ylabel("V (m/s)")
    axV.set_xlabel("hours since sunrise")
    axV.set_xlim([0, None])
    axV.spines["left"].set_position(("axes", -0.01))
    axV.spines["bottom"].set_position(("axes", -0.01))

    plt.tight_layout(pad=0.1)
    plt.savefig(filename + ".pdf", bbox_inches="tight")

    plt.show()
    return fig, axs, figV, axV


def PlotProfiles(times, states, var_names, filename):
    h = states[gs.idx_h, :]  # define pointers for readability below
    s = states[gs.idx_s, :]
    q = states[gs.idx_q, :]
    u = states[gs.idx_u, :]
    v = states[gs.idx_v, :]
    num_vars = len(var_names)

    fig, axs = plt.subplots(1, num_vars - 1, figsize=((num_vars - 1) * 3.5, 3))

    hmax = np.max(h) * 1.5  # the domain to plot is 50% larger than the maximum ABL height
    z = np.linspace(
        0.0, hmax, num=100
    )  # create grid of points in the vertical direction fro background

    for it, time in enumerate(times):
        z_bl = np.array(
            [0.0, states[0, it], states[0, it], hmax]
        )  # create grid of points for the profiles

        id = 0
        for iv in range(num_vars):
            if iv == gs.idx_h:
                continue
            if iv == gs.idx_q:
                axs[id].plot(q_env(z), z, "--", color="black")
                profile = np.array([states[iv, it], states[iv, it], q_env(h[it]), q_env(hmax)])
            if iv == gs.idx_s:
                axs[id].plot(s_env(z), z, "--", color="black")
                profile = np.array([states[iv, it], states[iv, it], s_env(h[it]), s_env(hmax)])
            if iv == gs.idx_u:
                axs[id].plot(u_env(z), z, "--", color="black")
                profile = np.array([states[iv, it], states[iv, it], u_env(h[it]), u_env(hmax)])
            if iv == gs.idx_v:
                axs[id].plot(v_env(z), z, "--", color="black")
                profile = np.array([states[iv, it], states[iv, it], v_env(h[it]), v_env(hmax)])
            axs[id].plot(profile, z_bl, label="time {} h".format(times[it] / 3600.0))
            axs[id].set_xlabel(var_names[iv])
            id = id + 1

        axs[-1].legend(loc="best")

    for id in range(num_vars - 1):
        axs[id].set_ylabel(var_names[gs.idx_h])
        axs[id].set_ylim([0, None])
        axs[id].spines["left"].set_position(("axes", -0.01))
        axs[id].spines["bottom"].set_position(("axes", -0.01))

    plt.tight_layout(pad=0.1)
    plt.savefig(filename + ".pdf", bbox_inches="tight")

    plt.show()

    return fig, axs

def compute_diagnostics(t_array, y_array):
    h_vals = y_array[gs.idx_h, :]
    u_vals = y_array[gs.idx_u, :]
    v_vals = y_array[gs.idx_v, :]

    sflux_u_vals = np.zeros_like(t_array)
    sflux_v_vals = np.zeros_like(t_array)
    E_vals = np.zeros_like(t_array)

    for i, t in enumerate(t_array):
        state = y_array[:, i]
        sflux_u_vals[i] = gs.sflux_u(t, state)
        sflux_v_vals[i] = gs.sflux_v(t, state)
        E_vals[i] = gs.E(t, state)

    u_env_vals = u_env(h_vals)
    v_env_vals = v_env(h_vals)

    # entrainment contribution
    entrainment_u = E_vals * (u_env_vals - u_vals) / h_vals
    entrainment_v = E_vals * (v_env_vals - v_vals) / h_vals

    # surface-flux contribution
    surfaceflux_u = sflux_u_vals / h_vals
    surfaceflux_v = sflux_v_vals / h_vals

    # Coriolis contribution
    coriolis_u = f * (v_vals - v_env_vals)
    coriolis_v = -f * (u_vals - u_env_vals)

    # combined magnitude
    entrainment_mag = np.sqrt(entrainment_u ** 2 + entrainment_v ** 2)
    surfaceflux_mag = np.sqrt(surfaceflux_u ** 2 + surfaceflux_v ** 2)
    coriolis_mag = np.sqrt(coriolis_u ** 2 + coriolis_v ** 2)
    v_mag = np.sqrt(v_vals ** 2 + u_vals ** 2)
    #sum of the fluxes
    fluxsum = entrainment_mag - surfaceflux_mag
    return {
        #"E": E_vals,
        #"sflux_u": sflux_u_vals,
        #"sflux_v": sflux_v_vals,
        #"entrainment_u": entrainment_u,
        #"entrainment_v": entrainment_v,
        #"surfaceflux_u": surfaceflux_u,
        #"surfaceflux_v": surfaceflux_v,
        #"coriolis_u": coriolis_u,
        #"coriolis_v": coriolis_v,
        "coriolis (m/s)": coriolis_mag,
        "v_mag (m/s)": v_mag,
        "entrainment (m/s)": entrainment_mag,
        "surfaceflux (m/s)": surfaceflux_mag,
        "Sum of fluxes (m/s)": fluxsum
    }
def PlotDiagnostics(times, diag_dict, filename, nrows=2):
    fig, axs = make_grid(len(diag_dict), nrows=nrows)

    for ax, (label, values) in zip(axs, diag_dict.items()):
        ax.plot(times / 3600.0, values)
        ax.set_ylabel(label)
        ax.set_xlabel("hours since sunrise")
        ax.set_xlim([0, None])
        ax.spines["left"].set_position(("axes", -0.01))
        ax.spines["bottom"].set_position(("axes", -0.01))
        ax.xaxis.set_major_locator(MultipleLocator(12))
        ax.grid(axis="x", which="major", linestyle="--", linewidth=0.5, alpha=0.6)

    plt.tight_layout(pad=0.1)
    plt.savefig(filename + ".pdf", bbox_inches="tight")
    plt.show()
    return fig, axs


def PlotDiagnosticsMultiRun(times, diag_runs, varnames, filename, nrows=2):
    fig, axs = make_grid(len(varnames), nrows=nrows)

    for ax, varname in zip(axs, varnames):
        for run_label, diag in diag_runs.items():
            ax.plot(times / 3600.0, diag[varname], label=run_label)
        ax.set_ylabel(varname)
        ax.set_xlabel("hourse since sunrise")
        ax.set_xlim([0, None])
        ax.spines["left"].set_position(("axes", -0.01))
        ax.spines["bottom"].set_position(("axes", -0.01))

    axs[-1].legend(loc="best")
    plt.tight_layout(pad=0.1)
    plt.savefig(filename + ".pdf", bbox_inches="tight")
    plt.show()
    return fig, axs

def make_grid(num_plots, nrows=2, ax_width=3.5, ax_height=3):
    ncols = math.ceil(num_plots / nrows)
    fig, axs = plt.subplots(
        nrows, ncols,
        figsize=(ncols * ax_width, nrows * ax_height),
        squeeze=False,
    )
    axs = axs.ravel()
    for ax in axs[num_plots:]:
        ax.set_visible(False)
    return fig, axs[:num_plots]