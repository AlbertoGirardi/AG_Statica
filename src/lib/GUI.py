import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import os

from . import AGS_corpi
from .auxiliary import *

scale = 3


def get_incremental_filename(base_dir, base_name, ext):
    i = 1
    while True:
        filename = f"{base_name}_{i}.{ext}"
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1


def draw_polygon(plot, shape, rotation_angle, position):

    """obsoleta"""
    print("drawing")

    fig,ax = plot

    ax.clear

    rotation_matrix = AGS_corpi.rotation_matrix2D(rotation_angle)                   #first apply rotation with rotation matrix, aroudn barycenter
    print(rotation_matrix)
    shape = rotation_matrix@shape


    shape = shape + position[:,np.newaxis]          #shifting the shape matrix with the position vector


    ax.plot(0,0, 'og')   #marking the origin with a green dot
    ax.plot(shape[0,:],shape[1,:],'o-b')

    ax.axis([-scale, scale, -scale, scale])
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')






def plot_pos_vel_xy(sol_d, tsol,  TITLE, shape=np.array([0,0]), animate = False, sol_a=None, T=5, dt=1/10, time_ratio = 1 ):

    """PLOTS X, Y POSITION, X,Y VELOCITY against time
    and position in XY plane
    
    sol_d: scipy solver solution, in the form of state vector  [x,y,vx,vy]
    sol_a: solution to compare to, in the form of state vector (if not provided is not plotted)
    tsol: array of time istants for which solution has been calculated
    animate: do a matplotlib animation of the xy graph


    """

    fig,ax = plt.subplot_mosaic([['x', 'y','a', 'xy', 'xy','xy','xy'], ['vx', 'vy','w', 'xy', 'xy', 'xy','xy']])    
    fig.suptitle(TITLE)
    fig.set_size_inches(14,8)

    graphs = {'x': 0, 'y':1 ,'a':2, 'vx':3, 'vy':4,'w':5 }

    #x position

    ax['x'].plot(sol_d.t, sol_d.y[0,:],'+r',label = 'RK45')
    
    ax['x'].set_xlabel("t [s]")
    ax['x'].set_ylabel("x [m]")
    # ax['x'].set_title("position x")
        
    #y position

    ax['y'].plot(sol_d.t, sol_d.y[1,:],'+r',label = 'RK45')
    ax['y'].set_xlabel("t [s]")
    ax['y'].set_ylabel("y [m]")
    # ax['y'].set_title("position y")


    #x velocity

    ax['vx'].plot(sol_d.t, sol_d.y[3,:],'+r',label = 'RK45')
    ax['vx'].set_xlabel("t [s]")
    ax['vx'].set_ylabel("vx [m/s]")
    # ax['vx'].set_title("velocity x")


    #y velocity
    ax['vy'].plot(sol_d.t, sol_d.y[4,:],'+r',label = 'RK45')
    ax['vy'].set_xlabel("t [s]")
    ax['vy'].set_ylabel("vy [m/s]")
    # ax['vy'].set_title("velocity y")

    #angle
    ax['a'].plot(sol_d.t, sol_d.y[2,:],'+r',label = 'RK45')
    ax['a'].set_xlabel("t [s]")
    ax['a'].set_ylabel("phi [rad]")

    #angular velocity
    ax['w'].plot(sol_d.t, sol_d.y[5,:],'+r',label = 'RK45')
    ax['w'].set_xlabel("t [s]")
    ax['w'].set_ylabel("omega [rad]")




    if sol_a is not None:

        ax['vy'].plot(tsol, sol_a[4,:],'-b',label = 'exact')
        ax['vx'].plot(tsol, sol_a[3,:],'-b',label = 'exact')
        ax['y'].plot(tsol, sol_a[1,:],'-b',label = 'exact')
        ax['x'].plot(tsol, sol_a[0,:],'-b',label = 'exact')
        ax['a'].plot(tsol, sol_a[2,:],'-b',label = 'exact')
        ax['w'].plot(tsol, sol_a[5,:],'-b',label = 'exact')
        ax['xy'].plot(sol_a[0,:], sol_a[1,:] , 'c',label = 'exact')






    #plotting the movement on the xy plane
    ax['xy'].grid(True)
    ax['xy'].set_aspect('equal', adjustable='box')
    ax['xy'].plot(sol_d.y[0,0],  sol_d.y[1,0] , 'oy', label = "start")  
    ax['xy'].plot(sol_d.y[0,:], sol_d.y[1,:] , '+g', label = 'RK')
    ax['xy'].plot(0,0,  'or')  #marking origin
    ax['xy'].set_xlabel("x[m]")
    ax['xy'].set_ylabel("y[m]")

    ax['xy'].legend()
    ax['xy'].set_title("POSITION in XY PLANE")

    
    # print(max(sol_d.y[0,:]), max(sol_d.y[1,:]))

    if max(sol_d.y[0,:])< 0.1:
        ax['xy'].set_xlim(-1,1)

    if abs(max(sol_d.y[1,:]))< 0.1:
        ax['xy'].set_ylim(-1,1)


    def update_animation_graph(frame):
        # print(shape)
        # print(sol_d.y[:2,frame])

        Rot = rotation_matrix2D(sol_d.y[2,frame])
        # print(Rot)

        shape_shifted = Rot@shape + sol_d.y[:2,frame, np.newaxis]


        polygon.set_xdata(shape_shifted[0])
        polygon.set_ydata(shape_shifted[1])

        barycenter.set_xdata(sol_d.y[0,frame])   #marks barycenter
        barycenter.set_ydata(sol_d.y[1,frame])

        for g in graphs.keys():
            t_graphs[g].set_xdata( tsol[frame])
            t_graphs[g].set_ydata( sol_d.y[graphs[g],frame])


        L.get_texts()[-1].set_text(f"T={round(frame*dt, 2) } s") 

        return (polygon, L, t_graphs)


    if animate:
        
        Rot = rotation_matrix2D(sol_d.y[2,0])
        # print(Rot)

        shape_shifted = Rot@shape + sol_d.y[:2,0, np.newaxis]
        polygon = ax['xy'].plot(shape_shifted[0], shape_shifted[1], 'o-b', label= 'T=0 s')[0]
        barycenter = ax['xy'].plot(sol_d.y[0,0],  sol_d.y[1,0], 'og')[0]

        t_graphs = {}
        for g in graphs.keys():

            t_graphs[g] = ax[g].plot(tsol[0], sol_d.y[graphs[g],0],'og', label = 'now')[0]




        L = ax['xy'].legend()
    ax['x'].legend( )

    ani = animation.FuncAnimation(fig=fig, func=update_animation_graph, frames=(int(T/dt)+1), interval=dt*1000/time_ratio) 

    fig.tight_layout()
    fig.set_size_inches(14, 8)
  
    fig.savefig(get_incremental_filename('data\\plots', 'AG_traiettoria', 'png'), dpi = 200)
    plt.show()

