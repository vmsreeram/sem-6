import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
import numpy as np

# Define initial temperature
def init_condn(x):
    # Create an array of zeros with the same shape as x
    temp = np.zeros_like(x)
    # Set interior temperature values using slicing
    temp[1:-1] = np.exp(-x[1:-1])
    return temp

# Define the PDE for heat conduction
def heat_conduction(t, temp, Mu):
    # Calculate the spatial step size
    dx = length / (len(temp) - 1)
    # Create an array of zeros with the same shape as temp
    temp_dt = np.zeros_like(temp)
    # Set the time derivative of temperature for interior points using slicing
    temp_dt[1:-1] = Mu * (temp[2:] - 2 * temp[1:-1] + temp[:-2]) / dx**2
    return temp_dt

# Define parameters
length = 1.0                # rod length 
Mu = 0.01                   # thermal diffusivity of the rod
time_span = (0, 10)         # for simulation
num_points = 100
pos = np.linspace(0, length, num_points)

# Solve the PDE using the initial condition and time span
initial_temp = init_condn(pos)
sol = solve_ivp(heat_conduction, time_span, initial_temp, args=(Mu,), t_eval=np.linspace(time_span[0], time_span[1], 100))

# Create the plot
fig, ax = plt.subplots()

# Define the animation function
def animate(i):
    # Clear the plot
    ax.clear()
    # Plot the temperature values at time i
    ax.plot(pos, sol.y[:, i])
    # Set the axis limits
    ax.set_xlim([0, length])
    ax.set_ylim([0, 1])
    # Set the axis labels and title
    ax.set_xlabel("Position")
    ax.set_ylabel("Temperature")
    ax.set_title("Time: "+str(sol.t[i]))

# Create the animation object
_ = FuncAnimation(fig, animate, frames=len(sol.t), interval=50)
# Show the plot
plt.show()