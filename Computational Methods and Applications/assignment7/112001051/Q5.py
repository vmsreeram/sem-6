import numpy as np
from scipy.linalg import inv
import matplotlib.pyplot as plt

# Define the system of equations as a function of x
def f(x):
    f1 = 3*x[0] - np.cos(x[1]*x[2]) - 3/2
    f2 = 4*x[0]**2 - 625*x[1]**2 + 2*x[2] - 1
    f3 = 20*x[2] + np.exp(-x[0]*x[1]) + 9
    return np.array([f1, f2, f3])

# Define the Jacobian matrix of the system of equations as a function of x
def J(x):
    j11,j12,j13 = 3,x[2]*np.sin(x[1]*x[2]),x[1]*np.sin(x[1]*x[2])
    j21,j22,j23 = 8*x[0],-1250*x[1],2
    j31,j32,j33 = -x[1]*np.exp(-x[0]*x[1]),-x[0]*np.exp(-x[0]*x[1]),20
    return np.array([[j11, j12, j13], [j21, j22, j23], [j31, j32, j33]])

# Implement the Newton-Raphson method to solve the system of equations
def newtonRaphson(x0, tol=1e-6, max_iter=100):
    x = x0
    f_norm = []
    for _ in range(max_iter):
        # Calculate the value of f(x) and its norm
        f_val = f(x)
        f_norm_val = np.linalg.norm(f_val)
        f_norm.append(f_norm_val)
        # Check if the norm is below the tolerance level
        if f_norm_val < tol:
            break
        # Calculate the Jacobian matrix and its inverse
        J_val = J(x)
        J_inv = inv(J_val)
        # Update the value of x using the Newton-Raphson formula
        x = x - J_inv.dot(f_val)
    # Return the solution x and the sequence of f norms
    return x, f_norm

# Set the initial guess for x and solve the system of equations using Newton-Raphson method
x0 = np.array([1, 2, 3])
sol, f_norm = newtonRaphson(x0=x0)

# Print the solution
print("x =", sol)

# Plot the sequence of f norms over the iterations
plt.plot(f_norm)
plt.grid()
plt.xlabel("Iteration number")
plt.ylabel("||f("+r"$x_k$"+")||")
plt.title("||f("+r"$x_k$"+")|| vs number of iterations")
plt.show()