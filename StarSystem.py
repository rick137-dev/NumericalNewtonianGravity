import numpy as np

from Solver import SystemSolver
from Star import Star


class StarSystem:

    def __init__(self, gravitational_constant = 1, distance_epsilon = 0, merge_distance = 1e-4):
        self.stars = []
        self.system_trajectories = None
        self.gravitational_constant = gravitational_constant
        self.distance_epsilon = distance_epsilon
        self.merge_distance = merge_distance

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
        x1, y1 = pos_1
        x2, y2 = pos_2
        return (x1-x2)**2 + (y1-y2)**2


    def getCubedDistance(self,pos_1, pos_2):
        x1 , y1 = pos_1
        x2, y2 = pos_2

        #The epsilon term is for numerical softening at small distances to avoid singularities
        distance = np.sqrt(((x1-x2)**2) + ((y1-y2)**2) + (self.distance_epsilon**2))
        return distance**3

    @staticmethod
    def mergeStars(star1_position, star1_velocity,star2_position, star2_velocity, mass_1, mass_2):
        new_star1_mass = mass_1 + mass_2
        new_star2_mass = float(0)

        new_x = (mass_1 * star1_position[0] + mass_2 * star2_position[0]) / (mass_1 + mass_2)
        new_y = (mass_1 * star1_position[1] + mass_2 * star2_position[1]) / (mass_1 + mass_2)
        new_star1_position = [new_x, new_y]

        new_star2_position = star2_position

        new_star1_velocity = [(mass_1*star1_velocity[0] + mass_2*star2_velocity[0])/new_star1_mass,(mass_1*star1_velocity[1] + mass_2*star2_velocity[1])/new_star1_mass]
        new_star2_velocity = [0,0]

        return new_star1_position, new_star2_position, new_star1_velocity, new_star2_velocity, new_star1_mass, new_star2_mass



    #Here we assume Y and masses are already numpy
    def enforceMergeEvent(self, time, Y: np.array, masses : np.array):
        N = Y.size
        L = N // 2

        Y_pos = Y[:L]
        Y_velocities = Y[L:]

        mergedStars = False

        for i in range(0,L,2):
            pos_i = [Y_pos[i], Y_pos[i + 1]]
            vel_i = [Y_velocities[i], Y_velocities[i + 1]]
            mass_i = masses[i//2]

            for j in range(i+1,L,2):
                pos_j = [Y_pos[j], Y_pos[j + 1]]
                vel_j = [Y_velocities[j], Y_velocities[j + 1]]
                mass_j = masses[j // 2]


                if mass_i >0 and mass_j >0 and StarSystem.getSquaredDistance(pos_i,pos_j)<self.merge_distance**2:
                    mergedStars = True
                    new_star1_position, new_star2_position, new_star1_velocity, new_star2_velocity, new_star1_mass, new_star2_mass = StarSystem.mergeStars(pos_i,vel_i,pos_j,vel_j,mass_i,mass_j)

                    Y[i], Y[i+1] = new_star1_position
                    Y[j], Y[j+1] = new_star2_position

                    Y[i+L] , Y[i+1+L] = new_star1_velocity
                    Y[j + L], Y[j + 1 + L] = new_star2_velocity

                    masses[i//2] = new_star1_mass
                    masses[j//2] = new_star2_mass


                    #Refresh copied variables
                    pos_i = [Y_pos[i], Y_pos[i + 1]]
                    vel_i = [Y_velocities[i], Y_velocities[i + 1]]
                    mass_i = masses[i // 2]




        return mergedStars






    def getSystemDerivative(self, time, Y : np.array, masses : np.array):

        N = Y.size

        if (N % 4) != 0:
            raise ValueError("State vector length must be divisible by 4 since each body has 2 numbers for position and 2 numbers for velocity")
        n_bodies = N // 4

        if masses.size != n_bodies:
            raise ValueError(f"Masses must have length {n_bodies}, got {masses.size}")

        L = N // 2

        Y_pos = Y[:L].copy()
        Y_velocities = Y[L:].copy()

        Y_dot = np.empty(N,dtype = float)
        Y_acceleration = np.empty(L,dtype = float)

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

            Y_acceleration[i] = ax
            Y_acceleration[i+1] = ay


        Y_dot[:L] = Y_velocities
        Y_dot[L:] = Y_acceleration
        return Y_dot


    def calculateTrajectories(self, step_size, end_time, method = "RKScipy"):
        return SystemSolver.generalSolver(self, step_size, end_time, method)

