import numpy as np
from . import GUI
from .auxiliary import *



#classe base per un corpo



class Rigido():

    def __init__(self, mass, inertia, position, rotation_angle=0 , velocity=np.zeros(2), angular_velocity=0 , shape= np.array([[1,0,-1,1], [0,1,0,0]]) ):

        """
        CLASS FOR A GENERAL BODY IN 2 DIMENSIONS,

        handles all the mathematics 
        
        for polygon shape body
        shape: nx2 matrix, containing all the vertexes, x coord in first row, y coord second row"""
        self.shape = shape
        self.rotation_angle = rotation_angle
        self.angular_velocity = angular_velocity


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





class Point_mass(Rigido):

    """classe per punto materiale, con la stessa trattazione matematica del rigido ma rotazione forzata a 0 """
    
    def __init__(self, mass, position, velocity):
        super().__init__(mass=mass, inertia=1, position=position, rotation_angle=0, velocity=velocity, angular_velocity=0, shape=np.array([0,0]) )
