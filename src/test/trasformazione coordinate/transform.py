
import numpy as np
import matplotlib.pyplot as plt


rotmT = np.array([[0, -1], [1,0]])

def MomentumVarignon(f, r):
    
    rT = rotmT@r

    M = rT@f

    fig, ax = plt.subplots()
    print(r, rT)


    #GRAPHING TEST
    scale = 4

    ax.set(xlim=[-scale, scale], ylim=[-scale, scale], xlabel='X[m]', ylabel='Y [m]') 

    plt.quiver(0, 0, r[0], r[1],  angles='xy', scale_units='xy', scale=1, color='r')
    plt.quiver(0, 0, rT[0], rT[1],  angles='xy', scale_units='xy', scale=1, color='b')
    plt.quiver( r[0], r[1], f[0], f[1],  angles='xy', scale_units='xy', scale=1, color='g')
    print(M, np.linalg.norm(r)*np.linalg.norm(f))
    ax.set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()

    
    return M


MomentumVarignon(np.array([1,-1]),r =  np.array([1,1]))