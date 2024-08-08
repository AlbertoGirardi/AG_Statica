
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

        self.vincoli = []

        self.sol_a = None                               #exact solution of the system

        self.T = 0     #placeholder for total time
        self.dt = 0   #placeholder for simulation time

        self.g = gravity_a     #diagonal values of the mass-inertia matrix for the universe

        M_m_diag = []
        masking_m = []

        for b in self.bodylist:             #tells every body the universe gravity
            b.universe = self
            M_m_diag.extend([b.mass, b.mass, b.inertia])
            masking_m.extend([int(not b.isLab)]*3)


        self.Mass_matrix = np.diag(M_m_diag)            #creates the mass-inertia matrix

        self.fixed_frame_masking = np.diag(masking_m)   #creates masking matrix to fix in place the laboratory body, if present


        print(self.Mass_matrix)
        print(self.fixed_frame_masking)

        if self.n_bodies > 2:
            raise RuntimeError("only one or two body system!")
        
        

        u0_ = []

        # STATE VECTOR [x1,y1,phi1,vx1,vy1, omega1, xn,yn,phin,vxn,vyn, omegan, ...] 

        for n,b in enumerate(self.bodylist):
            u0_.extend((b.position,[b.rotation_angle], b.velocity, [b.angular_velocity]))

            if b.isLab and n != 0:
                raise RuntimeError("the laboratory must be the first body provided!")

        # print(u0_)

        self.u0 = np.concatenate(u0_)               #buildis starting state vector

        print(f"Initialized Universe with {self.n_bodies} bodies, \nstarting state: {self.u0}\n")

        print(self.u0)
        # print(self.u0[3:5])


    def addVincoli(self, vincoli):


        self.vincoli.extend(vincoli)


    def solve(self, T, dt): 

        """SOLVES THE SYSTEM WITH RK45, via scipy
            T : is the simulation timespan [s]
            dt: simulation timestep [s]
        """

        self.N    = int(T/dt)
        self.tsol = np.linspace(0,T,self.N+1)                                    #istanti per i quali si calcola la soluzione
        self.dt   = dt
        self.T    = T

        print("SOLVING ODE...")

        self.dynamic_solution = solve_ivp(self, [0, self.T], self.u0 , method='RK45', t_eval=self.tsol)

        print("DONE!\n\n")



    def __call__(self, t, u): 
        
        """dato il vettore di stato u [x1,y1,phi1,vx1,vy1, omega1, xn,yn,phin,vxn,vyn, omegan, ...] 
        e il tempo restituisce il vettore FLUSSO[vx1, vy1, omega1, ax1, ay1, epsilon1,vxn, vyn, omegan, axn, ayn, epsilonn, ... ]

        dove n è il numero del corpo
        calcolando l'accelerazione subita
            
        necessary for solving the system with the scipy api

        """


        q = np.concatenate([u[(6*n):(6*n+3)] for n in range(self.n_bodies)])              

        dq = np.concatenate([u[(6*n+3):(6*n+6)] for n in range(self.n_bodies)])


        FORCES = np.concatenate([b.Force(t,u) for b in self.bodylist])



        accelerations = FORCES / np.diag(self.Mass_matrix)        #CALCULATES ACCELERATIONS FROM TOTAL FORCE AND MASS-INERTIA MATRIX 
        accelerations = self.fixed_frame_masking@accelerations      #applies masking to make laboratory fixed in place  
        #!TODO add vincoli

        print(self.vincoli[0].Jacobian(u))

        #builds the state vector given velocities and accelerations
        flusso_ = []

        for n in range(self.n_bodies):
            #iterates through all bodies and adds to the state vector the velocities and accelerations of each
            flusso_.extend((dq[3*n:3*n+3], accelerations[3*n:3*n+3] ))

        FLUSSO = np.concatenate(flusso_) 

        return FLUSSO                                             #ritorna il vettore FLUSSO


        




    def draw(self, titolo, do_animation=False,  time_ratio = 1):

        """draws the (for now) single body of the universe, using matplotlib

            do_animation: if true also animates the motion

            the time ratio sets the ratio between simulation time and real time
            """
        lib.GUI.plot_pos_vel_xy(self.dynamic_solution, self.tsol,  titolo, shape=self.bodylist[1].shape,
                                 sol_a=self.sol_a, forces_=self.bodylist[1].forces , animate=do_animation, T=self.T, dt= self.dt, time_ratio=time_ratio, save_vid=False)