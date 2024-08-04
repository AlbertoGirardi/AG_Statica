import numpy as np
from .auxiliary import *



class Force():

    """GENERIC CLASS FOR A FORCE
  implements api with __call__
  to get the force value simply the force object is called
  do not use directly"""
    
    plottable = False
    color = 'b'

    def __call__(self, body, t, u):
        return self.calculateForce(body, t, u)
  
    def calculateForce(self):
        #just placeholder
        raise NotImplementedError("This class should never be used directly")




class ConstantForceB(Force):
    """
    Class for a constant force an pure torque applied at the barycenter
    """

    def __init__(self, force):
      
        """force: 3 element ARRAY:  [Fx, Fy, M]"""

        self.force = force
        # print (np.shape(force))
        if np.shape(force) != (3,):
            raise ValueError("Incorrect dimensions of the force vector")

    def calculateForce(self, body, t, u):
     
     return self.force





class ConstantForce(Force):
    """
    Class for a constant force applied at a given point of the body
    """

    def __init__(self, force, arm):
      
        """force: 2 element ARRAY:  [Fx, Fy], absolute coordinates
           arm: vector 2d that is the application point of the force in the local body coordinates"""

        self.force = force
        self.arm = arm
        # print (np.shape(force))
        if np.shape(force) != (2,):
            raise ValueError("Incorrect dimensions of the force vector")

    def calculateForce(self, body, t, u):
     
        alpha = u[2]
        return ForceTorque(self.force, self.arm, alpha)

    




class ForceGravity(ConstantForceB):
  
  """
  Applies gravity to the body
  
  """
   
  def __init__(self):
     pass
  
  def calculateForce(self, body, t, u):
    return np.array([0, body.universe.g*body.mass, 0])
  




class Spring(Force):

    """CLASS FOR A 2D SPRING
        exerts a force based on Hook Law
       
        """
   
    def __init__(self, k, l0,  abs_attachment, local_attachment):
      
      """
        k: spring constant [N/m]
        l0: length of the spring at rest [m]
        abs_attachment: point in the global coordinate space where spring is attached [2d vector]
        local_attachment: point in the local (body) coordinate space where spring is attached [2d vector] 

      
      """
      self.k = k
      self.L0 = l0
      self.attachment1 = abs_attachment
      self.attachmentBody = local_attachment
      self.plottable = True
      self.color = 'y'

    #   print(self.attachment1)
    #   print(self.L0)


    def calculateForce(self, body, t, u):

        #RETURNS FORCE VECTOR OF THE SPRING

        d = coord_transform_local_to_abs_u(self.attachmentBody, u)  - self.attachment1                       #vector that rapresents spring direction
        # print(u[:2])
        L = np.linalg.norm(d)                               #lenght of the spring

        if L == 0:  
           #if the lenght of the spring is 0, it is impossible to predict in which direction it will exert a force
           raise RuntimeError("Singularity: unpredictable future")

        dL = ( L - self.L0 )                                #spring contraction/extension

        print(dL)
        # print(L)
        d_ = d/abs(L)                                       #versor of spring force

        F = (- self.k * dL* d_)                             #HOOK LAW, returning vector force

        # print(dL, F[0])
        # print(F, np.linalg.norm(F) - dL*self.k )   #test that is correct
        return ForceTorque(F, self.attachmentBody, u[2])
       
    def plot(self, q, u):

        attachment2 = coord_transform_local_to_abs_u(self.attachmentBody, u) - self.attachment1

        q.set_UVC( attachment2[0], attachment2[1])





class Dampner(Force):

    """
    Exerts a damping force proportional to the relative speed
    """


    def __init__(self, b, abs_attachment, local_attachment):

        """
        b: constant of proportionality between speed and force 

        abs_attachment: point in the global coordinate space where spring is attached [2d vector]
        local_attachment: point in the local (body) coordinate space where spring is attached [2d vector] 
        """

        self.b  = b
        self.attachment1 = abs_attachment
        self.attachmentBody = local_attachment   
        self.plottable = True
        self.color = 'r'



    def calculateForce(self, body, t, u):

        #returns the dampner force in vector form

        d = coord_transform_local_to_abs_u(self.attachmentBody ,u)  - self.attachment1           #vector rapresenting dampner

        v = velocity_transform_loc_to_abs(u[3:5], u[2], u[5], self.attachmentBody)         #velocity of body attachment point respect to dampner attachment  

        # print(u[:2])
        L = np.linalg.norm(d)           #lenght of dampner
        d_ = d/abs(L)                   #versor of  force direction

        
        if L == 0:  
           #if the lenght of the spring is 0, it is impossible to predict in which direction it will exert a force
           raise RuntimeError("Singularity: unpredictable future")


        vL = d_@v                       #velocity in the direction of the dampner

        f = vL * self.b                 #calculate force magnitude

        F = - d_ * f                    #calculate force vector 
        
        return ForceTorque(F, self.attachmentBody, u[2])
    

    def plot(self, q, u):

        attachment2 = coord_transform_local_to_abs_u(self.attachmentBody, u)

        q.set_UVC( attachment2[0], attachment2[1])

