
from   scipy.integrate import solve_ivp
import numpy as np
import lib.GUI


class Universe:

    """class for the universe:
    contains all the bodies and solves their dinamycs and constraints"""


    def __init__(self, bodylist, gravity_a = 0):

        """
        bodylist: list of bodies (1 MAX)
        gravity_a: gravitationa acceleration of the universe (negative -> downward) 
        
        """


        self.bodylist = bodylist
        self.n_bodies = len(self.bodylist)              #numero di corpi
        self.sol_a = None                               #exact solution of the system

        self.T = 0     #placeholder for total time
        self.dt = 0   #placeholder for simulation time

        self.g = gravity_a     #diagonal values of the mass-inertia matrix for the universe

        M_m_diag = []

        for b in self.bodylist:             #tells every body the universe gravity
            b.universe = self
            M_m_diag.extend([b.mass, b.mass, b.inertia])


        self.Mass_matrix = np.diag(M_m_diag)
        print(self.Mass_matrix)

        if self.n_bodies != 1:
            raise RuntimeError("only one body system")
        
        b1 = self.bodylist[0]
        self.u0 = np.concatenate((b1.position,[b1.rotation_angle], b1.velocity, [b1.angular_velocity]))

        # print(self.u0)
        # print(self.u0[3:5])




    def solve(self, T, dt):

        """SOLVES THE SYSTEM WITH RK45, via scipy
            T: is the simulation timespan [s]
            dt: simulation timestep [s]
        """

        self.N = int(T/dt)
        self.tsol  = np.linspace(0,T,self.N+1)                                    #istanti per i quali si calcola la soluzione 
        self.dt = dt
        self.T = T

        self.dynamic_solution = solve_ivp(self, [0, self.T], self.u0 , method='RK45', t_eval=self.tsol)



    def __call__(self, t, u):
        
        
        """dato il vettore di stato u [x,y,phi,vx,vy, omega] e il tempo restituisce il vettore FLUSSO[vx, vy, omega, ax, ay, epsilon], calcolando l'accelerazione subita
            
        necessary for solving the system with the scipy api

        """

        x, y, a , vx, vy, w = u                        #spacchettamento vettore di stato


        dx = vx                                 #dummy 
        dy = vy
        dphi = w

        accelerations = self.bodylist[0].Force(t, u) / np.diag(self.Mass_matrix)        #CALCULATES ACCELERATIONS FROM TOTAL FORCE AND MASS-INERTIA MATRIX

        dvx = accelerations[0]                                                          #gets accelerations in the various dimensions
        dvy = accelerations[1]
        dw = accelerations[2]

        return [dx, dy, dphi, dvx, dvy, dw]                                              #ritorna il vettore FLUSSO


        




    def draw(self, titolo, do_animation=False,  time_ratio = 1):

        """draws the (for now) single body of the universe, using matplotlib

            do_animation: if true also animates the motion

            the time ratio sets the ratio between simulation time and real time
            """
        lib.GUI.plot_pos_vel_xy(self.dynamic_solution, self.tsol,  titolo, shape=self.bodylist[0].shape,
                                 sol_a=self.sol_a, animate=do_animation, T=self.T, dt= self.dt, time_ratio=time_ratio)