import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks


def solve_van_der_pol(x0, v0, mu, t0, T, n):
    def fdash(t, y):
        x, v = y
        return [v, mu*(1 - x**2)*v - x]

    # Evaluate the solution at these time points
    t_eval = np.linspace(t0, T, n)

    # Solve the system of ODEs
    sol = solve_ivp(fun=fdash, t_span=[t0, T], y0=[x0, v0], t_eval=t_eval)
    # print(sol.y[0])
    
    # Plot the solution curve
    plt.plot(t_eval, sol.y[0])

    # Label the axes and add a title to the plot
    plt.xlabel(r"$t$")
    plt.ylabel(r"$x(t)$")
    plt.title("Van der Pol equation, "+r"$\mu$ = "+str(mu))

    # Compute the time period of the limit cycle
    pks,_ = find_peaks(sol.y[0])
    time_period = np.mean(np.diff(t_eval[pks]))

    print(f"The time period of the limit cycle for mu = {mu} is {time_period:.4f}")
    
    # Show the plot
    plt.grid()
    plt.show()


solve_van_der_pol(x0=0, v0=5, mu=0.05, t0=0, T=100, n=1000)
