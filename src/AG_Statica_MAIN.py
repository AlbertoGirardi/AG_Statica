#AG_Statica

#di Alberto Girardi


import lib.AGS_corpi
import numpy as np
import matplotlib.pyplot as plt
import lib.universe 



def MAIN():
    #funzione main con il corpo del programma

    print("AG Statica")

    x0 = 0
    y0 = 0
    vx0 = 6
    vy0 = 10
    g= -9.81


    posizione = np.array([x0,y0])
    velocity = np.array([vx0,vy0])


    mass = lib.AGS_corpi.Point_mass(3, posizione, velocity)

    print(mass.u0)

    universo = lib.universe.Universe((mass,), gravity_a=g)

    # print(mass.accelerationX(), mass.accelerationY())

    universo.solve(3, 0.1)


    #calcola la soluzione esatta del sistema
    tsol = universo.tsol
    xsol = x0 + vx0*tsol
    ysol = y0 + vy0*tsol + 0.5*g*tsol**2

    vxsol = np.full(tsol.shape, vx0)
    vysol = vy0 + g*tsol


    sol_exact = np.vstack((xsol, ysol, vxsol, vysol))                       #unione delle soluzioni calcolate in una matrice formata da una serie di vettori di stato
                                                                            #per ogni istante di tempo

    universo.sol_a = sol_exact

    
    universo.draw()







if __name__ == '__main__':              #entry guard, rende chiaro che sia da eseguire
    MAIN()

