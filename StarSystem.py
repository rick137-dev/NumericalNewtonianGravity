from Solver import SystemSolver
from Star import Star


class StarSystem:

    def __init__(self):
        self.stars = []
        self.system_trajectories = None

    def getStars(self):
        return self.stars

    def addStar(self, star: Star):
        self.stars.append(star)

    def addStars(self, starList):
        for star in starList:
            self.stars.append(star)

    def getStarCount(self):
        return len(self.stars)

    @staticmethod
    def getSquaredDistance(pos_1, pos_2):
        x1 , y1 = pos_1
        x2, y2 = pos_2
        distance_squared = ((x1-x2)**2) + ((y1-y2)**2)
        return max(distance_squared,1e-3)



    @staticmethod
    def getSystemDerivative(time, Y, masses):
        N = len(Y)

        return None


    def calculateTrajectories(self, step_size, end_time, method = "RKScipy"):
        return SystemSolver.generalSolver(self,step_size, end_time, method)

