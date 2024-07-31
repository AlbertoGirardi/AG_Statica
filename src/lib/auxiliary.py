import numpy as np



#(- self.k / (np.linalg.norm(u[:2])**2)) *(u[:2])     #1D GRAVITY LAW

def rotation_matrix2D(alfa):

    """returns a rotation matrix for the given angle in radiants"""
    
    RM2D= [[np.cos(alfa),-np.sin(alfa)],
      [np.sin(alfa),np.cos(alfa)]]
    return RM2D



def MRUA(tsol, x0, y0, vx0, vy0, ax, ay, a0, w0, e):
   
    xsol = x0 + vx0*tsol + 0.5*ax*tsol**2
    ysol = y0 + vy0*tsol + 0.5*ay*tsol**2

    vxsol = vx0 + ax*tsol
    vysol = vy0 + ay*tsol

    asol = a0 + w0*tsol + 0.5*e*tsol**2

    wsol = w0 + e*tsol

    return np.vstack((xsol, ysol, asol, vxsol, vysol, wsol))                       #unione delle soluzioni calcolate in una matrice formata da una serie di vettori di stato
                                                                            #per ogni istante di tempo




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
  


class Spring(Force):
   
    def __init__(self, k, l0,  abs_attachment, local_attachment):

      self.k = k
      self.L0 = l0
      self.attachment1 = abs_attachment
      self.attachmentBody = local_attachment
      print(self.attachment1)
      print(self.L0)

    def calculateForce(self, body, t, u):
        
        d = u[:2] - self.attachment1
        print(u[:2])
        L = np.linalg.norm(d)

        if L == 0:
           raise RuntimeError("Singularity: unpredictable future")

        dL = ( L - self.L0 )     #spring contraction/extension


        # print(L)
        L_ = d/abs(L)                   #versor of spring force

        F = (- self.k * dL* L_)                 #HOOK LAW

        # print(dL, F[0])
        # print(F, np.linalg.norm(F) - dL*self.k )   #test that is correct
        return np.concatenate([F, [0]])
       

class Dampner(Force):

    def __init__(self, k):
       self.k  = k
      


if __name__ == '__main__':   
   
    #test code
    pass
