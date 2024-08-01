import numpy as np
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
        self.inertia = inertia
        self.position = position
        self.velocity = velocity
        
        # print(self.u0)
        self.forces = []

        self.universe = None    #univers of which the body is part, used for comunicating general parameters 

       




    def addForce(self, force_list):

        """adds a list of given forces to the list of total forces"""
        self.forces.extend(force_list)



    

    def Force(self, t, u):

        """returns an array of the total forces and torques applied to the body
        [Fx, Fy, M]
        """

        resultingForce = np.zeros(3)

        for force in self.forces:

            resultingForce += force(self, t, u)
            

        return resultingForce







class Point_mass(Rigido):

    """classe per punto materiale, con la stessa trattazione matematica del rigido ma rotazione forzata a 0 """
    
    def __init__(self, mass, position, velocity):
        super().__init__(mass=mass, inertia=1, position=position, rotation_angle=0, velocity=velocity, angular_velocity=0, shape=np.array([0,0]) )
