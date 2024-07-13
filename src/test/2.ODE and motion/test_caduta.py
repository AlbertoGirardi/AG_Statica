import numpy as np
import matplotlib.pyplot as plt
from   scipy.integrate import solve_ivp
from test_bodysolver import plot_pos_vel_xy, RMSE, elinfty, mass_falling

import math

def calculate_energy(u):

    """ calculates the kinetic+potential energy of a body, given state vector u"""

    return 0.5*(u[2,:]**2+u[3,:]**2) - g*u[1,:]

#posizioni iniziali nei due assi
x0 = 0
y0 = 5

#velocita iniziali nei due assi
vx0 =8
vy0 = 10

g = -9.81 #m/s^2   gravitational acceleration


T    = 3 #tempo totale simulazione
N_per = 100 # numero di intervalli di tempo in un perido
N    = N_per # numero di intervalli di tempo 
dt   = T/N # intervallo di tempo





tsol  = np.linspace(0,T,N+1)                                    #istanti per i quali si calcola la soluzione 


#MRUA per calcolare la soluzione esatta
xsol = x0 + vx0*tsol
ysol = y0 + vy0*tsol + 0.5*g*tsol**2

vxsol = np.full(tsol.shape, vx0)
vysol = vy0 + g*tsol


sol_exact = np.vstack((xsol, ysol, vxsol, vysol))                       #unione delle soluzioni calcolate in una matrice formata da una serie di vettori di stato
                                                                        #per ogni istante di tempo



#VETTORE DI STATO   [x,y,vx,vy]
u0 = np.array([x0,y0, vx0, vy0])    # vettore di stato inizializzato a t=0

system = mass_falling(g= g)     #sistema
# metodo Runge Kutta predictor corrector 4/5 ordine
sol = solve_ivp(system, [0, T], u0 , method='RK45', t_eval=tsol)


#calcolo e stampa errori rispetto alla soluzione analitica
err    = elinfty(sol.y[0,:] ,xsol)  
RMSerr = RMSE(sol.y[0,:] ,xsol) 
print("err  ={0:14.3f}, err/dt  ={1:14.3f}".format(err,err/dt))
print("RMSE ={0:14.3f}, RMSE/dt ={1:14.3f}".format(RMSerr,RMSerr/dt))


energy = system.energy(sol.y)
# print(energy)
stdev = np.std(energy)
print(f"avarage total energy:{np.average(energy):.4f}J standard deviation of the value of total energy :{stdev:.4f} (~10^{math.floor(math.log10(stdev))})")

print(sol.y[:2,0])

plot_pos_vel_xy(sol, tsol, sol_exact, TITLE="CORPO IN CADUTA LIBERA")



