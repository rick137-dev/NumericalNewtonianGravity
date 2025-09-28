
class Star:

    def __init__(self, initial_position, initial_velocity, mass):
        self.initial_position = initial_position
        self.initial_velocity = initial_velocity
        self.mass = mass


    def getMass(self):
        return self.mass

    def changeMass(self, mass):
        self.mass = mass

    def getPosition(self):
        return self.initial_position

    def getVelocity(self):
        return self.initial_velocity


    def setPosition(self, position):
        self.initial_position = position

    def setVelocity(self, velocity):
        self.initial_velocity = velocity


