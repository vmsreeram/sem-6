import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, fixed_quad, quadrature, romberg

def y(x):
    return 2 * x * np.exp(x**2)

def actual_area(u):
    return np.exp(u**2) - 1

def visualize_area():
    us = np.linspace(0, 1, 100)
    actual_areas = [actual_area(u) for u in us]
    quad_areas = [quad(y, 0, u)[0] for u in us]                     # it returns tuple, 2nd one is error
    fixed_quad_areas = [fixed_quad(y, 0, u)[0] for u in us]
    quadrature_areas = [quadrature(y, 0, u)[0] for u in us]
    romberg_areas = [romberg(y, 0, u) for u in us]

    plt.plot(us, actual_areas, label='Actual area')
    plt.plot(us, quad_areas, label='quad')
    plt.plot(us, fixed_quad_areas, label='fixed_quad')
    plt.plot(us, quadrature_areas, label='quadrature')
    plt.plot(us, romberg_areas, label='romberg')
    plt.legend()
    plt.grid()
    plt.show()

visualize_area()
