import os



class Project():

    def __init__(self, name, universo):
        self.name = name
        self.universo = universo

        #create folder structure
        base_path = os.path.join(os.getcwd(),'\\data', self.name)
        output_path = os.path.join(base_path, 'output', 'plots')
        system_path = os.path.join(base_path, 'system')

        # Create directories
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(system_path, exist_ok=True)


    def save(self):
        """Saves by pickling the initial state of the universe and all of its bodies before running the simulation"""
        pass
        

    def solve(self, T, dT):
        self.save()
        self.universo.solve(T, dT)

    def save_sim(self):
        pass

    def load(self):
        pass


    
