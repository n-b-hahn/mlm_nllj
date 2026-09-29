import numpy as np
from environment import *
from surface import *
from entrainment import *
import globals as gs


# Define of ordinary differential equations
def dh_dt(t, state):
    h = state[gs.idx_h]
    dh = gs.E(t, state) + w_env(h)
    return dh


def ds_dt(t, state):
    h = state[gs.idx_h]
    s = state[gs.idx_s]
    ds = (gs.E(t, state) * (s_env(h) - s) + gs.sflux_s(t, state)) / h
    return ds


def dq_dt(t, state):
    h = state[gs.idx_h]
    q = state[gs.idx_q]
    dq = (gs.E(t, state) * (q_env(h) - q) + gs.sflux_q(t, state)) / h
    return dq

def du_dt(t, state):
    h = state[gs.idx_h]
    v = state[gs.idx_v]
    u = state[gs.idx_u]
    du = (gs.E(t, state) * (u_env(h) - u) + gs.sflux_u(t, state))/h +(f*(v-v_env(h)))
    return du

def dv_dt(t, state):
    h = state[gs.idx_h]
    v = state[gs.idx_v]
    u = state[gs.idx_u]
    dv = (gs.E(t, state) * (v_env(h) - v) + gs.sflux_v(t, state))/ h -(f*(u-u_env(h)))
    return dv


# To test this module
def test():
    print("to be done")


if __name__ == "__main__":
    test()
