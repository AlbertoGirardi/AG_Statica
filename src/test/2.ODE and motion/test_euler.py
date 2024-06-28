
import numpy as np
import matplotlib.pyplot as plt

g = 9.81 # m/s^2 accelerazione di gravità
m = 1 # kg massa

x0 = 10 # m posizione iniziale corpo
v0 = 0 # velocità iniziale corpo
a = -g



N = 10 # numero di intervalli di tempo
T = 1.5 # perido di integrazione
dt = T/N

t = np.zeros(N + 1)
u = np.zeros((N + 1,2))

u[0,0] = x0 # q prima colonna variabile generica per la posizione
u[0,1] = v0 # q secondo colonna varibile generica per la velocità

# metodo Eulero
for i in range(N):
    F = -m*g
    ai = F/m
    xi  = u[i,0]
    vi  = u[i,1]
    
    t[i + 1]   = t[i] + dt
    u[i + 1,0] = xi + vi*dt
    u[i + 1,1] = vi + ai*dt


usol = x0 + v0*t + 1/2*a*t**2
usolv = v0 + a*t

fig,ax = plt.subplots(2)    

ax[0].plot(t, u[:,0],'+r',label = 'Euler forward')
ax[0].plot(t, usol,'-g',label = 'exact')
ax[0].legend()
ax[0].set_title("POSITION")

ax[1].plot(t, u[:,1],'+r',label = 'Euler forward')
ax[1].plot(t, usolv,'-g',label = 'exact')
ax[1].legend()
ax[1].set_title("VELOCITY")
plt.tight_layout()

plt.show()