import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

dt = 1/24   #refresh rate
T = 6       #total time of the animation

fig, ax = plt.subplots()


triangle_s = np.array([[1,0,-1,1], [0,1,0,0]])

shape = triangle_s

line2 = ax.plot(shape[0,:],shape[1,:],'o-b', label = "T=0")[0]



ax.set(xlim=[-5, 10], ylim=[-5, 10], xlabel='X[m]', ylabel='Y [m]')    #graph setup
ax.plot(0,0, marker = 'o',mfc = 'g')   #arks the origin
ax.legend()
ax.grid(True)
L=plt.legend(loc=1)


xl = []
yl = []
v = np.array([1,1])   #velocity, xy vector


for i in range(int(T/dt)):
    #traslates the shape and saves the x and y coordinates of the points in respective list
    xl.append((shape + dt*i*v[:,np.newaxis])[0])
    yl.append((shape + dt*i*v[:,np.newaxis])[1])

   
# print(xl)
# print(yl)

# print(L.get_texts())

def update(frame):  
    # for each frame, update the data stored on each artist.

    # update the line plot to the shape at the current moment
    line2.set_xdata(xl[frame])          
    line2.set_ydata(yl[frame])
    L.get_texts()[0].set_text(f"T={round(frame*dt, 2)}")            #updates the live timer
    return (L, line2)

print(dt,int(T/dt), dt*int(T/dt))

ani = animation.FuncAnimation(fig=fig, func=update, frames=int(T/dt), interval=dt*1000)             #creates the animation
plt.show()
