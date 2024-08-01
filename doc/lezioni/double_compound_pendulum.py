import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from   scipy.integrate import solve_ivp

class double_compound_pendulum:
    def __init__(self,  g,l1,l2,m1,m2,JG1,JG2):
        
        self.g   = g
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.JG1 = JG1
        self.JG2 = JG2
 
    
    def __call__(self, t, u):
        theta1,theta2,pdtheta1,pdtheta2 = u
        g = self.g
        l1 = self.l1 
        l2 = self.l2
        m1 = self.m1
        m2 = self.m2 
        JG1 =self.JG1 
        JG2 =self.JG2 
        
        JO1 = (JG1 + m1*(l1/2.)**2)
        JO2 = (JG2 + m2*(l2/2.)**2)
      
        ct1t2 = np.cos(theta1 - theta2)
        st1t2 = np.sin(theta1 - theta2)
        
        A1 = JO1 + m2*l1**2.
        A2 = JO2
        B  = 0.5*m2*l1*l2*ct1t2

        C1 = (0.5*m1+m2)*g*l1*np.sin(theta1) 
        C2 = 0.5*m2*g*l2*np.sin(theta2) 
        D  = 0.5*m2*l1*l2*st1t2
        
        dtheta1   = (A2*pdtheta1- B*pdtheta2)/(A1*A2-B**2)
        dtheta2   = (A1*pdtheta2- B*pdtheta1)/(A1*A2-B**2)
        
        dpdtheta1 = -D*dtheta1*dtheta2-C1 
        dpdtheta2 = +D*dtheta1*dtheta2-C2  

        return [dtheta1, dtheta2,dpdtheta1,dpdtheta2]

def Hamiltonian(theta1 ,theta2, pdtheta1,pdtheta2, g,l1,l2,m1,m2,JG1,JG2):
        
    JO1 = (JG1 + m1*(l1/2.)**2)
    JO2 = (JG2 + m2*(l2/2.)**2)
      
    ct1t2 = np.cos(theta1 - theta2)
    st1t2 = np.sin(theta1 - theta2)
        
    A1 = JO1 + m2*l1**2.
    A2 = JO2
    B  = 0.5*m2*l1*l2*ct1t2

    C1 = (0.5*m1+m2)*g*l1*np.sin(theta1) 
    C2 = 0.5*m2*g*l2*np.sin(theta2) 
    D  = 0.5*m2*l1*l2*st1t2
        
    dtheta1   = (A2*pdtheta1- B*pdtheta2)/(A1*A2-B**2)
    dtheta2   = (A1*pdtheta2- B*pdtheta1)/(A1*A2-B**2)

    T =  0.5*JO1*dtheta1**2 + 0.5*JO2*dtheta2**2 + 0.5*m2*l1*dtheta1**2 + 0.5*l1*l2*ct1t2*dtheta1*dtheta2
    V = -0.5*m1*g*l1*np.cos(theta1) - m2*g*( l1*np.cos(theta1) + 0.5*l2*np.cos(theta2)) 

    H = T + V 

    return H


g = 9.81
l1=1.
l2=1.
m1=1.
m2=1.
JG1=1./12.*m1*l1**2
JG2=1./12.*m2*l2**2


T    = 10 #perido
N    = 1000 # numero di intervalli di tempo 
dt   = T/N # intervallo di tempo
solverstr = 'Radau' #Radau DOP853 RK45


t  = np.linspace(0,T,N+1)

theta10 = 120./180.*np.pi
theta20 = 180./180.*np.pi
pdtheta10 = 0. 
pdtheta20 = 0.
u0 = np.array([theta10,theta20,pdtheta10,pdtheta20])
# metodo Runge Kutta predictor corrector 4/5 ordine
sol = solve_ivp(double_compound_pendulum(g=g, l1=l1, l2=l2, m1=m1, m2=m2, JG1=JG1, JG2=JG2), [0, T], u0 , method = solverstr, dense_output=True)

# Unpack dynamical variables as a function of time.
theta1, theta2, pdtheta1, pdtheta2 = sol.sol(t)

H  = Hamiltonian(theta1 ,theta2, pdtheta1,pdtheta2, g,l1,l2,m1,m2,JG1,JG2)
H0 = Hamiltonian(theta10 ,theta20, pdtheta10,pdtheta20, g,l1,l2,m1,m2,JG1,JG2)
errdrift = abs((H-H0)/H0)
EDRIFT_TRESHOLD = 1e-3

if any(errdrift > EDRIFT_TRESHOLD ):
    print('Maximum energy drift exceeded')




# Convert to Cartesian coordinates of the two rods.
x0 =  np.zeros_like(theta1)
y0 =  np.zeros_like(theta1)
x1 =  l1 * np.sin(theta1)
y1 = -l1 * np.cos(theta1)
x2 =  x1 + l2 * np.sin(theta2)
y2 =  y1 - l2 * np.cos(theta2)

xmat = np.column_stack((x0,x1,x2))
ymat = np.column_stack((y0,y1,y2))

figs,axs = plt.subplots(1,2)  

axs[0].set_title(solverstr)
axs[0].axis([-l1-l2, l1+l2,-l1-l2, l1+l2])
axs[0].set_aspect('equal', adjustable='box')
line, = axs[0].plot(xmat[0,:], ymat[0,:], 'o-b', lw=2)


axs[1].set_title('drift error')
axs[1].axis([0, T,np.min(errdrift), np.max(errdrift) ])
line1, = axs[1].plot(t[0],errdrift[0],'-r')


def update(frame):
    line.set_data(xmat[frame,:],ymat[frame,:])
    line1.set_data(t[0:frame],errdrift[0:frame])
    return [line,line1]


ani = animation.FuncAnimation(fig=figs, func=update, frames=N+1, interval=dt*1000,repeat=False)
plt.show()