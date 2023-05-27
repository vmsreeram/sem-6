import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def angular_to_coordinate(r, theta):
    return r*math.sin(theta),r*(-math.cos(theta))

def simpleGravityPendulum(theta_0, omega_0, h, t_max, g, L):
    t = []
    ti = 0
    while(ti < t_max):
        t.append(ti)
        ti += h
    t.append(t_max)
    
    theta = [theta_0 for i in range(len(t))]
    omega = [omega_0 for i in range(len(t))]
    # Apply the forward Euler method
    for i in range(len(t)-1):
        omega[i+1] = omega[i] - (g/L)*math.sin(theta[i])*h
        theta[i+1] = theta[i] + omega[i+1]*h
    
    # Set up the figure and axes for the plot
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-L * 1.5, L * 1.5)
    ax.set_ylim(-L * 1.5, L * 1.5)
    ax.set_title("Simple gravity pendulum")

    # Define the pendulum bob and cord
    cord, = ax.plot([], [], lw=1.5, c="k")
    bob = plt.Circle(angular_to_coordinate(L,theta_0), 0.05*L, fc="grey",zorder=3)

    # Define the animation functions
    def init():
        ax.add_patch(bob)
        return [cord,bob]

    def animate(i):
        nonlocal theta, omega
        x, y = angular_to_coordinate(L,theta[i])
        bob.set_center((x, y))
        cord.set_data([0, x], [0, y])
        return [cord,bob]
        

    # Create the animation and show it
    num_frames = int((t_max) / h)
    anim = FuncAnimation(fig, animate, init_func=init, frames=num_frames,interval=2.5, blit=True, repeat=True)
    plt.show()


simpleGravityPendulum(theta_0=math.pi/3,omega_0=0,h=0.01,t_max=100,g=9.81,L=1.0)
