import numpy as np
import matplotlib.pyplot as plt

# Function to integrate
def f(x):
    return 2*x*np.exp(x**2)

# Exact area under the curve ~ because f(x) = d/dx (exp(x**2))
exact_area = np.exp(9) - np.exp(1)

# Ttrapezoidal rule approximation
def trapezoidal_rule(f, a, b, M):
    x = np.linspace(a, b, M+1)
    sum = 0
    for k in range(1,M+1):
        sum+=f(x[k])+f(x[k-1])
    area = ((b - a) / (2*M)) * sum
    return area

# Generate data for plotting
M_values = range(1, 201)
area_values = [trapezoidal_rule(f, 1, 3, M) for M in M_values]

# Plot the areas
plt.plot(M_values, area_values)
plt.plot([1, 200], [exact_area, exact_area], linestyle='--', color='red', label='Exact Area')
plt.legend()
plt.title("Area Under the Curve " + r"$y(x) = 2x \cdot e^{x^2}$" + "in [1,3] using Trapezoidal Rule")
plt.xlabel("Number of Intervals (M)")
plt.ylabel("Area")
plt.show()
