
from   scipy.integrate import solve_ivp
import numpy as np
import lib.GUI


class Universe:

    """class for the universe:
    contains all the bodies and solves their dinamycs and constraints"""


    def __init__(self, bodylist, gravity_a = 0):
        self.bodylist = bodylist
        self.n_bodies = len(self.bodylist)              #numero di corpi

        for b in self.bodylist:
            b.g = gravity_a

        if self.n_bodies != 1:
            raise RuntimeError("only one body system")


    def solve(self, T, dt):

        N = int(T/dt)
        self.tsol  = np.linspace(0,T,N+1)                                    #istanti per i quali si calcola la soluzione 

        self.dynamic_solution = solve_ivp(self, [0, T], self.bodylist[0].u0 , method='RK45', t_eval=self.tsol)



    def __call__(self, t, u):
        
        
        """dato il vettore di stato u [x,y,vx,vy] e il tempo restituisce il vettore FLUSSO[vx, vy, ax, ay], calcolando l'accelerazione subita

        """

        x, y, vx, vy = u                        #spacchettamento vettore di stato
        dx = vx                                 #dummy 
        dy = vy
        dvx = self.bodylist[0].accelerationX(t, u)          #ottiene accelerazione del corpo nelle due direzioni
        dvy = self.bodylist[0].accelerationY(t, u)
        return [dx, dy, dvx, dvy]               #ritorna il vettore FLUSSO


        




    def draw(self):
        lib.GUI.plot_pos_vel_xy(self.dynamic_solution, self.tsol, self.sol_a, "test")