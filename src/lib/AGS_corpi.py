import numpy as np
from . import GUI
from .auxiliary import *



#classe base per un corpo


class Corpo():
    
    def __init__(self, mass, position, velocity):

        """mass: float [kg] 
           position and velocity: numpy arrays, 2 dimensions
        """

        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.u0 = np.concatenate((self.position, self.velocity))
        self.forces = []

        self.g = 0   #gravitational acceleration

    
    def addForce(self, force_list):
        self.forces.append(force_list)


    def accelerationX(self, t, u):
        return 0
    
    def accelerationY(self, t, u):
        return self.g




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

