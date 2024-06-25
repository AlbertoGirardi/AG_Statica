import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from . import AGS_corpi

scale = 3



def draw_polygon(plot, shape, rotation_angle, position):
    print("drawing")

    fig,ax = plot

    ax.clear

    rotation_matrix = AGS_corpi.rotation_matrix2D(rotation_angle)                   #first apply rotation with rotation matrix, aroudn barycenter
    print(rotation_matrix)
    shape = rotation_matrix@shape


    shape = shape + position[:,np.newaxis]          #shifting the shape matrix with the position vector


    ax.plot(0,0, marker = 'o',mfc = 'g')   #marking the origin with a green dot
    ax.plot(shape[0,:],shape[1,:],'o-b')

    ax.axis([-scale, scale, -scale, scale])
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')




def plot_rotating_polygon(plot, shape, rotation_angle, position):

    fig,ax = plot
    ani = animation.FuncAnimation(fig, draw_polygon, frames=50,  blit=True, interval = 50)