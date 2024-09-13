import numpy as np

def Rastrigin(x):
    value  = 0
    n = x.shape[0]
    for i in range(n):
        value +=  (x[i] - 3.0)**2 - 10 * np.cos(2 * np.pi * (x[i] - 3.0))

    value += 10  * n
    return value

def RozenBlock(x):
    dim = x.shape[0]
    value = 0.0
    for i in range(dim - 1):
        value += 100.0 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1.0) ** 2
    return value  


def Sphere(x):
    eval = float (((x - 5.0) * (x - 5.0)).sum())
    return eval
