from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import math

def threeBodyProblem(init_r, init_v, t0, T, n):
    def get_norm(r1, r2):
        return max(np.linalg.norm(r2 - r1), 15)     # If norm is more than 15, returns 15

    def double_derivative(r1, r2, r3):
        norm1 = get_norm(r2, r1) ** 3
        norm2 = get_norm(r3, r1) ** 3
        rdouble_derivative = ((r2 - r1) / norm1) + ( (r3 - r1) / norm2)
        return list(rdouble_derivative)

    def three_body_derivatives(_, y):
        r1, r2, r3, v1, v2, v3 = np.reshape(y, (6, 2))
        v1d = double_derivative(r1, r2, r3)
        v2d = double_derivative(r2, r3, r1)
        v3d = double_derivative(r3, r1, r2)
        return np.concatenate((v1, v2, v3, v1d, v2d, v3d))

    # We evaluate at these time points
    t = np.linspace(t0, T, n)

    # Solving
    sol = solve_ivp(fun=three_body_derivatives, t_span=[t0, T], y0=[*init_r, *init_v], t_eval=t)

    # Values of points
    # print(len(sol.y))
    r1x,r1y,r2x,r2y,r3x,r3y,_,_,_,_,_,_ = sol.y

    # Figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(aspect="equal")

    # The three bodies
    bob_radius = 0.1
    body1 = ax.add_patch(plt.Circle((r1x[0], r1y[0]), bob_radius, color="r"))
    body2 = ax.add_patch(plt.Circle((r2x[0], r2y[0]), bob_radius, color="b"))
    body3 = ax.add_patch(plt.Circle((r3x[0], r3y[0]), bob_radius, color="g"))

    # Plotting the trajectories
    bodies = [body1, body2, body3]

    def init():
        # Setting title, labels, and plot limits
        ax.set_title("Three body problem")
        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.set_xlim(-2, 6)
        ax.set_ylim(-4, 4)

        # Returning
        return bodies

    def animate(i):
        # Update the positions of the circles
        body1.set_center((r1x[i], r1y[i]))
        body2.set_center((r2x[i], r2y[i]))
        body3.set_center((r3x[i], r3y[i]))

        # Returning
        return bodies

    # Setting up the animation
    anim = FuncAnimation(fig,animate,init_func=init,frames=len(r1x),repeat=True,interval=1,blit=True,)

    # Making custom legend
    line1 = Line2D([], [], color="white", marker='o', markersize=7, markerfacecolor="red")
    line2 = Line2D([], [], color="white", marker='o', markersize=7, markerfacecolor="blue")
    line3 = Line2D([], [], color="white", marker='o', markersize=7, markerfacecolor="green")
    plt.legend((line1, line2, line3), ('Body 1', 'Body 2', 'Body 3'), numpoints=1, loc=1)
    plt.show()


threeBodyProblem(init_r=[*[0, 0], *[3, math.sqrt(3)], *[3, -math.sqrt(3)]], init_v=[*[0, 0], *[0, 0], *[0, 0]], t0=0, T=800, n=2000)
