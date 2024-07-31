import numpy as np
import os



#(- self.k / (np.linalg.norm(u[:2])**2)) *(u[:2])     #1D GRAVITY LAW

rotmT = np.array([[0, -1], [1,0]])          #rotation matrix for perpendicular vector


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



def TorqueVarignon(f, r):
    
    """
    Given a force f applied with arm r (absolute coordinates) calculates the TORQUE
    """
    
    rT = rotmT@r

    M = rT@f
    
    return M



def ForceTorque(f, r, alfa):

    """returns force-torque vector given force and arm and rotation angle"""
   
    Rot = rotation_matrix2D(alfa)
    return np.concatenate([f, [TorqueVarignon(f, Rot@r)]])



   

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
        local_attachment: point in the local (body) coordinate space where spring is attached [2d vector] #TODO 

      
      """
      self.k = k
      self.L0 = l0
      self.attachment1 = abs_attachment
      self.attachmentBody = local_attachment
    #   print(self.attachment1)
    #   print(self.L0)



    def calculateForce(self, body, t, u):

        #RETURNS FORCE VECTOR OF THE SPRING

        d = u[:2]  - self.attachment1                       #vector that rapresents spring direction
        # print(u[:2])
        L = np.linalg.norm(d)                               #lenght of the spring

        if L == 0:  
           #if the lenght of the spring is 0, it is impossible to predict in which direction it will exert a force
           raise RuntimeError("Singularity: unpredictable future")

        dL = ( L - self.L0 )                                #spring contraction/extension


        # print(L)
        d_ = d/abs(L)                                       #versor of spring force

        F = (- self.k * dL* d_)                             #HOOK LAW, returning vector force

        # print(dL, F[0])
        # print(F, np.linalg.norm(F) - dL*self.k )   #test that is correct
        return ForceTorque(F, self.attachmentBody, u[2])
       


class Dampner(Force):

    """
    Exerts a damping force proportional to the relative speed
    """


    def __init__(self, b, abs_attachment, local_attachment):

        """
        b: constant of proportionality between speed and force 

        abs_attachment: point in the global coordinate space where spring is attached [2d vector]
        local_attachment: point in the local (body) coordinate space where spring is attached [2d vector] #TODO 
        """

        self.b  = b
        self.attachment1 = abs_attachment
        self.attachmentBody = local_attachment   


    def calculateForce(self, body, t, u):

        #returns the dampner force in vector form

        d = u[:2]  - self.attachment1           #vector rapresenting dampner
        v = u[3:5]                                #velocity of body respect to dampner attachment

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







def get_incremental_filename(base_dir, base_name, ext):

    """
    base_dir: directory
    base_name: fine name
    ext: extension of file
    returns "directory/base_name[n].ext"  with n is a number to version files
 
    """
    i = 1
    while True:
        filename = f"{base_name}_{i}.{ext}"
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1



if __name__ == '__main__':   
   
    #test code
    print(rotation_matrix2D(np.pi/2))

