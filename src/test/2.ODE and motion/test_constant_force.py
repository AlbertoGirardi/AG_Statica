import numpy as np
import matplotlib.pyplot as plt
from   scipy.integrate import solve_ivp
from test_bodysolver import plot_pos_vel_xy, RMSE, elinfty, mass_2constant_forces




#posizioni iniziali nei due assi
x0 = 1
y0 = 0

#velocita iniziali nei due assi
vx0 = 0
vy0 = 0

m = 10

FX = 5
FY = 0


T    = 3 #tempo totale simulazione
N_per = 10 # numero di intervalli di tempo in un perido
N    = N_per # numero di intervalli di tempo 
dt   = T/N # intervallo di tempo





tsol  = np.linspace(0,T,N+1)                                    #istanti per i quali si calcola la soluzione 


#MRUA per calcolare la soluzione esatta
ax = FX/m
ay = FY/m

xsol = x0 + vx0*tsol + 0.5*ax*tsol**2
ysol = y0 + vy0*tsol + 0.5*ay*tsol**2

vxsol = vx0 + ax*tsol
vysol = vy0 + ay*tsol


sol_exact = np.vstack((xsol, ysol, vxsol, vysol))                       #unione delle soluzioni calcolate in una matrice formata da una serie di vettori di stato
                                                                        #per ogni istante di tempo



#VETTORE DI STATO   [x,y,vx,vy]
u0 = np.array([x0,y0, vx0, vy0])    # vettore di stato inizializzato a t=0


# metodo Runge Kutta predictor corrector 4/5 ordine
sol = solve_ivp(mass_2constant_forces(m, FX,FY), [0, T], u0 , method='RK45', t_eval=tsol)


#calcolo e stampa errori rispetto alla soluzione analitica
err    = elinfty(sol.y[0,:] ,xsol)  
RMSerr = RMSE(sol.y[0,:] ,xsol) 
print("err  ={0:14.3f}, err/dt  ={1:14.3f}".format(err,err/dt))
print("RMSE ={0:14.3f}, RMSE/dt ={1:14.3f}".format(RMSerr,RMSerr/dt))

plot_pos_vel_xy(sol, tsol, sol_exact, TITLE="CORPO SOGGETTO A FORZE COSTANTI")
