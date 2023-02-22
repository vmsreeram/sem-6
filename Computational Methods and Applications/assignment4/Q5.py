import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, fixed_quad, quadrature, romberg

def f(x):
    return 2 * x * np.exp(x**2)

def actual_area(u):                     ## Actual area under the curve ~ because f(x) = d/dx (exp(x**2))
    return np.exp(u**2) - 1

def visualize_area(uint_l,uint_h):
    us = np.linspace(uint_l, uint_h, 200)                           # `us` contain the points where we compute points to plot
    actual_areas = [actual_area(u) for u in us]
    
    # calling different modules from scipy.integrate to compute estimates
    quad_areas = [quad(f, 0, u)[0] for u in us]                     # it returns tuple, 2nd one is error
    fixed_quad_areas = [fixed_quad(f, 0, u)[0] for u in us]
    quadrature_areas = [quadrature(f, 0, u)[0] for u in us]
    romberg_areas = [romberg(f, 0, u) for u in us]

    # plotting...
    plt.plot(us, actual_areas, label='Actual area')
    plt.plot(us, quad_areas, label='quad')
    plt.plot(us, fixed_quad_areas, label='fixed_quad')
    plt.plot(us, quadrature_areas, label='quadrature')
    plt.plot(us, romberg_areas, label='romberg')
    plt.legend()
    plt.xlabel(r'$u$')
    plt.ylabel('Area')
    plt.title('Comparison of estimates and actual area\n'+r'under $2x\cdot e^{x^2}$ in the interval $[0,u]$')
    plt.grid()
    plt.show()

visualize_area(0,3)
