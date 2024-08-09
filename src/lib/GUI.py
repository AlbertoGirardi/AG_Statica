import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import os

from . import AGS_corpi
from .auxiliary import *

scale = 3





def draw_polygon(plot, shape, rotation_angle, position):

# **! OBSOLETO
    """obsoleta
    """
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






def plot_pos_vel_xy(  sol_d, tsol,  TITLE, shape=np.array([0,0]), forces_ = [], animate = False, sol_a=None, T=5, dt=1/10, time_ratio = 1, save_img = True, save_vid = False ):

    """PLOTS X, Y POSITION, X,Y VELOCITY against time
    and position in XY plane
    
    sol_d: scipy solver solution, in the form of state vector  [x,y,vx,vy]
    tsol: array of time istants for which solution has been calculated
    TITLE: title
    shape: array of points rapresenting the polygonal shape
    animate: do a matplotlib animation of the xy graph
    sol_a: solution to compare to, in the form of state vector (if not provided is not plotted)
    T = total time of simulation
    dt = time step
    time_ratio = plyback speed
    save_img: saves image
    save_vid = saves video of the animation


    """

    #create graph with multiple plots
    fig,ax = plt.subplot_mosaic([['x', 'y','a', 'xy', 'xy','xy','xy'], ['vx', 'vy','w', 'xy', 'xy', 'xy','xy']])
    fig.suptitle(TITLE)
    fig.set_size_inches(14,8)

    graphs = {'x': 0, 'y':1 ,'a':2, 'vx':3, 'vy':4,'w':5 }

    #x position

    ax['x'].plot(sol_d.t, sol_d.y[0,:],'+r',label = 'RK45')
    ax['x'].set_xlabel("t [s]")
    ax['x'].set_ylabel("x [m]")
    ax['x'].grid(True)

    
    # ax['x'].set_title("position x")
        
    #y position

    ax['y'].plot(sol_d.t, sol_d.y[1,:],'+r',label = 'RK45')
    ax['y'].set_xlabel("t [s]")
    ax['y'].set_ylabel("y [m]")
    ax['y'].grid(True)

    # ax['y'].set_title("position y")


    #x velocity

    ax['vx'].plot(sol_d.t, sol_d.y[3,:],'+r',label = 'RK45')
    ax['vx'].set_xlabel("t [s]")
    ax['vx'].set_ylabel("vx [m/s]")
    ax['vx'].grid(True)

    # ax['vx'].set_title("velocity x")


    #y velocity
    ax['vy'].plot(sol_d.t, sol_d.y[4,:],'+r',label = 'RK45')
    ax['vy'].set_xlabel("t [s]")
    ax['vy'].set_ylabel("vy [m/s]")
    ax['vy'].grid(True)

    # ax['vy'].set_title("velocity y")

    #angle
    ax['a'].plot(sol_d.t, sol_d.y[2,:],'+r',label = 'RK45')
    ax['a'].set_xlabel("t [s]")
    ax['a'].set_ylabel("phi [rad]")
    ax['a'].grid(True)


    #angular velocity
    ax['w'].plot(sol_d.t, sol_d.y[5,:],'+r',label = 'RK45')
    ax['w'].set_xlabel("t [s]")
    ax['w'].set_ylabel("omega [rad]")
    ax['w'].grid(True)





    if sol_a is not None:

        #plots all the analitical solutions
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
    ax['xy'].plot(sol_d.y[0,0],  sol_d.y[1,0] , 'oy', label = "start")          #plotting start position
    ax['xy'].plot(sol_d.y[0,:], sol_d.y[1,:] , '+g', label = 'RK')
    ax['xy'].plot(0,0,  'or')  #marking origin
    ax['xy'].set_xlabel("x[m]")
    ax['xy'].set_ylabel("y[m]")

    ax['xy'].legend()
    ax['xy'].set_title("POSITION in XY PLANE")

    
    # print(max(sol_d.y[0,:]), max(sol_d.y[1,:]))

    #adjusting axis size if it is too small
    s=2
    if abs(max(sol_d.y[0,:]))< 0.1: 
        ax['xy'].set_xlim(-s,s)

    if abs(max(sol_d.y[1,:]))< 0.1: 
        ax['xy'].set_ylim(-s,s)


    def update_animation_graph(frame): 

        """
        function that updates each frame of the live graph
        """


        # print(shape)
        # print(sol_d.y[:2,frame])


        #rotation matrix for the given rotation angle
        Rot = rotation_matrix2D(sol_d.y[2,frame])

        #calculates the coordinates of the points of the body, shifting them according to barycenter positon after applying rotation
        shape_shifted = Rot@shape + sol_d.y[:2,frame, np.newaxis]

        #updates the body points data on the graph 
        polygon.set_xdata(shape_shifted[0])
        polygon.set_ydata(shape_shifted[1])

        #moves the barycenter too
        barycenter.set_xdata(sol_d.y[0,frame])   #marks barycenter
        barycenter.set_ydata(sol_d.y[1,frame])

        #moves the current data value indicator in the vs time graph
        for g in graphs.keys(): 
            t_graphs[g].set_xdata( tsol[frame])
            t_graphs[g].set_ydata( sol_d.y[graphs[g],frame])


        for n, fg in enumerate(forces_rep):
            forces[n].plot(fg,sol_d.y[:,frame])
            
        #writes the current animation time
        L.get_texts()[-1].set_text(f"T={round(frame*dt, 2) } s") 

        return (polygon, L, t_graphs, forces_rep)


    if animate:
        
        #plots the starting shape
        Rot = rotation_matrix2D(sol_d.y[2,0])
        # print(Rot)

        #initializes plot
        shape_shifted = Rot@shape + sol_d.y[:2,0, np.newaxis]
        polygon = ax['xy'].plot(shape_shifted[0], shape_shifted[1], 'o-b', label= 'T=0 s')[0]
        barycenter = ax['xy'].plot(sol_d.y[0,0],  sol_d.y[1,0], 'og')[0]

        forces_rep = []
        forces = []

        for f in forces_:

            if f.plottable:
                forces_rep.append(ax['xy'].quiver(f.attachment1[0], f.attachment1[1], 0, 0, color=f.color,  angles='xy', scale_units='xy', scale=1, width = 0.005))
                forces.append(f)

        # print(forces_rep, 'a')


        t_graphs = {}
        #plots the vs time graph and stores them
        for g in graphs.keys():

            t_graphs[g] = ax[g].plot(tsol[0], sol_d.y[graphs[g],0],'og', label = 'now')[0]




        L = ax['xy'].legend()
    ax['x'].legend()

    #generates animation
    ani = animation.FuncAnimation(fig=fig, func=update_animation_graph, frames=(int(T/dt)+1), interval=dt*1000/time_ratio) 

    fig.tight_layout()
    fig.set_size_inches(14, 8)
  
    if save_img:
        fig.savefig(get_incremental_filename('data\\plots', 'AG_traiettoria', 'png'), dpi = 200)
    
    if save_vid:
        ani.save(get_incremental_filename('data\\plots', 'AG_traiettoria', 'mp4'), writer='ffmpeg')

    plt.show()

