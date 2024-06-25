import numpy as np
from . import GUI


def rotation_matrix2D(alfa):
    
    RM2D= [[np.cos(alfa),-np.sin(alfa)],
      [np.sin(alfa),np.cos(alfa)]]
    return RM2D

#classe base per un corpo

class Corpo():
    
    def __init__(self, mass, position, velocity):

        """mass: float [kg] 
           position and velocity: numpy arrays, 3 dimensions
        """
        self.mass = mass
        self.position = position
        self.velocity = velocity




class Point_mass(Corpo):
    
    def __init__(self, mass, position, velocity):
        super().__init__(mass, position, velocity)

    def draw(self):
        pass


class Rigido(Corpo):
    def __init__(self, mass, position, rotation_angle , velocity, shape ,inertia):

        """
        for polygon shape body
        shape: nx2 matrix, containing all the vertexes, x coord in first row, y coord second row"""
        super().__init__(mass, position, velocity)
        self.shape = shape
        self.rotation_angle = rotation_angle

    def draw(self):
        GUI.draw_polygon(self.shape, self.rotation_angle, self.position )
