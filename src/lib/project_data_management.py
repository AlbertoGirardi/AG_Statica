import os
import pickle
import copy
import pandas as pd




class Project():

    def __init__(self, name):
        self.name = name
        

        #create folder structure
        base_path = os.path.join('data', self.name)
        self.output_path = os.path.join(base_path, 'output')
        self.plots_path = os.path.join(base_path, 'output', 'plots')
        self.system_path = os.path.join(base_path, 'system')

        # Create directories
        os.makedirs(base_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.plots_path, exist_ok=True)

        os.makedirs(self.system_path, exist_ok=True)

    def link_Universe(self, universo):
        """links an universe object to the universe"""
        self.universo = universo
                      
    def save(self):
        """Saves by pickling the initial state of the universe and all of its bodies before running the simulation"""
        with open(os.path.join(self.system_path, 'system.pkl'), 'wb') as f:
            pickle.dump(copy.deepcopy(self.universo), f)




        

    def solve(self, T, dT):
        self.save()
        self.universo.solve(T, dT)



        #saves output state vector at all moments in time


        #the labels for the colums containing each data, repeated because there are two bodies
        column_labels =  ['x', 'y','a','vx', 'vy','w',]*2 

        output_data = pd.DataFrame( self.universo.dynamic_solution.y.T, columns=column_labels)
        output_data.insert(0, 't', self.universo.dynamic_solution.t )

        output_data.to_csv(os.path.join(self.output_path, 'state_vector.csv'), index =False)



    def plot(self):
        self.universo.draw("test", do_animation=True, save_path=self.plots_path )

        

    def load(self):
        
        try:
            with open(os.path.join(self.system_path, 'system.pkl'), 'rb') as f:
                self.universo = pickle.load(f)

        except FileNotFoundError:
            print("Errore: progetto non ritrovato!!!")

    
