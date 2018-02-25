import numpy as np
import copy



def implicit_general(obj):

    # initializes the matrixes for the equation systems
    a = np.zeros((obj.numPoints, obj.numPoints))
    b = np.zeros(obj.numPoints)
    # print a

    # left boundary
    a[0][0] = 1
    if obj.boundaries[0] == 0:
        b[0] = obj.temperature[1][0]
    else:
        b[0] = obj.boundaries[0]

    # right boundary
    a[obj.numPoints - 1][obj.numPoints - 1] = 1
    if obj.boundaries[1] == 0:
        value = obj.temperature[obj.numPoints - 2][0]
        b[obj.numPoints - 1] = value
    else:
        b[obj.numPoints - 1] = obj.boundaries[1]

    # creates the matrixes and solves the equation systems
    for i in range(1, obj.numPoints - 1):
        beta = obj.k[i] * obj.dt / \
            (2 * obj.rho[i] * obj.Cp[i] * obj.dx * obj.dx)
        sigma = obj.dt / (obj.rho[i] * obj.Cp[i])

        a[i][i - 1] = -beta
        a[i][i] = 1 + 2 * beta - sigma * obj.Q[i]
        a[i][i + 1] = -beta
        b[i] = (1 - 2 * beta - sigma * obj.Q[i]) * \
            obj.temperature[i][0] + \
            beta * obj.temperature[i + 1][0] + \
            beta * obj.temperature[i - 1][0] + 2. * sigma * \
            (obj.Q0[i] - obj.Q[i] * obj.ambTemperature)

    x = np.linalg.solve(a, b)
    # y=x

    # y=x
    
    # return x
    y=copy.copy(obj.temperature)
    # updates the temperature list
    for i in range(obj.numPoints):
        y[i][1] = x[i]
        y[i][0] = x[i]

    return y