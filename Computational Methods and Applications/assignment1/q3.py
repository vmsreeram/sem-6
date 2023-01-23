import numpy as np
import matplotlib.pyplot as plt
import math

def isInsideCircle(x,y):
    if(x*x + y*y <= 0.5*0.5):
        return True
    return False

n = 2000000
mn = [-0.5,-0.5]
mx = [0.5,0.5]
data = np.random.uniform(low=mn,high=mx,size=(n,2))
# print (data)

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
Err = []
for point in data:
  cur = findPi(isInsideCircle(point[0],point[1]))
  y.append(cur)
  Err.append(abs(cur-math.pi))
  x.append(totalpts)
plt.plot(x,y)
plt.plot(x,Err)
plt.axhline(y = math.pi, color = 'r', linestyle = '-')

print(y[-1])
# TODO : separate graphs