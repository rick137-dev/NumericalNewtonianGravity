import numpy as np
import scipy


class SystemSolver:

    @staticmethod
    def generalSolver(starSystem, step_size, end_time, method = "RKScipy"):
        if method == "Euler":
            return SystemSolver.solveEulerMethod(starSystem,step_size,end_time)
        else:
            return None


    @staticmethod
    def solveEulerMethod(starSystem, step_size, end_time):
        trajectory = []
        Y_0 = []

        for star in starSystem.getStars():
            pos_x , pos_y = star.getPosition()
            Y_0.append(pos_x)
            Y_0.append(pos_y)

        for star in starSystem.getStars():
            vel_x,vel_y = star.getVelocity()
            Y_0.append(vel_x)
            Y_0.append(vel_y)


        Y_0 = np.array(Y_0,dtype = float)

        trajectory.append(Y_0)

        times = np.arange(0, end_time + step_size, step_size)


        for time in times[:-1]:
            Y = trajectory[-1]
            Y_new = Y + step_size*starSystem.getSystemDerivative(time, Y)
            trajectory.append(Y_new)

        return times , trajectory




    @staticmethod
    def solveMidpointMethod(starSystem, step_size, end_time):
        trajectory = []
        Y_0 = []

        for star in starSystem.getStars():
            pos_x, pos_y = star.getPosition()
            Y_0.append(pos_x)
            Y_0.append(pos_y)

        for star in starSystem.getStars():
            vel_x, vel_y = star.getVelocity()
            Y_0.append(vel_x)
            Y_0.append(vel_y)

        Y_0 = np.array(Y_0, dtype=float)

        trajectory.append(Y_0)

        times = np.arange(0, end_time + step_size, step_size)

        for time in times[:-1]:
            Y = trajectory[-1]
            slope_start = starSystem.getSystemDerivative(time,Y)
            time_midpoint = time + step_size//2
            Y_midpoint = Y + (step_size *slope_start)//2
            slope_midpoint = starSystem.getSystemDerivative(time_midpoint, Y_midpoint)
            Y_new = Y + step_size *slope_midpoint
            trajectory.append(Y_new)


        return times, trajectory


    def solveRungeKuttaScipy(self):
        pass



