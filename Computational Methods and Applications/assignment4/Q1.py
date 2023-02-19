import numpy as np
import matplotlib.pyplot as plt

# Defining the function sin(x^2)
def f(x):
    return np.sin(x**2)

# Defining the actual derivative of f(x)
def f_dash(x):
    return 2*x*np.cos(x**2)

# Defining the forward finite difference approximation of f(x)
def delta_plus(x, h):
    return (f(x + h) - f(x)) / h

# Generating data for plotting
x_values = np.linspace(0, 1, 1000)
y_f_dash = f_dash(x_values)
y_delta_plus = delta_plus(x_values, 0.01)

# Plotting...
plt.plot(x_values, y_f_dash, label="Actual Derivative")
plt.plot(x_values, y_delta_plus, label="Forward Difference Approximation")
plt.legend()
plt.title("Actual Derivative vs. Forward Difference Approximation of " +r"$sin(x^2)$")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()
