#AG_Statica

#di Alberto Girardi


import lib.AGS_corpi
import numpy as np
import lib.universe 

from lib.auxiliary import *
from lib.examples import *
from lib.vincoli import *
from lib.project_data_management import *



#angolo del pendolo rispetto alla verticale
a_ = np.pi/16

a = 1.5*np.pi+(a_)

h = 0.4
l = 1


x0 = +l/2
y0 = 0
vx0 = 0
vy0 = 0

g= -9.81
w = 0


m = 10

#distance of barycenter from pivot
dOG = l/2
#inertia of the pendulum respect to its barycentere
inertia = 1/12 * m * (l**2 + h**2)

#inertia respect to the pivot
inertiaO = inertia + m * ((l/2)**2)



def create_project():
  

    rot = rotation_matrix2D(a)

    posizione = rot @ np.array([x0,y0])
    velocity = np.array([vx0,vy0])



    # forma = np.array([[1,0,-1,1], [0,1,0,0]])  + barycenter[:,np.newaxis]      #forma spostata rispetto al baricentro



    forma_p = [-l/2,-h/2], [+l/2,-h/2],[+l/2,+h/2], [-l/2,+h/2],[-l/2,-h/2]
    forma = np.array([[p[0] for p in forma_p],[p[1] for p in forma_p]])

    # print(forma)

 

    #mass
   
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

    

    p = Project('Pendolo semplice')
    p.link_Universe(universo)

    
    return p



def MAIN():
    #funzione main con il corpo del programma

    print("AG Statica\n\n")


   
    progetto = create_project()

    # progetto = Project('triangolo_pendolo')
    # progetto.load()

    progetto.solve(1, 0.01)

    tsol = progetto.universo.tsol
    progetto.universo.sol_a = pendulum_linear_solution(m,-g, a_ ,dOG, inertiaO, tsol)

    a_error =round( RMSE(progetto.universo.sol_a[2,:], progetto.universo.dynamic_solution.y[8,:] )*100, 3)
    x_error =round( RMSE(progetto.universo.sol_a[0,:], progetto.universo.dynamic_solution.y[6,:] )*100, 3)
    y_error =round( RMSE(progetto.universo.sol_a[1,:], progetto.universo.dynamic_solution.y[7,:] )*100, 3)
    w_error = round(RMSE(progetto.universo.sol_a[5,:], progetto.universo.dynamic_solution.y[11,:] )*100, 3)
    vx_error =round( RMSE(progetto.universo.sol_a[3,:], progetto.universo.dynamic_solution.y[9,:] )*100, 3)
    vy_error = round(RMSE(progetto.universo.sol_a[4,:], progetto.universo.dynamic_solution.y[10,:] )*100, 3)

    print('Errors compared to exact solution\n')
    print(f'RMS angle error: {a_error}%')
    print(f'RMS x coord error: {x_error}%')
    print(f'RMS y coord error: {y_error}%')
    print(f'RMS angular velocity error: {w_error}%')
    print(f'RMS x velocity error: {vx_error}%')
    print(f'RMS y velocity error: {vy_error}%')

    # universo.sol_a = MRUA(tsol, x0 , y0, vx0, vy0, 0, g, a,  w, e )
    # print(universo.sol_a)
    # print('sol 1',progetto.universo.dynamic_solution.y[8,0:10], '\n\nz')
    # print('sol 2',progetto.universo.sol_a[2,0:10], '\n\nz')

    progetto.plot()



    



if __name__ == '__main__':              #entry guard, rende chiaro che sia da eseguire
    MAIN()
    # CorpoRotanteCaduta()

