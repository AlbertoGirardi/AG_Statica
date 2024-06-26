import numpy as np
from . import GUI
from .auxiliary import *



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
    def __init__(self, mass, position, rotation_angle , velocity, angular_velocity, shape ,inertia):

        """
        for polygon shape body
        shape: nx2 matrix, containing all the vertexes, x coord in first row, y coord second row"""
        super().__init__(mass, position, velocity)
        self.shape = shape
        self.rotation_angle = rotation_angle
        self.angular_velocity = angular_velocity


    def draw(self, plot):
        GUI.draw_polygon(plot, self.shape, self.rotation_angle, self.position )


    def run_Physics(self):
        
        step = 0.05
        stop = 5
        start = 0
        t = list([start + i * step for i in range(int((stop - start) / step) + 1)])
        
        angles = list(map(lambda t: self.angular_velocity*t, t))

        print(angles)
        return(angles)
