#AG_Statica

#di Alberto Girardi


import lib.AGS_corpi
import numpy as np




def MAIN():
    #funzione main con il corpo del programma

    print("AG Statica")
    print("es 1 test")

    triangle_s = np.array([[1,0,-1,1], [0,1,0,0]])
    print(triangle_s)
    print(triangle_s[0,:])
    print(triangle_s[1,:])

    posizione = np.array([1,1])
    triangle = lib.AGS_corpi.Rigido(1, posizione,0, np.zeros(2), triangle_s, 0 )
    triangle.draw()





if __name__ == '__main__':              #entry guard, rende chiaro che sia da eseguire
    MAIN()

