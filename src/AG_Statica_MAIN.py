#AG_Statica

#di Alberto Girardi


import lib.AGS_corpi
import numpy as np
import lib.universe 

from lib.auxiliary import *
from lib.examples import *
from lib.vincoli import *



def MAIN():
    #funzione main con il corpo del programma

    print("AG Statica\n\n")




    h = 0.2
    l = 5


    x0 = l/2
    y0 = 0
    vx0 = 0
    vy0 = 0
    g= -9.81

    posizione = np.array([x0,y0])
    velocity = np.array([vx0,vy0])

    # forma = np.array([[1,0,-1,1], [0,1,0,0]])  + np.array([0,-1/3])[:,np.newaxis]      #forma spostata rispetto al baricentro



    forma_p = [-l/2,-h/2], [+l/2,-h/2],[+l/2,+h/2], [-l/2,+h/2],[-l/2,-h/2]
    forma = np.array([[p[0] for p in forma_p],[p[1] for p in forma_p]])

    print(forma)

    w = np.pi*2/1*0 
    a = np.pi/2 *0

    m = 50
    M = 0
    inertia = m * (l**2/12 + h**2/2)


    e = M/inertia


    #definizione oggetto corpo
    mass = lib.AGS_corpi.Rigido(mass=m,inertia=inertia, position=posizione, velocity=velocity, shape=forma, rotation_angle=a, angular_velocity=w )
    lab = lib.AGS_corpi.Lab()

    # aggancio2 = np.array([-1,-1/3])
    aggancio2 = np.array([-l/2,0])
    cerniera = Cerniera((lab, mass), (np.array([0,0]), aggancio2))
    # print(mass.u0)

    universo = lib.universe.Universe((lab, mass,), gravity_a=g)
    universo.addVincoli([cerniera])

    mass.addForce([ForceGravity()])

    universo.solve(4,0.01)

    # tsol = universo.tsol
    # universo.sol_a = MRUA(tsol, x0 , y0, vx0, vy0, 0, g, a,  w, e )

    # print('a',universo.dynamic_solution.y[:,-1], '\n\nz')

    universo.draw("test", do_animation=True)


    



if __name__ == '__main__':              #entry guard, rende chiaro che sia da eseguire
    MAIN()

