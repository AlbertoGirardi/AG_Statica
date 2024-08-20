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
        self.f_mass = 10000*max([b.mass for b in self.bodies])                  #fictitious mass

        self.f_T = 0.001                                                      #fictitious natural period
        self.f_w = round(np.pi*2/self.f_T,1)

        print( f"omega: {self.f_w}, damp: {self.f_damp}, mass: {self.f_mass}"  )



    def Jacobian(self, u):

        s = []

        for n, sigma in enumerate(self.attachments):

            s.append(coord_transform_loc_to_abs(sigma, np.zeros(2), u[6*n+2]))            #from local non rotated to local rotated

        # print(s)


        J = np.array(  [[ 1, 0, -s[0][1], -1, 0, +s[1][1]],              
                        [ 0, 1, +s[0][0], 0, -1, -s[1][0]]]
        )

        # print(J)

        return J
    

    def dJacobian(self, u):

        sP = [None, None]

        for n, b in enumerate(self.bodies):

            sP[n] = rotmT @ velocity_transform_loc_to_abs(np.zeros(2), u[n*6+2],omega=u[n*6+5], sigma=self.attachments[n])
            #calculates the vector perpendicular to the velocity of the attachment point


        # print(sP)

        dJ = np.column_stack((NullMtx, sP[0], -NullMtx, -sP[1]))

        # print(dJ)
        return dJ
    

    def g(self, u):

        g = coord_transform_local_to_abs_u(self.attachments[0], u[:6]) - coord_transform_local_to_abs_u(self.attachments[1], u[6:])

        return g


    def dg(self, u):

        dg = velocity_transform_loc_to_abs_u(u[:6], self.attachments[0]) - velocity_transform_loc_to_abs_u(u[6:], self.attachments[1])
        return dg

        


        





        