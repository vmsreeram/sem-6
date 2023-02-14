import numpy as np
from scipy.interpolate import interp1d, CubicSpline, Akima1DInterpolator, BarycentricInterpolator
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the function to be interpolated
def f(x):
    return np.tan(x)*np.sin(30*x)*np.exp(x)

# Define the number of sampling points for the interpolation
num_points = [i for i in range(2,36)]


# Define the interpolation functions
interpolation_functions = [
                            CubicSpline
                           , Akima1DInterpolator
                           , BarycentricInterpolator
                           ]
interpolation_names = [
                        'Cubic Spline'
                       , 'Akima'
                       , 'Barycentric'
                       ]

interpolation_colors = [
                         'r'
                        , 'g'
                        , 'purple'
                        ]

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 1.0)
ax.set_ylim(-4.0, 4.0)


# Define the update function for the animation
def update(frame):
    ax.clear()
    # ax.set_xlim(0, 1.0)
    ax.set_ylim(-4.0, 4.0)

    num = num_points[frame]
    ax.set_title(r'Different interpolations for $tan(x) \cdot sin(30x) \cdot e^x$'+ ' for {} samples'.format(num))
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$f(x)$')
    ax.grid()
    
    x = np.linspace(0, 1.0, 500)
    y = f(x)
    ax.plot(x, y, label='True')
    
    # Generate the data for the plot for the current frame
    x = np.linspace(0, 1.0, num)
    y = f(x)


    # Plot the different interpolation functions
    for i, fn in enumerate(interpolation_functions):
        f_int = fn(x, y)
        x1=np.linspace(0, 1.0, 500)
        ax.plot(x1, f_int(x1), label=interpolation_names[i], c=interpolation_colors[i])

    # Add the legend
    ax.legend(loc='upper left')

# Generate the initial data for the plot

# Create and save the animation
anim = FuncAnimation(fig, update, frames=len(num_points), repeat=False)
anim.save('interpolation_animation.gif', writer='pillow')
