
from   scipy.integrate import solve_ivp
import numpy as np
import lib.GUI


class Universe:

    """class for the universe:
    contains all the bodies and solves their dinamycs and constraints"""


    def __init__(self, bodylist, gravity_a = 0):


        self.bodylist = bodylist
        self.n_bodies = len(self.bodylist)              #numero di corpi
        self.sol_a = None                               #exact solution of the system

        self.T = 0     #placeholder for total time
        self.dt = 0   #placeholder for simulation time

        self.g = gravity_a

        for b in self.bodylist:             #tells every body the universe gravity
            b.universe = self

        if self.n_bodies != 1:
            raise RuntimeError("only one body system")


    def solve(self, T, dt):

        """SOLVES THE SYSTEM WITH RK45, via scipy
            T: is the simulation timespan [s]
            dt: simulation timestep [s]
        """

        self.N = int(T/dt)
        self.tsol  = np.linspace(0,T,self.N+1)                                    #istanti per i quali si calcola la soluzione 
        self.dt = dt
        self.T = T

        self.dynamic_solution = solve_ivp(self, [0, self.T], self.bodylist[0].u0 , method='RK45', t_eval=self.tsol)



    def __call__(self, t, u):
        
        
        """dato il vettore di stato u [x,y,vx,vy] e il tempo restituisce il vettore FLUSSO[vx, vy, ax, ay], calcolando l'accelerazione subita
            
        necessary for solving the system with the scipy api

        """

        x, y, vx, vy = u                        #spacchettamento vettore di stato


        dx = vx                                 #dummy 
        dy = vy

        accelerations = self.bodylist[0].Force(t, u) / self.bodylist[0].mass

        dvx = accelerations[0]         #ottiene accelerazione del corpo nelle due direzioni
        dvy = accelerations[1]
        return [dx, dy, dvx, dvy]               #ritorna il vettore FLUSSO


        




    def draw(self, do_animation=False, time_ratio = 1):

        """draws the (for now) single body of the universe, using matplotlib

            do_animation: if true also animates the motion

            the time ratio sets the ratio between simulation time and real time
            """
        lib.GUI.plot_pos_vel_xy(self.dynamic_solution, self.tsol,  "test", shape=self.bodylist[0].shape,
                                 sol_a=self.sol_a, animate=do_animation, T=self.T, dt= self.dt, time_ratio=time_ratio)