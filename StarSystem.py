import numpy as np

from Solver import SystemSolver
from Star import Star


class StarSystem:

    def __init__(self, gravitational_constant = 1):
        self.stars = []
        self.system_trajectories = None
        self.gravitational_constant = gravitational_constant

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
    def getCubedDistance(pos_1, pos_2):
        x1 , y1 = pos_1
        x2, y2 = pos_2
        distance = np.sqrt(((x1-x2)**2) + ((y1-y2)**2))
        return max(distance**3,1e-3) #This is for numerical accuracy in the derivative function when the squared distance is in the denominator




    def getSystemDerivative(self, time, Y, masses):
        N = len(Y)
        Y_new = []

        for i in range(N//2,N):
            Y_new.append(Y[i])

        Y_pos = []

        for i in range(N//2):
            Y_pos.append(Y[i])

        L = len(Y_pos)

        for i in range(0,L//2,2):

            pos_i = [Y_pos[i],Y_pos[i+1]]
            mass_i = masses[i]

            dx , dy = float(0), float(0)

            for j in range(0,L//2,2):

                pos_j = [Y_pos[j], Y_pos[j + 1]]
                mass_j = masses[j]

                if mass_j >0 and mass_i >0 and pos_i != pos_j:
                    squared_distance = StarSystem.getCubedDistance(pos_i,pos_j)

                    dx = dx + (mass_j * self.gravitational_constant *(pos_i[0] - pos_j[0]))/squared_distance

                    dy = dy + (mass_j * self.gravitational_constant *(pos_i[1] - pos_j[1]))/squared_distance


            Y_new.extend([dx,dy])



        Y_new = np.array(Y_new,dtype = float)
        return Y_new


    def calculateTrajectories(self, step_size, end_time, method = "RKScipy"):
        return SystemSolver.generalSolver(self, step_size, end_time, method)

