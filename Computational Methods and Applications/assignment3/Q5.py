import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.animation import FuncAnimation

# Define a function to be interpolated
def func(x):
    return np.tan(x)+np.sin(30*x)+np.exp(x)

# Define the interpolation methods to be used
interp_methods = ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic']

# Generate x values for the original function
x = np.linspace(0, 10, num=100)
y = func(x)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-8, 18)
ax.set_title('Interpolation Methods')

# Initialize the lines and points to be animated
lines = []
points = []
for method in interp_methods:
    line, = ax.plot([], [], '-', label=method)
    lines.append(line)
    point, = ax.plot([], [], 'o', color=line.get_color(), markersize=3)
    points.append(point)

ax.legend()

# Define the animation function
def update(frame):
    for i, method in enumerate(interp_methods):
        # Interpolate the function using the specified method
        num_points = 10 * (frame + 1)
        x_interp = np.linspace(0, 10, num=num_points)
        y_interp = interp1d(x, y, kind=method)(x_interp)
        lines[i].set_data(x_interp, y_interp)
        points[i].set_data(x_interp, y_interp)

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(10), interval=500)

plt.show()
