import numpy as np
import matplotlib.pyplot as plt

def solveODE_fwdEuler(ode,t0, T,x_t0, Nh):
    h = (T-t0)/Nh
    
    points = []
    cur = t0
    while(cur<T):
        points.append(cur)
        cur+=h
    
    X = [x_t0]
    
    pass