import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

dt = 1/24
T = 6

fig, ax = plt.subplots()


triangle_s = np.array([[1,0,-1,1], [0,1,0,0]])

shape = triangle_s

line2 = ax.plot(shape[0,:],shape[1,:],'o-b', label = "T=0")[0]



ax.set(xlim=[-5, 10], ylim=[-5, 10], xlabel='X[m]', ylabel='Y [m]')
ax.plot(0,0, marker = 'o',mfc = 'g')
ax.legend()
ax.grid(True)
L=plt.legend(loc=1)


xl = []
yl = []
v = np.array([1,1])


for i in range(int(T/dt)):
    print(dt*i)
    xl.append((shape + dt*i*v[:,np.newaxis])[0])
    yl.append((shape + dt*i*v[:,np.newaxis])[1])

   
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
