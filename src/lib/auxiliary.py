import numpy as np


def rotation_matrix2D(alfa):

    """returns a rotation matrix for the given angle in radiants"""
    
    RM2D= [[np.cos(alfa),-np.sin(alfa)],
      [np.sin(alfa),np.cos(alfa)]]
    return RM2D
