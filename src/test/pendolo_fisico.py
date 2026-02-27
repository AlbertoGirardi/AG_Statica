import numpy as np
import matplotlib.pyplot as plt
from   scipy.integrate import solve_ivp

class physic_pendulum:
    def __init__(self,  omega):
        self.omega = omega
    
    def __call__(self, t, u):
        phi, dphi = u
        ddphi = -self.omega**2 * np.sin(phi)
        return [dphi, ddphi]

# condizioni iniziali
phi0  = np.pi/6 # angolo rispetto alla vericale
dphi0 = 0       # velocità di rotaziones

# modello matematico
# oggetto con polo fisso soggetto a gravità

# JO*ddphi + m*g*dOG*sin(phi) = 0
# JO momento d'inezia rispetto al punto di sospendita JO = JG + dOG^2*m
# m massa
# dOG distanza tra il centro di massa e la cerniera
# si può scrivere anche come
# ddphi = - (m*g*dOG/JO)*sin(phi)
# w^2   = (m*g*dOG/JO) frequenza naturale pendolo fisico

JO = 1 #kgm^2
g = 9.81 # m/s^2 
dOG = 1 # m lunghezza pendolo fisico fino al baricentro
m = 1 # kg massa pendolo fisico
omegac = np.sqrt(m*dOG*g/JO)
Tper = 2*np.pi/omegac


nper = 10 # numero di periodo
T    = nper*Tper #tempo totale simulazione
N_per = 100 # numero di intervalli di tempo in un perido
N    = N_per*nper # numero di intervalli di tempo 
dt   = T/N # intervallo di tempo

# soluzione ai piccoli angoli
tsol = np.linspace(0,T,N+1)
phisol =   phi0*np.cos(omegac*tsol) + dphi0/omegac*np.sin(omegac*tsol)
dphisol = -omegac*phi0*np.sin(omegac*tsol) + dphi0*np.cos(omegac*tsol)

u0 = np.array([phi0,dphi0])
# metodo Runge Kutta predictor corrector 4/5 ordine
sol = solve_ivp(physic_pendulum(omega=omegac), [0, T], u0 , method='RK45', t_eval=tsol)


    
fig,ax = plt.subplots()    
fig.suptitle('solve_ivp RK45')
ax.plot(sol.t, sol.y[0,:],'+r',label = 'RK45')
ax.plot(tsol, phisol,'-b',label = 'linear')
ax.legend()
ax.set_title('angolo')
ax.set_xlabel("t [s]")
ax.set_ylabel("phi[rad]")

plt.show()