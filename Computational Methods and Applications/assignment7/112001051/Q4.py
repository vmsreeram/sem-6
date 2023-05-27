import math
import matplotlib.pyplot as plt

# Define the Newton-Raphson method function
def newtonRaphsonMethod(f, fdash, x0, K):
    # Initialize the array of values with x0 repeated K+1 times
    X = [x0 for _ in range(K+1)] 
    # Applying Newton Raphson Method
    for k in range(K):
        # Update the value of X[k+1] using the Newton-Raphson formula
        X[k+1] = X[k] - (f(X[k]) / fdash(X[k]))
    # Return the array of values
    return X

# Define the secant method function
def secantMethod(f, x0, x1, K):
    # Initialize the array of values with x0, x1, and K zeros
    X = [x0, x1]+[0 for k in range(K)]
    # Applying Secant Method
    for k in range(1,K+1):
        # Update the value of X[k+1] using the secant formula
        X[k+1] = X[k] - f(X[k]) * ((X[k] - X[k-1]) / (f(X[k]) - f(X[k-1])))
    # Return the array of values
    return X

# Define a function to calculate the rate of convergence
def convergenceRate(X):
    # Use the formula for q given on the Wikipedia page
    q = []
    for k in range(2, len(X) - 1):
        q.append(math.log(abs((X[k+1] - X[k]) / (X[k] - X[k-1])))/math.log(abs((X[k] - X[k-1]) / (X[k-1] - X[k-2]))))
    # Return the array of convergence rates
    return q

# Define the function f(x) = x * exp(-x)
def fun(x):
    return x * math.exp(-x)

# Define the derivative of f(x)
def fundash(x):
    return -((x-1) * math.exp(-x))

# Apply Newton-Raphson method to f(x)
newtonRaphsonOP = newtonRaphsonMethod(f=fun,fdash=fundash,x0=10,K=100)
# Apply Secant method to f(x)
secantOP = secantMethod(f=fun,x0=10,x1=11,K=100)

# Calculate the convergence rate for each method
newtonRaphsonOP_convergenceRate=convergenceRate(newtonRaphsonOP)
secantOP_convergenceRate=convergenceRate(secantOP)

# Plot the rate of convergence for each method
plt.title("Rate of Convergence")
plt.ylabel(r"$\alpha$")
plt.xlabel("number of iterations")
plt.plot(list(range(2, len(newtonRaphsonOP_convergenceRate) + 2)), newtonRaphsonOP_convergenceRate, label="Newton Raphson Method")
plt.plot(list(range(2, len(secantOP_convergenceRate) + 2)), secantOP_convergenceRate, label="Secant Method")
plt.legend()
plt.grid()
plt.show()