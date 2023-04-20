import math
import matplotlib.pyplot as plt


def newtonRaphsonMethod(f, fdash, x0, K):
    X = [x0 for _ in range(K+1)] 
    # Applying Newton Raphson Method
    for k in range(K):
        X[k+1] = X[k] - (f(X[k]) / fdash(X[k]))
    return X


def secantMethod(f, x0, x1, K):
    X = [x0, x1]+[0 for k in range(K)]
    # Applying Secant Method
    for k in range(1,K+1):
        X[k+1] = X[k] - f(X[k]) * ((X[k] - X[k-1]) / (f(X[k]) - f(X[k-1])))
    return X

def convergenceRate(X):
    # wiki https://en.wikipedia.org/wiki/Rate_of_convergence#cite_note-6:~:text=.-,%5B6%5D,-Q%2Dconvergence%20definitions
    q = []
    for k in range(2, len(X) - 1):
        q.append(math.log(abs((X[k+1] - X[k]) / (X[k] - X[k-1])))/math.log(abs((X[k] - X[k-1]) / (X[k-1] - X[k-2]))))
    return q

def fun(x):
    return x * math.exp(-x)


def fundash(x):
    return -((x-1) * math.exp(-x))

newtonRaphsonOP = newtonRaphsonMethod(f=fun,fdash=fundash,x0=10,K=100)
secantOP = secantMethod(f=fun,x0=10,x1=11,K=100)

# print(newtonRaphsonOP)
# print(secantOP)

newtonRaphsonOP_convergenceRate=convergenceRate(newtonRaphsonOP)
secantOP_convergenceRate=convergenceRate(secantOP)

plt.title("Rate of Convergence")
plt.ylabel(r"$\alpha$")
plt.xlabel("number of iterations")
plt.plot(list(range(2, len(newtonRaphsonOP_convergenceRate) + 2)), newtonRaphsonOP_convergenceRate, label="Newton Raphson Method")
plt.plot(list(range(2, len(secantOP_convergenceRate) + 2)), secantOP_convergenceRate, label="Secant Method")
plt.legend()
plt.grid()
plt.show()