import numpy as np
import scipy
from StarSystem import StarSystem


class SystemSolver:

    @staticmethod
    def generalSolver(starSystem: StarSystem, step_size, end_time, method = "RKScipy", absolute_tolerance = 1e-6, relative_tolerance = 1e-3):
        assert method == "RkScipy" or method == "Euler" or method =="Midpoint" , "Method name not found!"

        if method == "Euler":
            return SystemSolver.solveEulerMethod(starSystem,step_size,end_time)
        elif method == "Midpoint":
            return SystemSolver.solveMidpointMethod(starSystem,step_size,end_time)
        else:
            return SystemSolver.solveRungeKuttaScipy(starSystem, step_size, end_time,absolute_tolerance, relative_tolerance)

    @staticmethod
    def getInitialState(starSystem : StarSystem):
        Y_0 = []
        masses = []

        for star in starSystem.getStars():
            masses.append(star.getMass())

        for star in starSystem.getStars():
            pos_x, pos_y = star.getPosition()
            Y_0.append(pos_x)
            Y_0.append(pos_y)

        for star in starSystem.getStars():
            vel_x, vel_y = star.getVelocity()
            Y_0.append(vel_x)
            Y_0.append(vel_y)

        Y_0 = np.array(Y_0, dtype=float)
        masses = np.array(masses, dtype=float)

        return Y_0 , masses


    @staticmethod
    def solveEulerMethod(starSystem: StarSystem, step_size, end_time):
        trajectory = []
        Y_0 , masses = SystemSolver.getInitialState(starSystem)

        trajectory.append(Y_0)

        times = np.arange(0, end_time + step_size, step_size)


        for time in times[:-1]:
            Y = trajectory[-1]
            Y_new = Y + step_size*starSystem.getSystemDerivative(time, Y, masses)
            trajectory.append(Y_new)

        return times , trajectory



    #This method uses 1 midpoint, so it is equivalent to Runge Kutta 2
    @staticmethod
    def solveMidpointMethod(starSystem: StarSystem, step_size, end_time):
        trajectory = []
        Y_0, masses = SystemSolver.getInitialState(starSystem)

        trajectory.append(Y_0)

        times = np.arange(0, end_time + step_size, step_size)

        for time in times[:-1]:
            Y = trajectory[-1]
            slope_start = starSystem.getSystemDerivative(time,Y, masses)
            time_midpoint = time + step_size//2
            Y_midpoint = Y + (step_size *slope_start)//2
            slope_midpoint = starSystem.getSystemDerivative(time_midpoint, Y_midpoint, masses)
            Y_new = Y + step_size *slope_midpoint
            trajectory.append(Y_new)


        return times, trajectory

    #Scipy solve_ivp uses by default Runge Kutta 4-5, using standard order 5 and an extra order for adaptive step size
    @staticmethod
    def solveRungeKuttaScipy(starSystem: StarSystem, step_size, end_time,absolute_tolerance, relative_tolerance):

        Y_0 , masses = SystemSolver.getInitialState(starSystem)

        return scipy.integrate.solve_ivp(fun=lambda t, y: starSystem.getSystemDerivative(t, y, masses),t_span = [0,end_time],y0 = Y_0, atol = absolute_tolerance, rtol = relative_tolerance)







