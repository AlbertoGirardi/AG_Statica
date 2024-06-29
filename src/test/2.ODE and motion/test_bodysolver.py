

import numpy as np
import matplotlib.pyplot as plt


def plot_pos_vel_xy(sol_d, tsol, sol_a):

    """PLOTS X, Y POSITION, X,Y VELOCITY against time
    and position in XY plane
    
    sol_d: scipy solver solution, in the form of state vector  [x,y,vx,vy]
    sol_a: solution to compare to, in the form of state vector
    tsol: array of time istants for which solution has been calculated
    """
    fig,ax = plt.subplot_mosaic([['x', 'y', 'xy'], ['vx', 'vy', 'xy']])    
    fig.suptitle('2 MOLLE SU CARRELLI con RK45')
    fig.set_size_inches(12,6)

    #x position

    ax['x'].plot(sol_d.t, sol_d.y[0,:],'+r',label = 'RK45')
    ax['x'].plot(tsol, sol_a[0,:],'-b',label = 'exact')
    ax['x'].legend( bbox_to_anchor=(-0.1, 1))
    ax['x'].set_xlabel("t [s]")
    ax['x'].set_ylabel("x [m]")
        
    #y position
    ax['y'].plot(sol_d.t, sol_d.y[1,:],'+r',label = 'RK45')
    ax['y'].plot(tsol, sol_a[1,:],'-b',label = 'exact')
    ax['y'].set_xlabel("t [s]")
    ax['y'].set_ylabel("y [m]")

    #x velocity

    ax['vx'].plot(sol_d.t, sol_d.y[2,:],'+r',label = 'RK45')
    ax['vx'].plot(tsol, sol_a[2,:],'-b',label = 'exact')
    ax['vx'].set_xlabel("t [s]")
    ax['vx'].set_ylabel("vx [m]")
    ax['vx'].set_title("velocity x")


    #y velocity
    ax['vy'].plot(sol_d.t, sol_d.y[3,:],'+r',label = 'RK45')
    ax['vy'].plot(tsol, sol_a[3,:],'-b',label = 'exact')
    ax['vy'].set_xlabel("t [s]")
    ax['vy'].set_ylabel("vy [m]")
    ax['vy'].set_title("velocity y")



    #plotting the movement on the xy plane
    ax['xy'].grid(True)
    ax['xy'].set_aspect('equal', adjustable='box')
    ax['xy'].plot(sol_d.y[0,0],  sol_d.y[1,0] , 'og', label = "start")  
    ax['xy'].plot(sol_d.y[0,:], sol_d.y[1,:] , '+g', label = 'traiettoria RK')
    ax['xy'].plot(0,0,  'or')  #marking origin

    ax['xy'].plot(sol_a[0,:], sol_a[1,:] , label = 'traiettoria a')

    ax['xy'].legend(bbox_to_anchor=(0.5, 1.35))
    ax['xy'].set_title("POSITION in XY PLANE")

    fig.tight_layout()
    plt.show()




def elinfty(x,xsol):
    return np.max(np.abs(x - xsol))
def RMSE(x,xsol):
    N = np.size(x)
    return np.sqrt(1/N*np.sum((x - xsol)**2))   





def spring_acceleration(omega, deltax):

    """returns the acceleration of a system of a mass tied to a spring,  omega: constant omega,  deltax: displacement of the spring"""

    return - (omega**2 * deltax)





class Dynamic_system():

    """CLASSE PER UN SISTEMA DINAMICO DI 1 CORPO
     rappresentato da un punto materiale sul piano XY, dal vettore di stato. Questa classe non si utilizza direttamente, ma si eredita da questa
    non overload __call__
     NECESSARY TO DEFINE  self.accelerationX(t, u) and self.accelerationY(t, u) in child class """

    def __init__(self):
        pass


    def __call__(self, t, u):

        
        """dato il vettore di stato u [x,y,vx,vy] e il tempo restituisce il vettore FLUSSO[vx, vy, ax, ay], calcolando l'accelerazione subita

        """

        x, y, vx, vy = u                        #spacchettamento vettore di stato
        dx = vx                                 #dummy 
        dy = vy
        dvx = self.accelerationX(t, u)          #ottiene accelerazione del corpo nelle due direzioni
        dvy = self.accelerationY(t, u)
        return [dx, dy, dvx, dvy]               #ritorna il vettore FLUSSO

    



class mass_2spring(Dynamic_system):

    """CLASSE PER CORPO VINCOLATO DA DUE MOLLE SU CARRELLI

    omegax: valore costante omega per molla asse x;
    omegay: valore costante omega per molla asse y
    """
    def __init__(self,  omegax, omegay):
        self.omegax = omegax
        self.omegay = omegay

    def accelerationX(self, t, u):

        """acceleration of the system in X direction, t:time,  u: state vector"""
        x, y, vx, vy = u

        return spring_acceleration(self.omegax, x)


    def accelerationY(self, t, u):
        x, y, vx, vy = u

        """acceleration of the system in Y direction, t:time,  u: state vector"""
        return spring_acceleration(self.omegay, y)

    
