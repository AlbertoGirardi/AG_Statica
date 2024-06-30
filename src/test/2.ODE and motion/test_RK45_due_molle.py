import numpy as np
import matplotlib.pyplot as plt
from   scipy.integrate import solve_ivp
from test_bodysolver import plot_pos_vel_xy, RMSE, elinfty, mass_2spring

import math

#posizioni iniziali nei due assi
x0 = 1
y0 = -2

#velocita iniziali nei due assi
v0 = +5
vy0 = +1


#costanti omega molle
omegax = 7
omegay = 2


Tper = 2*np.pi/omegax


nper = 1 # numero di periodo
T    = nper*Tper #tempo totale simulazione
N_per = 100 # numero di intervalli di tempo in un perido
N    = N_per*nper # numero di intervalli di tempo 
dt   = T/N # intervallo di tempo





tsol  = np.linspace(0,T,N+1)                                    #istanti per i quali si calcola la soluzione 


#SOLUZIONI ANALITICHE 
xsol = x0*np.cos(omegax*tsol) + v0/omegax*np.sin(omegax*tsol)           #soluzioni analitiche posizione x e y 
ysol = y0*np.cos(omegay*tsol) + vy0/omegay*np.sin(omegay*tsol)

vxsol  = -omegax*x0*np.sin(omegax*tsol) + v0*np.cos(omegax*tsol)           #soluzioni a. velocità
vysol = -omegay*y0*np.sin(omegay*tsol) + vy0*np.cos(omegay*tsol)

sol_exact = np.vstack((xsol, ysol, vxsol, vysol))                       #unione delle soluzioni calcolate in una matrice formata da una serie di vettori di stato
                                                                        #per ogni istante di tempo

#VETTORE DI STATO   [x,y,vx,vy]
u0 = np.array([x0,y0, v0, vy0])    # vettore di stato inizializzato a t=0

system = mass_2spring(omegax=omegax, omegay=omegay)  #sistema con due molle
# metodo Runge Kutta predictor corrector 4/5 ordine
sol = solve_ivp(system, [0, T], u0 , method='RK45', t_eval=tsol)


#calcolo e stampa errori rispetto alla soluzione analitica
err    = elinfty(sol.y[0,:] ,xsol)  
RMSerr = RMSE(sol.y[0,:] ,xsol) 
print("err  ={0:14.3f}, err/dt  ={1:14.3f}".format(err,err/dt))
print("RMSE ={0:14.3f}, RMSE/dt ={1:14.3f}".format(RMSerr,RMSerr/dt))




energy = system.energy(sol.y)
stdev = np.std(energy)

print(f"avarage total energy:{np.average(energy):.4f}J standard deviation of the value of total energy :{stdev:.4f} (~10^{math.floor(math.log10(stdev))})")

plot_pos_vel_xy(sol, tsol, sol_exact, TITLE="DUE MOLLE SU CARRELLI")


