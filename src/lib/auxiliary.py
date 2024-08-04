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



   
def coord_transform_loc_to_abs(local_coord, local_origin_abs, angle, debug=False):

    """
    Transforms a local coordinate into absolute frame of reference
    local_origin: origin of the local system 2d vector, in abs coordinates
    angle: orientatio of the local system
    
    """
    
    Rot = rotation_matrix2D(angle)

    s = Rot@local_coord

    r = s + local_origin_abs

    if debug:
        fig, ax = plt.subplots()
        scale = 7
        ax.set(xlim=[-scale, scale], ylim=[-scale, scale], xlabel='X[m]', ylabel='Y [m]') 
        ax.set_aspect('equal', adjustable='box')
        plt.quiver(local_origin_abs[0], local_origin_abs[1], local_coord[0], local_coord[1], angles='xy', scale_units='xy', scale=1, color='r', label='sig')
        plt.quiver(local_origin_abs[0], local_origin_abs[1], s[0], s[1], angles='xy', scale_units='xy', scale=1, color='b', label='s')
        plt.quiver(0,0, local_origin_abs[0], local_origin_abs[1], angles='xy', scale_units='xy', scale=1, color='y', label='rO')
        
        plt.quiver(0,0, r[0], r[1], angles='xy', scale_units='xy', scale=1, color='y', label='rA')

        plt.legend()
        plt.grid(True)
        fig.savefig(get_incremental_filename('data\\plots', 'test_velocity_transform    ', 'png'), dpi = 200)

        plt.show()

    return  r



def coord_transform_local_to_abs_u(loc_c, u):
   
   """
   Transforms a local coordinate into absolute frame of reference
   u: state vector
   """
   return coord_transform_loc_to_abs(local_coord=loc_c, local_origin_abs=u[:2], angle=u[2])



def velocity_transform_loc_to_abs(v_orgin, alpha,  omega, sigma, debug=False):

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
    v_s = omega * sT                                    #velocity of point relative to barycenter
    v_a = v_orgin +  v_s                        #calculate velocity, summing the component of the barycenter and the tangetial velocity
    
    if debug:
        fig, ax = plt.subplots()
        scale = 7
        ax.set(xlim=[-scale, scale], ylim=[-scale, scale], xlabel='X[m]', ylabel='Y [m]') 
        ax.set_aspect('equal', adjustable='box')
        plt.quiver(0, 0, sigma[0], sigma[1], angles='xy', scale_units='xy', scale=1, color='r', label='sig')
        plt.quiver(0, 0, s[0], s[1], angles='xy', scale_units='xy', scale=1, color='b', label='s')
        plt.quiver(s[0], s[1], sT[0], sT[1], angles='xy', scale_units='xy', scale=1, color='g', label='sT')
        plt.quiver(0,0, v_a[0], v_a[1], angles='xy', scale_units='xy', scale=1, color='y', label='v')
        plt.quiver(0,0, v_orgin[0], v_orgin[1], angles='xy', scale_units='xy', scale=1, color='k', label='vO')
        plt.quiver(v_orgin[0], v_orgin[1], v_s[0], v_s[1], angles='xy', scale_units='xy', scale=1, color='c', label='v_s')

        plt.legend()
        plt.grid(True)
        fig.savefig(get_incremental_filename('data\\plots', 'test_velocity_transform    ', 'png'), dpi = 200)

        plt.show()

    return v_a









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


    # print(velocity_transform_loc_to_abs(v_orgin=np.array([4,3]), alpha=np.pi/2, omega=2, sigma=np.array([1,1/2])))
    print(coord_transform_loc_to_abs(np.array([1,0]), local_origin_abs=np.array([5,4]), angle=2 ,debug=True))

