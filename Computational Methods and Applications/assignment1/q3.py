import numpy as np
import matplotlib.pyplot as plt
import math

def estimatePi(n):
    def isInsideCircle(x,y):                                        # tells if (x,y) is inside a unit circle centered at the orign
        if(x*x + y*y <= 0.5*0.5):
            return True
        return False

    mn = [-0.5,-0.5]
    mx = [0.5,0.5]
    data = np.random.uniform(low=mn,high=mx,size=(n,2))             # data will have uniform points inside a unit square centered at the orign
    global no_inside,totalpts
    no_inside=0                                                     # number of points within a unit circle centered at the orign
    totalpts=0                                                      # number of points generated
    def findPi(isInside):                                           # computes Monte-Carlo estimate of pi, and auto-increments counters
        global no_inside,totalpts
        if(isInside):
            no_inside+=1
        totalpts+=1
        return (4*no_inside/totalpts)

    x = []
    y = []

    for point in data:                                              # storing computed Monte-Carlo estimate of pi for each point generated so that it can be used for plotitng
        cur = findPi(isInsideCircle(point[0],point[1]))
        y.append(cur)
        x.append(totalpts)
    
    # plotting ...
    plt.plot(x,y,label='Monte Carlo method')
    plt.axhline(y = math.pi, color = 'r', linestyle = '-',label='Value of math.pi')     # for horizontal line with the actual `math.pi`
    plt.ylim(3.10,3.20)                                                                 # forcing it, as the image in question says it
    plt.grid(color='grey', linestyle='--')
    plt.xlabel('No. of points generated')
    plt.ylabel('4 × fraction of points within the circle')
    plt.title('Estimating π using Monte Carlo Method')
    plt.legend(loc='lower right')

    print("Estimated π =",y[-1])
    print("Actual π =",math.pi)

    plt.show()

estimatePi(2000000)