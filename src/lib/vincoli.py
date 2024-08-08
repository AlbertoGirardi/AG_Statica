import numpy as np
from .AGS_corpi import *
from .auxiliary import *

class Cerniera():
    
    def __init__(self, bodies, attachments):

        if len(bodies) != 2:
            raise RuntimeError("Two bodies are involved in a constraint!")
        
        if len(attachments) != 2:
            raise RuntimeError("Two attachments must be provided!")
        
        #!TODO check all the sizes of the vectors are correct!
        #!TODO the bodies must be given in the same order as in the universe!
        

        self.bodies = bodies
        self.attachments =  attachments


        #determining fictitious parameters using rule of thumb

        self.f_damp = 1             #damping
        self.f_mass = 1000*max([b.mass for b in self.bodies])                  #fictitious mass

        self.f_T = 0.3                                                      #fictitious natural period
        self.f_w = np.pi*2/self.f_T

        print(self.f_w, self.f_damp, self.f_mass)



    def Jacobian(self, u):

        s = []

        for n, sigma in enumerate(self.attachments):

            s.append(coord_transform_loc_to_abs(sigma, np.zeros(2), u[n+2]))

        print(s)


        J = np.array(  [[ 1, 0, -s[0][1], -1, 0, +s[1][1]],              
                        [ 0, 1, +s[0][0], 0, -1, -s[1][0]]]
        )

        print(J)

        return J


        





        