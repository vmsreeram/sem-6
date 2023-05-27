import copy
from math import exp
import random
import numpy as np
import matplotlib.pyplot as plt
from numpy import float64, linalg, linspace

class Polynomial:
    def __init__(self,data=None):
        # Disallowing invalid calls
        if data==None:
            raise TypeError("Polynomial need to be initialised with list")
        if type(data)!=list:
            raise TypeError("Invalid argument: Expected list of numbers, found "+str(type(data)))
        for val in data:
            if type(val)!=int and type(val)!=float and type(val)!=float64:
                raise TypeError("Invalid argument: Expected list of only numbers, found an element of type "+str(type(val)))
        
        # Class variables are made private, to make them safe from external malicious users 
        self.__data = data
        self.__n = len(data)
    
    # For print(obj)
    def __str__(self):
        return 'Coefficients of the polynomial are:\n'+' '.join(str(i) for i in self.__data)
    
    # to overload +
    def __add__(self,other):
        if(type(other)!=Polynomial):                                            # Polynomial cannot be added with non-polynomial
            raise Exception('Unsupported adding')

        x=Polynomial([0 for _ in range(max(self.__n,other.__n))])
        for i in range(min(self.__n,other.__n)):                                # add until where both polys are valid (till min len)
            x.__data[i]+=other.__data[i]+self.__data[i]
        if(other.__n>self.__n):                                                 # then add rest
            for i in range(min(self.__n,other.__n),max(self.__n,other.__n)):
                x.__data[i]+=other.__data[i]
        elif(other.__n<self.__n):
            for i in range(min(self.__n,other.__n),max(self.__n,other.__n)):
                x.__data[i]+=self.__data[i]
        return x

    # to overload -
    def __sub__(self,other):
        if(type(other)!=Polynomial):
            raise Exception('Unsupported subtraction')
        
        return self+Polynomial([-1*other.__data[i] for i in range(other.__n)])
    
    # to overload pre-* with num
    def __rmul__(self,other):
        if(type(other)==int or type(other)==float):
            n_dec=1
            if(type(other)==float):
                n_dec = len(str(other).split(".")[1])               # computing num of decimal places, and round to that.
            return Polynomial([round(other*self.__data[i],n_dec) for i in range(self.__n)])
        raise Exception('Unsupported multiplication')
    
    # # to overload post-* with poly or num
    def __mul__(self,other):
        if(type(other) is Polynomial):
            x = [0 for _ in range((self.__n)+(other.__n)-1)]
            for i in range(self.__n):
                for j in range(other.__n):
                    x[i+j] += self.__data[i]*other.__data[j]
                
            return Polynomial(x)
        if(type(other)==int or type(other)==float):
            # print("Warning: Only pre multiplication with number is asked in question")
            n_dec=1
            if(type(other)==float):
                n_dec = len(str(other).split(".")[1])               # handling floating point precision inconsistencies, by rounding
            return Polynomial([round(other*self.__data[i],n_dec) for i in range(self.__n)])
    
    # to evaluate poly at some point
    def __getitem__(self, x):
        ans=0
        for i in range(self.__n):
            ans+=(x**i)*self.__data[i]
        return ans
    
    # helper function that returns LaTeX formatted string of the polynomial
    def __title(self):
        s = ''
        initLen=len(s)
        if self.__n>0:
            if self.__data[0]!=0:
                if(self.__data[0]<0):
                    s+=r'$-$'
                s+=str(abs(round(self.__data[0],3)))
        if self.__n>1:
            if self.__data[1]!=0:
                if(self.__data[1]<0):
                    s+=r'$-$'
                elif len(s)!=initLen:                       # no need of + if nothing printed till now, such as f(x)= +4x
                    s+=r'$+$'
                if abs(self.__data[1])!=1:
                    s+=str(abs(round(self.__data[1],3)))
                s+=r'$x$'
        if self.__n>2:
            for i in range(2,self.__n):
                if self.__data[i]!=0:
                    if(self.__data[i]<0):
                        s+=r'$-$'
                    elif len(s)!=initLen:
                        s+=r'$+$'
                    if abs(self.__data[i])!=1:
                        s+=str(abs(round(self.__data[i],3)))
                    s+=r'$x^{}$'.format(i)
        if len(s)==initLen:                                 # if empty polynomial is passed, 0 is assumed.
            s+=r'$0$'
        s += '(rounded)'
        return s
    
    def __round_vals(self):                                 # helper function to round to 4 dec places, to handle floating point precision mistakes
        for i in range(self.__n):
            self.__data[i]=round(self.__data[i],4)
            
    def show(self,a,b):
        __n_samples = 101                                   # number of points to uniformly sample btw a and b
        x = [a+(i*(b-a)/(__n_samples-1)) for i in range(__n_samples)]
        y = []
        for xi in x:
            y.append(self[xi])                              # evaluated value
        plt.plot(x,y)
        
        # plt.title('Plot of the polynomial '+''.join(r'${}{}x^{}$'.format(('+' if i>0 and ix>0 else ''),('' if (i)==1 else i if i!=-1 else '-'),ix) for ix,i in enumerate(self.__data)) )
        plt.title(r'Plot of the polynomial $P(x)=$'+self.__title())
        plt.xlabel(r'$x$')
        plt.ylabel(r'$P(x)$')
        
        # plt.grid()
        # plt.show()
    
    
    def fitViaMatrixMethod(self, points, dontPlot=False):
        # handling invalid cases
        if type(points) is not list:
            raise Exception('Invalid input : expected list')
        for point in points:
            if len(point)!=2 or (type(point[0])is not int and type(point[0])is not float and type(point[0])is not float64) or (type(point[1])is not int and type(point[1])is not float and type(point[1])is not float64):
                raise Exception('Invalid input : list elements should be length-2 tuples of numbers')
        
        # finding values of A,b (usual meanings, as in slide)
        A = []
        b = []
        xpts = []                                       # xpts,ypts are computed for ease of plotting scatter of given points
        ypts = []
        x_min,x_max = points[0][0],points[0][0]         # x_min,x_max are used to find range of plot
        for x,y in points:
            A.append([x**i for i in range(len(points))])
            b.append(y)
            xpts.append(x)
            ypts.append(y)
            x_min,x_max=min(x_min,x),max(x_max,x)        
        
        matmethod_poly=Polynomial(list(linalg.solve(A,b)))      # linalg.solve solves and returns coeff as iterable, Solution to the system a x = b. Returned shape is identical to b.
        
        
        if dontPlot:            # we don't want the fitting function called internally to display plot, so to return just ans.
            return matmethod_poly
        
        matmethod_poly.__round_vals()                           # rounding so that it does not look ugly while printing in plot
        
        # plotting ...
        # print(matmethod_poly_coef)
        # print(x_min,x_max)
        plt.scatter(xpts,ypts,c='r')
        x_vals = [x/100 for x in range(100*x_min, 1+100*x_max)]
        y_vals = [matmethod_poly[x] for x in x_vals]
        plt.plot(x_vals, y_vals,c='b')
        plt.grid()
        plt.title('Polynomial interpolation using matrix method\nwhere '+r'$f(x)=$'+matmethod_poly.__title())
        plt.xlabel(r'$x$')
        plt.ylabel(r'$f(x)$')
        plt.show()
        
    def fitViaLagrangePoly(self, points, dontPlot=False):
        # handling invalid cases
        if type(points) is not list:
            raise Exception('Invalid input : expected list')
        for point in points:
            if len(point)!=2 or (type(point[0])is not int and type(point[0])is not float and type(point[0])is not float64) or (type(point[1])is not int and type(point[1])is not float and type(point[1])is not float64):
                raise Exception('Invalid input : list elements should be length-2 tuples of numbers')
        
        xpts = []
        ypts = []
        x_min,x_max = points[0][0],points[0][0]
        for x,y in points:
            xpts.append(x)
            ypts.append(y)
            x_min,x_max=min(x_min,x),max(x_max,x)
        
        # solving for lagrange_poly using the algo
        lagrange_poly = Polynomial([0])
        for i in range(len(points)):
            nr,dr = Polynomial([1]),1
            for j in range(len(points)):
                if i!=j:
                    nr *= Polynomial([-xpts[j],1])
                    dr *= xpts[i]-xpts[j]
            lagrange_poly += (ypts[i]/dr)*nr
        
        if dontPlot:            # we don't want the fitting function called internally to display plot, so to return just ans.
            return lagrange_poly
        lagrange_poly.__round_vals()
        
        # plotting ...
        plt.scatter(xpts,ypts,c='r')
        x_vals = [x/100 for x in range(100*x_min, 1+100*x_max)]
        y_vals = [lagrange_poly[x] for x in x_vals]
        plt.plot(x_vals, y_vals,c='b')
        plt.grid()
        plt.title('Polynomial interpolation using Lagrange polynomial method\nwhere '+r'$\tilde{f}(x)=$'+lagrange_poly.__title())
        plt.xlabel(r'$x$')
        plt.ylabel(r'$\tilde{f}(x)$')
        plt.show()
    
    def derivative(self):
        lst = []
        for i,val in enumerate(self.__data[1:]):
            lst.append((i+1)*val)
        return Polynomial(lst)
    
    def area(self,start,stop, retValOnly=False):
        lst = [0]
        for i,val in enumerate(self.__data):
            lst.append(val/(i+1))
        ans = (Polynomial(lst)[stop]-Polynomial(lst)[start])
        if retValOnly:            # we don't want the area computing function called internally to print string, so to return just ans.
            return ans
        return 'Area in the interval ['+str(start)+', '+str(stop)+'] is: '+str(ans)
    
    def __pow__(self, n):
        if n < 0 or type(n)!=int:
            raise Exception("Power requires to be a non-negative integer")

        ans = Polynomial([1])
        for _ in range(n):
            ans = ans * self

        return ans
    
