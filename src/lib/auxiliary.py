import numpy as np
import os

import matplotlib.pyplot as plt
from scipy.special import ellipj

from   scipy.integrate import solve_ivp


#(- self.k / (np.linalg.norm(u[:2])**2)) *(u[:2])     #1D GRAVITY LAW

rotmT = np.array([[0, -1], [1,0]])          #rotation matrix for perpendicular vector

#useful matrixes
IdentityMtx = np.diag([1,1])
NullMtx = np.diag([0,0])


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
   #! REDO FOR MULTIPLE BODIES!
   return coord_transform_loc_to_abs(local_coord=loc_c, local_origin_abs=u[:2], angle=u[2])



def velocity_transform_loc_to_abs(v_orgin, alpha,  omega, sigma=np.zeros(2), debug=False):

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
    # print('fatto')
    return v_a



def velocity_transform_loc_to_abs_u(u, sigma=np.zeros(2), debug=False):

    return velocity_transform_loc_to_abs(v_orgin=u[:2], alpha=u[2], omega=u[5], sigma=sigma)







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



def pendulum_exact_solution(m,g, dOG ,JO, tsol):

    class physic_pendulum:
        def __init__(self,  omega):
            self.omega = omega
        
        def __call__(self, t, u):
            phi, dphi = u
            ddphi = -self.omega**2 * np.sin(phi)
            return [dphi, ddphi]

    # condizioni iniziali
    phi0  = np.pi/6 # angolo rispetto alla vericale
    dphi0 = 0       # velocità di rotaziones

    # modello matematico
    # oggetto con polo fisso soggetto a gravità

    # JO*ddphi + m*g*dOG*sin(phi) = 0
    # JO momento d'inezia rispetto al punto di sospendita JO = JG + dOG^2*m
    # m massa
    # dOG distanza tra il centro di massa e la cerniera
    # si può scrivere anche come
    # ddphi = - (m*g*dOG/JO)*sin(phi)
    # w^2   = (m*g*dOG/JO) frequenza naturale pendolo fisico

    JO = 1 #kgm^2
    g = 9.81 # m/s^2 
    dOG = 1 # m lunghezza pendolo fisico fino al baricentro
    m = 1 # kg massa pendolo fisico
    omegac = np.sqrt(m*dOG*g/JO)




    u0 = np.array([phi0,dphi0])
    # metodo Runge Kutta predictor corrector 4/5 ordine
    sol = solve_ivp(physic_pendulum(omega=omegac), [0, T], u0 , method='RK45', t_eval=tsol)


    s0 = 0*tsol
    asol = s0
    wsol = s0

    return np.vstack((s0, s0, asol, s0, s0, wsol))




def pendulum_linear_solution(m,g,phi0, dOG ,JO, tsol):

    """
    Calculates the 
      JO: moment of inertia of the pendulum from the pivot point:  kgm^2
      dOG: distance from the barycenter of the pendulum from the pivot: m
      m: mass of the pendulum: kg
      tsol: array of moments of time at which to calculate the solution
      phi0: angle to the vertical
    # """

    # condizioni iniziali
   
    dphi0 = 0       # velocità di rotaziones

    # modello matematico
    # oggetto con polo fisso soggetto a gravità

    # JO*ddphi + m*g*dOG*sin(phi) = 0
    # JO momento d'inezia rispetto al punto di sospendita JO = JG + dOG^2*m
    # m massa
    # dOG distanza tra il centro di massa e la cerniera
    # si può scrivere anche come
    # ddphi = - (m*g*dOG/JO)*sin(phi)
    # w^2   = (m*g*dOG/JO) frequenza naturale pendolo fisico


    omegac = np.sqrt(m*dOG*g/JO)



 
    asol =   phi0*np.cos(omegac*tsol) + dphi0/omegac*np.sin(omegac*tsol) + 3/2*np.pi
    wsol = -omegac*phi0*np.sin(omegac*tsol) + dphi0*np.cos(omegac*tsol)

    xsol = dOG * np.cos(asol)
    ysol = dOG * np.sin(asol)

    vsol = [velocity_transform_loc_to_abs(v_orgin=dOG*wsol[n_], alpha=asol[n_], omega=wsol[n_]) for n_ in range(len(tsol))]
    print(vsol[0])
    vxsol = [sol[0] for sol in vsol]
    vysol = [sol[1] for sol in vsol]

    # vxsol = xsol*0
    # vysol = xsol*0

    return np.vstack((xsol, ysol, asol,vxsol, vysol, wsol))

def RMSE(x,xsol):
    N = np.size(x)
    return np.sqrt(1/N*np.sum((x - xsol)**2))   





