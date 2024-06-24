#classe base per un corpo

class Corpo():
    
    
    def __init__(self, mass, position, velocity):
        self.mass = mass




class point_mass(Corpo):
    pass


class rigido(Corpo):
    def __init__(self, mass, position, velocity, inertia):
        super().__init__(mass, position, velocity)