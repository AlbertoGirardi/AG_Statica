import matplotlib.pyplot as plt
import numpy as np

scale = 3

def draw_polygon(shape, rotation_angle, position):
    print("drawing")

    fig,ax = plt.subplots()

    shape = shape + position[:,np.newaxis]          #shifting the shape matrix with the position vector

    ax.plot(0,0, marker = 'o',mfc = 'g')   #marking the origin with a green dot
    ax.plot(shape[0,:],shape[1,:],'o-b')

    ax.axis([-scale, scale, -scale, scale])
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    plt.show()

