import numpy as np


def rotation_matrix2D(alfa):

    """returns a rotation matrix for the given angle in radiants"""
    
    RM2D= [[np.cos(alfa),-np.sin(alfa)],
      [np.sin(alfa),np.cos(alfa)]]
    return RM2D




class Force():

  """GENERIC CLASS FOR A FORCE
  implements api with __call__
  to get the force value simply the force object is called
  do not use directly"""
    
  def __call__(self, body, t, u):
    return self.calculateForce(body, t, u)
  
  def calculateForce(self):
    #just placeholder
    raise NotImplementedError("This class should never be used directly")


class ConstantForce(Force):
   

  def __init__(self, force):
      
      """force: 3 element ARRAY:  [Fx, Fy, M]"""

      self.force = force
      print (np.shape(force))
      if np.shape(force) != (3,):
         raise ValueError("Incorrect dimensions of the force vector")

  def calculateForce(self, body, t, u):
     
     return self.force
  


class ForceGravity(ConstantForce):
   
  def __init__(self):
     pass
  
  def calculateForce(self, body, t, u):
    return np.array([0, body.universe.g*body.mass, 0])
  



if __name__ == '__main__':   
   
    #test code
   f= ConstantForce(np.array([3,2,0]))
   print(f())