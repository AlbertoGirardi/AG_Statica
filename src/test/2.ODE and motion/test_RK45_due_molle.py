import numpy as np
import matplotlib.pyplot as plt
from   scipy.integrate import solve_ivp
from test_bodysolver import plot_pos_vel_xy


#posizioni iniziali nei due assi
x0 = 1
y0 = -2

#velocita iniziali nei due assi
v0 = +5
vy0 = +1


#costanti omega molle
omegax = 5
omegay = 2


Tper = 2*np.pi/omegax


nper = 4 # numero di periodo
T    = nper*Tper #tempo totale simulazione
N_per = 100 # numero di intervalli di tempo in un perido
N    = N_per*nper # numero di intervalli di tempo 
dt   = T/N # intervallo di tempo



class mass_2spring:

    """CLASSE PER CORPO VINCOLATO DA DUE MOLLE SU CARRELLI

    omegax: valore costante omega per molla asse x
    omegay valore costante omega per molla asse y
    """
    def __init__(self,  omegax, omegay):
        self.omegax = omegax
        self.omegay = omegay

    
    def __call__(self, t, u):

        """dato il vettore di stato u [x,y,vx,vy] e il tempo restituisce il vettore FLUSSO[vx, vy, ax, ay]
        """
        x, y, vx, vy = u
        dx = vx
        dy = vy
        dvx = -self.omegax**2 * x
        dvy = -self.omegay**2 * y
        return [dx, dy, dvx, dvy]


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


# metodo Runge Kutta predictor corrector 4/5 ordine
sol = solve_ivp(mass_2spring(omegax=omegax, omegay=omegay), [0, T], u0 , method='RK45', t_eval=tsol)

plot_pos_vel_xy(sol, tsol, sol_exact)