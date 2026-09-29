# List  of the environmental, free troposphere conditions
import numpy as np
from parameters import *


# Linear profiles
def w_env(z):
    return divergence * z


def s_env(z):
    return s_00 + gamma_s * z


def q_env(z):
    return q_00 + gamma_q * z


def u_env(z):
    return (u_g + gamma_u * z)

def v_env(z):
    return (v_g + gamma_v * z)


# To test this module
def test():
    print(w_env(1000.0))


if __name__ == "__main__":
    test()
