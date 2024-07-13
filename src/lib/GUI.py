import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from . import AGS_corpi

scale = 3



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






def plot_pos_vel_xy(sol_d, tsol,  TITLE, shape=np.array([0,0]), animate = False, sol_a=None, T=5, dt=1/10):

    """PLOTS X, Y POSITION, X,Y VELOCITY against time
    and position in XY plane
    
    sol_d: scipy solver solution, in the form of state vector  [x,y,vx,vy]
    sol_a: solution to compare to, in the form of state vector (if not provided is not plotted)
    tsol: array of time istants for which solution has been calculated
    animate: do a matplotlib animation of the xy graph


    """

    fig,ax = plt.subplot_mosaic([['x', 'y', 'xy'], ['vx', 'vy', 'xy']])    
    fig.suptitle(TITLE)
    fig.set_size_inches(12,6)

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

    ax['vx'].plot(sol_d.t, sol_d.y[2,:],'+r',label = 'RK45')
    ax['vx'].set_xlabel("t [s]")
    ax['vx'].set_ylabel("vx [m/s]")
    # ax['vx'].set_title("velocity x")


    #y velocity
    ax['vy'].plot(sol_d.t, sol_d.y[3,:],'+r',label = 'RK45')
    ax['vy'].set_xlabel("t [s]")
    ax['vy'].set_ylabel("vy [m/s]")
    # ax['vy'].set_title("velocity y")


    if sol_a is not None:

        ax['vy'].plot(tsol, sol_a[3,:],'-b',label = 'exact')
        ax['vx'].plot(tsol, sol_a[2,:],'-b',label = 'exact')
        ax['y'].plot(tsol, sol_a[1,:],'-b',label = 'exact')
        ax['x'].plot(tsol, sol_a[0,:],'-b',label = 'exact')



    ax['x'].legend( )


    #plotting the movement on the xy plane
    ax['xy'].grid(True)
    ax['xy'].set_aspect('equal', adjustable='box')
    ax['xy'].plot(sol_d.y[0,0],  sol_d.y[1,0] , 'oy', label = "start")  
    ax['xy'].plot(sol_d.y[0,:], sol_d.y[1,:] , '+g', label = 'RK')
    ax['xy'].plot(0,0,  'or')  #marking origin
    ax['xy'].set_xlabel("x[m]")
    ax['xy'].set_ylabel("y[m]")
    ax['xy'].plot(sol_a[0,:], sol_a[1,:] , 'c',label = 'exact')

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
        shape_shifted = shape + sol_d.y[:2,frame, np.newaxis]
        polygon.set_xdata(shape_shifted[0])
        polygon.set_ydata(shape_shifted[1])
        L.get_texts()[3].set_text(f"T={round(frame*dt, 2)}") 

        return (polygon, L)


    if animate:
        polygon = ax['xy'].plot(shape[0], shape[1], 'o-b', label= 'T=0')[0]
        L = ax['xy'].legend()

    ani = animation.FuncAnimation(fig=fig, func=update_animation_graph, frames=int(T/dt), interval=dt*1000) 

    fig.tight_layout()
    plt.show()

