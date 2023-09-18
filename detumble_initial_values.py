from variables import *
import numpy as np
import matplotlib.pyplot as plt

def set_initial_rotational_speed():
    rotational_speed_x=np.random.normal(0.0,40,1)
    rotational_speed_y=np.random.normal(0.0,40,1)
    rotational_speed_z=np.random.normal(0.0,40,1)