import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

dt = 0.05
T = 6

fig, ax = plt.subplots()


triangle_s = np.array([[1,0,-1,1], [0,1,0,0]])

shape = triangle_s

line2 = ax.plot(shape[0,:],shape[1,:],'o-b')[0]

ax.set(xlim=[-5, 10], ylim=[-5, 10], xlabel='Time [s]', ylabel='Z [m]')
ax.legend()
ax.grid(True)

xx = []
yy = []
vy = np.array([0,1])
vx = np.array([1,0])

for i in range(int(T/dt)):
    xx.append((shape + dt*i*vx[:,np.newaxis])[0])
    yy.append((shape + dt*i*vy[:,np.newaxis])[1])

   
print(xx)
print(yy)


def update(frame):  
    # for each frame, update the data stored on each artist.

    # update the line plot:
    line2.set_xdata(xx[frame])
    line2.set_ydata(yy[frame])
    return ( line2)


ani = animation.FuncAnimation(fig=fig, func=update, frames=int(T/dt), interval=dt*1000)
plt.show()