def FindRoots_Aberth(roots,maxIter=100):
    EPS = 0.001  # define a small number to represent the desired accuracy of roots
    poly = Polynomial([1])  # initialize a polynomial with a single root at 1 (identity polynomial)
    
    for root in roots:
        poly = poly * Polynomial([-root, 1])  # multiply the polynomial by factors (x - root)

    poly_deriv = poly.derivative()  # compute the derivative of the polynomial

    X = []
    for i in range(len(roots)):
        X.append(random.random() * np.average(roots))  # generate a list of random initial guesses for roots
    N = len(X)

    roots.sort()  # sort the actual roots in ascending order to compare with the computed roots
    
    # start the Aberth method to compute the roots of the polynomial ~ https://en.wikipedia.org/wiki/Aberth_method
    for iter in range(maxIter):
        X_next = []
        X.sort()  # sort the current computed roots in ascending order to compare with the actual roots
        flag = True

        # check if the computed roots are within EPS of the actual roots
        for i in range(N):
            if(abs(X[i] - roots[i]) > EPS):
                flag = False
                break

        # if the computed roots are within EPS of the actual roots, print and return the roots
        if(flag == True):
            print(poly)
            print("Roots:",X,"\n")
            return

        for i in range(N):
            dsum = 0  # initialize the denominator sum to zero
            for j in range(N):
                if(i != j and X[i] != X[j]):  # avoid division by zero
                    dsum += 1/(X[i] - X[j])  # compute the denominator sum

            # if the derivative is zero, set it to small num to avoid division by zero
            der = poly_deriv[X[i]] if(poly_deriv[X[i]] != 0) else 0.0001

            numr = poly[X[i]] / der  # compute the numerator
            denr = 1 - numr * dsum  # compute the denominator

            # add the new computed root to the list
            X_next.append(X[i]-numr/denr)

        # update the current roots to the new computed roots
        X.clear()
        for i in X_next:
            X.append(i)

    # if the maximum number of iterations is reached, print the polynomial and the computed roots
    print("More iterations needed")
    print(poly)
    print("Roots:",X,"\n")


# call the function with some example inputs
FindRoots_Aberth([31,41],maxIter=20)
FindRoots_Aberth([8,9,22,44],maxIter=20)
