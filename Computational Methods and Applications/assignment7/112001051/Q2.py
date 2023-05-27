import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def heat_eq(u_0, g, m, f, mu=1):

    X, Y = np.mgrid[0:1:m*1j, 0:1:m*1j]
    xy = np.stack((X, Y))
    value = np.apply_along_axis(lambda i: g(*i), 0, xy)
    t = 0
    dx = 1/m

    def fwdEuler(dt):
        """
        u(i,j,t+1) = u(i,j,t+1) + (Mu*dt/(dx²)) * (u(i+1,j,t) + u(i-1,j,t) + u(i,j+1,t) + u(i,j-1,t) - 4u(i,j,t) + f(x,y,t))
        """
        nonlocal t
        r =  (mu*dt/dx**2)
        values_next = value.copy()
        
        for i in range(1,m-1):
            for j in range(1,m-1):
                values_next[i][j] += r * (
                    value[i+1][j] + value[i-1][j] + value[i][j+1] + value[i][j-1] - 4*value[i][j]
                    ) + f(*xy[:,i,j],t)

        edge_values = np.apply_along_axis(lambda pos: u_0(*pos, t), 0, xy)
        values_next[0,:] = edge_values[0]
        values_next[-1,:] = edge_values[-1]
        values_next[:,0] = edge_values[:,0]
        values_next[:,-1] = edge_values[:,-1]

        t += dt
        value[:, :] = values_next[:, :]


    def eqn():
        return value

    return fwdEuler, eqn


def animate(frame, eqn, dt, im):
    eqn[0](dt)
    im.set_data(eqn[1]())


def visualize_2d(xc, yc, m=20):
    def heat_PDE(x,y,t):
        return np.exp(-np.sqrt((x-xc)**2 + (y-yc)**2))
    def bound_cndn(x,y,t):
        return 0.0
    def init_cndn(x,y):
        return 0.0
    
    fwdEuler, eqn = heat_eq(
        bound_cndn, 
        init_cndn, 
        m, 
        heat_PDE
        )
    dt = 0.00001

    fig, ax = plt.subplots()
    im = ax.imshow(eqn(), vmin=0, vmax=350,cmap='hot')

    ani = animation.FuncAnimation(
        fig, animate, interval=2, 
        fargs=(heat_eq(bound_cndn, init_cndn, m, heat_PDE),dt,im)
        )

    plt.show()


visualize_2d(0.9, 0.9)