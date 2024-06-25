import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

def rotation_matrix2D(alfa):
    
    RM2D= [[np.cos(alfa),-np.sin(alfa)],
      [np.sin(alfa),np.cos(alfa)]]
    return RM2D


dt = 1/24
T = 10

fig, ax = plt.subplots()


triangle_s = np.array([[1,0,-1,1], [0,1,0,0]])

shape = triangle_s

line2 = ax.plot(shape[0,:],shape[1,:],'o-b', label = "T=0")[0]


scale = 3

ax.set(xlim=[-scale, scale], ylim=[-scale, scale], xlabel='X[m]', ylabel='Y [m]')
ax.plot(0,0, marker = 'o',mfc = 'g')
ax.legend()
ax.grid(True)
L=plt.legend(loc=1)


xl = []
yl = []
w = 2*np.pi/T
print(w)


for i in range(int(T/dt)):
    print(dt*i)

    Rot = rotation_matrix2D(dt*i*w)

    xl.append((Rot@shape)[0])
    yl.append((Rot@shape)[1])

   
print(xl)
print(yl)

print(L.get_texts())


def update(frame):  
    # for each frame, update the data stored on each artist.

    # update the line plot:
    line2.set_xdata(xl[frame])
    line2.set_ydata(yl[frame])
    L.get_texts()[0].set_text(f"T={round(frame*dt, 2)}")
    return (L, line2)

print(dt,int(T/dt))

ani = animation.FuncAnimation(fig=fig, func=update, frames=int(T/dt), interval=dt*1000)
plt.show()
