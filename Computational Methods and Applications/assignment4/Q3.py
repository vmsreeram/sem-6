import numpy as np
import matplotlib.pyplot as plt

# Defining the function sin(x^2)
def f(x):
    return np.sin(x**2)

# Defining the actual derivative of f(x)
def f_dash(x):
    return 2*x*np.cos(x**2)

# Defining the double derivative of f(x)
def f_doubledash(x):
    return 2*(-2*x*x*np.sin(x**2) + np.cos(x**2))

# Defining the triple derivative of f(x)
def f_tripledash(x):
    return -4*x*(2*x*x*np.cos(x**2) + 3*np.sin(x**2))

# Defining the approximations of f(x) and populating required variables
def delta_plus(x, h):
    return (f(x + h) - f(x)) / h
def delta_c(x, h):
    return (f(x + h) - f(x - h)) / (2*h)

x_values = np.linspace(0, 1, 100)
y_f_dash = f_dash(x_values)

def compute_maxAbsErrs(h):
    y_delta_plus = delta_plus(x_values, h)
    y_delta_plus_absErr = np.abs(y_delta_plus - y_f_dash)
    ans_delta_plus = max(y_delta_plus_absErr)

    y_delta_c = delta_c(x_values, h)
    y_delta_c_absErr = np.abs(y_delta_c - y_f_dash)
    ans_delta_c = max(y_delta_c_absErr)
    
    return ans_delta_plus,ans_delta_c

def compute_theoreticalErrors(h):
    max_deltaPlusErr_th,max_deltaCErr_th = 0,0
    for x in np.linspace(0,1,100):
        max_doubleder_err = max(abs(f_doubledash(xx)) for xx in np.linspace(x,x+h,100))
        max_tripleder_err = max(abs(f_tripledash(xx)) for xx in np.linspace(x,x+h,100))
        max_deltaPlusErr_th = max(max_deltaPlusErr_th,(h/2)*max_doubleder_err)
        max_deltaCErr_th = max(max_deltaCErr_th,(h**2/6)*max_tripleder_err)
    return max_deltaPlusErr_th,max_deltaCErr_th

# Generating data for plotting
hs = [i*0.01 for i in range(1,101)]
maxErr_delta_plus,maxErr_delta_c=[],[]
for h in hs:
    aa, bb = compute_maxAbsErrs(h)
    maxErr_delta_plus.append(aa)
    maxErr_delta_c.append(bb)

theoErr_delta_plus,theoErr_delta_c=[],[]
for h in hs:
    aa, bb = compute_theoreticalErrors(h)
    theoErr_delta_plus.append(aa)
    theoErr_delta_c.append(bb)

# Plotting...
plt.plot(hs, maxErr_delta_plus, label="maximum absolute error in forward difference")
plt.plot(hs, maxErr_delta_c, label="maximum absolute error in central difference")
plt.plot(hs, theoErr_delta_plus, label="theoretical maximum absolute error in forward difference")
# plt.plot(hs, theoErr_delta_c, label="theoretical maximum absolute error in central difference")
plt.legend()
plt.title("maximum absolute error of approximations for " +r"$sin(x^2)$")
plt.xlabel("h")
plt.ylabel(r"$\epsilon$")
plt.grid()
plt.show()
