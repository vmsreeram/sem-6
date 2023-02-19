import numpy as np
import matplotlib.pyplot as plt

# Defining the function sin(x^2)
def f(x):
    return np.sin(x**2)

# Defining the actual derivative of f(x)
def f_dash(x):
    return 2*x*np.cos(x**2)

# Defining the approximations of f(x) and populating required variables
def delta_plus(x, h):
    return (f(x + h) - f(x)) / h
def delta_minus(x, h):
    return (f(x) - f(x - h)) / h
def delta_c(x, h):
    return (f(x + h) - f(x - h)) / (2*h)

x_values = np.linspace(0, 1, 1000)
y_f_dash = f_dash(x_values)
y_delta_plus = delta_plus(x_values, 0.01)
y_delta_minus = delta_minus(x_values, 0.01)
y_delta_c = delta_c(x_values, 0.01)

# Generating data for plotting
y_delta_plus_absErr = np.abs(y_delta_plus - y_f_dash)
y_delta_minus_absErr = np.abs(y_delta_minus - y_f_dash)
y_delta_c_absErr = np.abs(y_delta_c - y_f_dash)


# Plotting...
plt.plot(x_values, y_delta_plus_absErr, label="Absolute error in forward difference")
plt.plot(x_values, y_delta_c_absErr, label="Absolute error in central difference")
plt.plot(x_values, y_delta_minus_absErr, label="Absolute error in backward difference")
plt.legend()
plt.title("Absolute errors in forward, central, backward difference methods for " +r"$sin(x^2)$")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()
