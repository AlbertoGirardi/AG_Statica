#AG_Statica

#di Alberto Girardi


import lib.AGS_corpi
import numpy as np
import matplotlib.pyplot as plt
import lib.universe 

from lib.auxiliary import *



def MAIN():
    #funzione main con il corpo del programma

    print("AG Statica")


    #valori di partenza per il problema
    x0 = 0
    y0 = 2
    vx0 = 8
    vy0 = 11
    g= -9.81

    posizione = np.array([x0,y0])
    velocity = np.array([vx0,vy0])

    forma = np.array([[1,0,-1,1], [0,1,0,0]])   + np.array([0,-1/3])[:,np.newaxis]      #forma spostata rispetto al baricentro

    w = np.pi*2/1.5 *0
    a = np.pi/2

    M = 0.2

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
    xsol = x0 + vx0*tsol
    ysol = y0 + vy0*tsol + 0.5*g*tsol**2
    asol = a + w*tsol + 0.5*e*tsol**2

    wsol = w + e*tsol
    vxsol = np.full(tsol.shape, vx0)
    vysol = vy0 + g*tsol


    sol_exact = np.vstack((xsol, ysol, asol, vxsol, vysol, wsol))                       #unione delle soluzioni calcolate in una matrice formata da una serie di vettori di stato
                                                                            #per ogni istante di tempo

    universo.sol_a = sol_exact

    # print(universo.dynamic_solution.y)
    universo.draw("CORPO ROTANTE IN CADUTA",do_animation=True, time_ratio=1)





if __name__ == '__main__':              #entry guard, rende chiaro che sia da eseguire
    MAIN()

