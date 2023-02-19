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
def delta_c(x, h):
    return (f(x + h) - f(x - h)) / (2*h)

x_values = np.linspace(0, 1, 1000)
y_f_dash = f_dash(x_values)

def compute_maxAbsErrs(h):
    y_delta_plus = delta_plus(x_values, h)
    y_delta_plus_absErr = np.abs(y_delta_plus - y_f_dash)
    ans_delta_plus = max(y_delta_plus_absErr)

    y_delta_c = delta_c(x_values, h)
    y_delta_c_absErr = np.abs(y_delta_c - y_f_dash)
    ans_delta_c = max(y_delta_c_absErr)
    
    return ans_delta_plus,ans_delta_c

# Generating data for plotting
hs = [i*0.001 for i in range(1001)]
maxErr_delta_plus,maxErr_delta_c=[],[]
for h in hs:
    aa, bb = compute_maxAbsErrs(h)
    maxErr_delta_plus.append(aa)
    maxErr_delta_c.append(bb)

# Plotting...
plt.plot(hs, maxErr_delta_plus, label="maximum absolute error in forward difference")
plt.plot(hs, maxErr_delta_c, label="maximum absolute error in central difference")
plt.legend()
plt.title("maximum absolute error of approximations for " +r"$sin(x^2)$")
plt.xlabel("h")
plt.ylabel(r"$\epsilon$")
plt.grid()
plt.show()
