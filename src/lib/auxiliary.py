import numpy as np
import os

import matplotlib.pyplot as plt


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



   
def coord_transform_loc_to_abs(local_coord, local_origin_abs, angle):

    """
    Transforms a local coordinate into absolute frame of reference
    local_origin: origin of the local system 2d vector, in abs coordinates
    angle: orientatio of the local system
    
    """
    
    Rot = rotation_matrix2D(angle)

    s = Rot@local_coord

    return s + local_origin_abs



def coord_local_to_abs_u(loc_c, u):
   
   """
   Transforms a local coordinate into absolute frame of reference
   u: state vector
   """
   
   return coord_transform_loc_to_abs(local_coord=loc_c, local_origin_abs=u[:2], angle=u[2])



def velocity_transform_loc_to_abs(v_orgin, alpha,  omega, sigma):

    """
    calculates the velocity of a point given its position in the local coords, the velocity and rotation, angular velocity of the body
    
    v_origin: 2d vector, velocity of local frame origin
    alpha: rotation of the local frame respect to absolute
    omega: angular velocity of body
    sigma: position of the point in local frame

    
    """

    Rot = rotation_matrix2D(alpha)                          #rotation matrix to calculate position vector in abs coord (only in orientation)
    s = Rot@sigma                                           #calculate the position vector in abs coord, origin = body barycenter

    sT = rotmT@s                                        #vector perpendicular to original
    v_a = v_orgin + omega * sT                         #calculate velocity, summing the component of the barycenter and the tangetial velocity
    

    # fig, ax = plt.subplots()
    # scale = 4
    # ax.set(xlim=[-scale, scale], ylim=[-scale, scale], xlabel='X[m]', ylabel='Y [m]') 
    # ax.set_aspect('equal', adjustable='box')
    # plt.quiver(0, 0, sigma[0], sigma[1], angles='xy', scale_units='xy', scale=1, color='r')
    # plt.quiver(0, 0, s[0], s[1], angles='xy', scale_units='xy', scale=1, color='b')
    # plt.quiver(s[0], s[1], sT[0], sT[1], angles='xy', scale_units='xy', scale=1, color='g')
    # plt.quiver(0,0, v_a[0], v_a[1], angles='xy', scale_units='xy', scale=1, color='y')
    # plt.quiver(0,0, v_orgin[0], v_orgin[1], angles='xy', scale_units='xy', scale=1, color='g')
    # plt.grid(True)
    # plt.show()

    return v_a




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

        d = coord_local_to_abs_u(self.attachmentBody, u)  - self.attachment1                       #vector that rapresents spring direction
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
       
    def plot(self, q, u):

        attachment2 = coord_local_to_abs_u(self.attachmentBody, u)

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

        d = coord_local_to_abs_u(self.attachmentBody ,u)  - self.attachment1           #vector rapresenting dampner

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

        attachment2 = coord_local_to_abs_u(self.attachmentBody, u)

        q.set_UVC( attachment2[0], attachment2[1])







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
    # print(rotation_matrix2D(np.pi/2))


    print(velocity_transform_loc_to_abs(v_orgin=np.array([0,0]), alpha=np.pi, omega=1, sigma=np.array([1,0])))

