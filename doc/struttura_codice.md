[AG_Statica_MAIN.py](../src/AG_Statica_MAIN.py) =>  script da eseguire, MAIN, ovvero solo chiamate di funzioni
[librerie del progetto](../src/lib/)  => dichiarazioni di classi e funzioni 


### LIBRERIE ESTERNE

Numpy
matplotlib






## GUI

GUI with matplotlib
animation with matplotlib animate

physics solver -> list of positions and rotation angles -> list of shape matrixes (rotated and shifted) -> used to plot the moving shapes



## physics solving

univers --> __call__ function that returns the force in that moment on the body
physics solver implemented in the universe, runs over all bodies and generates a list of state vectors
state vectors passed to gui for plotting.


STATE VECTOR  [x,y,vx,vy]  for mass points

STATE VECTOR  [x,y,phi, vx,vy, omega]  for rigid bodies


