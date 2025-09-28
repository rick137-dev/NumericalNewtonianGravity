import numpy as np

from Solver import SystemSolver
from Star import Star


class StarSystem:

    def __init__(self, gravitational_constant = 1, distance_epsilon = 0):
        self.stars = []
        self.system_trajectories = None
        self.gravitational_constant = gravitational_constant
        self.distance_epsilon = distance_epsilon

    def getStars(self):
        return self.stars

    def addStar(self, star: Star):
        self.stars.append(star)

    def addStars(self, starList):
        for star in starList:
            self.stars.append(star)

    def getStarCount(self):
        return len(self.stars)


    def getCubedDistance(self,pos_1, pos_2):
        x1 , y1 = pos_1
        x2, y2 = pos_2

        #The epsilon term is for numerical accuracy at small distances
        distance = np.sqrt(((x1-x2)**2) + ((y1-y2)**2) + (self.distance_epsilon**2))
        return distance**3




    def getSystemDerivative(self, time, Y, masses):
        N = len(Y)

        if (N % 4) != 0:
            raise ValueError("State vector length must be divisible by 4 (x,y,v_x,v_y per body)")
        n_bodies = N // 4

        if len(masses) != n_bodies:
            raise ValueError(f"Masses must have length {n_bodies}, got {masses.size}")


        Y_new = []

        for i in range(n_bodies,N):
            Y_new.append(Y[i])

        Y_pos = []

        for i in range(n_bodies):
            Y_pos.append(Y[i])

        L = len(Y_pos)

        for i in range(0,L,2):

            pos_i = [Y_pos[i],Y_pos[i+1]]
            i_mass = i//2 #Correct indexing
            mass_i = masses[i_mass]

            ax , ay = float(0), float(0)

            for j in range(0,L,2):

                pos_j = [Y_pos[j], Y_pos[j + 1]]
                j_mass = j // 2  # Correct indexing
                mass_j = masses[j_mass]

                if mass_j >0 and mass_i >0 and i!=j:
                    cubed_distance = self.getCubedDistance(pos_i,pos_j)

                    ax = ax + (mass_j * self.gravitational_constant *(pos_j[0]-pos_i[0]))/cubed_distance

                    ay = ay + (mass_j * self.gravitational_constant *(pos_j[1]-pos_i[1]))/cubed_distance


            Y_new.extend([ax,ay])



        Y_new = np.array(Y_new,dtype = float)
        return Y_new


    def calculateTrajectories(self, step_size, end_time, method = "RKScipy"):
        return SystemSolver.generalSolver(self, step_size, end_time, method)

