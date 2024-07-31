import lib.AGS_corpi
import numpy as np
import matplotlib.pyplot as plt
import lib.universe 
import math

from lib.auxiliary import *


###LIST OF DIFFERENT EXAMPLE CASES OF USE OF THE PROGRAM

def CorpoRotanteCaduta():
    
    #valori di partenza per il problema
    x0 = 0
    y0 = 2
    vx0 = 0
    vy0 = 0
    g= 0

    posizione = np.array([x0,y0])
    velocity = np.array([vx0,vy0])

    forma = np.array([[1,0,-1,1], [0,1,0,0]])   + np.array([0,-1/3])[:,np.newaxis]      #forma spostata rispetto al baricentro

    w = np.pi*2/1.5 
    a = np.pi/2

    M = 0

    inertia = 0.4
    e = M/inertia


    #definizione oggetto corpo
    mass = lib.AGS_corpi.Rigido(mass=3,inertia=inertia, position=posizione, velocity=velocity, shape=forma, rotation_angle=a, angular_velocity=w )
    # print(mass.u0)


    universo = lib.universe.Universe((mass,), gravity_a=g)


    mass.addForce([ForceGravity(), ConstantForce(np.array([0,0,M]))])

    T=3
    dt = 1/24

    universo.solve(T, dt)

    #calcola la soluzione esatta del sistema
    tsol = universo.tsol

    universo.sol_a = MRUA(tsol, x0 , y0, vx0, vy0, 0, g, a,  w, e )
    # print(universo.dynamic_solution.y)
    universo.draw("CORPO ROTANTE IN CADUTA",do_animation=True, time_ratio=1)




def CorpoMolla():
    
    x0 = 5
    y0 = -11
    vx0 = 0
    vy0 = 0

    g = 0

    posizione = np.array([x0,y0])
    velocity = np.array([vx0,vy0])

    forma = np.array([[1,0,-1,1], [0,1,0,0]])   + np.array([0,-1/3])[:,np.newaxis]      #forma spostata rispetto al baricentro

    w = np.pi*2/1.5 *0
    a = np.pi/2 *0


    inertia = 0.4
    

    k = 5

    #definizione oggetto corpo
    mass = lib.AGS_corpi.Rigido(mass=3,inertia=inertia, position=posizione, velocity=velocity, shape=forma, rotation_angle=a, angular_velocity=w )
    # print(mass.u0)


    universo = lib.universe.Universe((mass,), gravity_a=g)

    molla = Spring(k, 8, np.array([5,0]), np.zeros(2))

    mass.addForce([molla, ForceGravity()])

    T=  15
    dt = 1/10

    universo.solve(T, dt)

    tsol = universo.tsol

    omegax = math.sqrt(k/mass.mass)

    xsol = x0*np.cos(omegax*tsol) + vx0/omegax*np.sin(omegax*tsol)           #soluzioni analitiche posizione x e y 

    vxsol  = -omegax*x0*np.sin(omegax*tsol) + vx0*np.cos(omegax*tsol)           #soluzioni a. velocità

    # ysol = tsol*0
    # asol = tsol*0
    # vysol = tsol*0
    # wsol = tsol*0


    # # calcola la soluzione esatta del sistema
    # universo.sol_a =  np.vstack((xsol, ysol, asol, vxsol, vysol, wsol))  
    # print(universo.dynamic_solution.y)
    universo.draw("CORPO COLLEGATO AD UNA MOLLA",do_animation=True, time_ratio=1)