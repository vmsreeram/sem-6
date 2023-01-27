import numpy as np
import matplotlib.pyplot as plt
import math

def estimatePi(n):
    def isInsideCircle(x,y):
        if(x*x + y*y <= 0.5*0.5):
            return True
        return False

    mn = [-0.5,-0.5]
    mx = [0.5,0.5]
    data = np.random.uniform(low=mn,high=mx,size=(n,2))
    global no_inside,totalpts
    no_inside=0
    totalpts=0
    def findPi(isInside):
        global no_inside,totalpts
        if(isInside):
            no_inside+=1
        totalpts+=1
        return (4*no_inside/totalpts)

    x = []
    y = []

    for point in data:
        cur = findPi(isInsideCircle(point[0],point[1]))
        y.append(cur)
        x.append(totalpts)
    plt.plot(x,y,label='Monte Carlo method')
    plt.axhline(y = math.pi, color = 'r', linestyle = '-',label='Value of math.pi')
    plt.ylim(3.10,3.20)
    plt.grid(color='grey', linestyle='--')
    plt.xlabel('No. of points generated')
    plt.ylabel('4 × fraction of points within the circle')
    plt.title('Estimating π using Monte Carlo Method')
    plt.legend(loc='lower right')

    print("Estimated π =",y[-1])
    print("Actual π =",math.pi)

    plt.show()

estimatePi(2000000)