import matplotlib.pyplot as plt
from numpy import float64
from numpy import linalg

class Polynomial:
    def __init__(self,data=None):
        if data==None:
            raise TypeError("Polynomial need to be initialised with list")
        if type(data)!=list:
            raise TypeError("Invalid argument: Expected list of numbers, found "+str(type(data)))
        for val in data:
            if type(val)!=int and type(val)!=float and type(val)!=float64:
                raise TypeError("Invalid argument: Expected list of only numbers, found an element of type "+str(type(val)))
        
        # Handle more than 1 argument
        self.data = data
        self.n = len(data)
    
    def __str__(self):
        return 'Coefficients of the polynomial are:\n'+' '.join(str(i) for i in self.data)
    
    def __add__(self,other):
        if(type(other)!=Polynomial):
            raise Exception('Unsupported adding')

        x=Polynomial([0 for _ in range(max(self.n,other.n))])
        for i in range(min(self.n,other.n)):
            x.data[i]+=other.data[i]+self.data[i]
        if(other.n>self.n):
            for i in range(min(self.n,other.n),max(self.n,other.n)):
                x.data[i]+=other.data[i]
        elif(other.n<self.n):
            for i in range(min(self.n,other.n),max(self.n,other.n)):
                x.data[i]+=self.data[i]
        return x

    def __sub__(self,other):
        if(type(other)!=Polynomial):
            raise Exception('Unsupported subtraction')
        
        return self+Polynomial([-1*other.data[i] for i in range(other.n)])
    
    def __rmul__(self,other):
        if(type(other)==int or type(other)==float):
            n_dec=1
            if(type(other)==float):
                n_dec = len(str(other).split(".")[1])
            return Polynomial([round(other*self.data[i],n_dec) for i in range(self.n)])
        if(type(other)==Polynomial):
            x = Polynomial([0 for _ in range((self.n)+(other.n)-1)])
            for i in range((self.n)):
                x += (10*i*self.data[i])*other[i]
            return x
    
    def __mul__(self,other):
        if(type(other) is Polynomial):
            x = [0 for _ in range((self.n)+(other.n)-1)]
            for i in range(self.n):
                for j in range(other.n):
                    x[i+j] += self.data[i]*other.data[j]
                
            return Polynomial(x)
        if(type(other)==int or type(other)==float):
            # print("Warning: Only pre multiplication with number is asked in question")
            n_dec=1
            if(type(other)==float):
                n_dec = len(str(other).split(".")[1])
            return Polynomial([round(other*self.data[i],n_dec) for i in range(self.n)])
    
    def __getitem__(self, x):
        ans=0
        for i in range(self.n):
            ans+=(x**i)*self.data[i]
        return ans
    def __title(self):
        s = ''
        initLen=len(s)
        if self.n>0:
            if self.data[0]!=0:
                if(self.data[0]<0):
                    s+=r'$-$'
                s+=str(abs(self.data[0]))
        if self.n>1:
            if self.data[1]!=0:
                if(self.data[1]<0):
                    s+=r'$-$'
                elif len(s)!=initLen:
                    s+=r'$+$'
                if abs(self.data[1])!=1:
                    s+=str(abs(self.data[1]))
                s+=r'$x$'
        if self.n>2:
            for i in range(2,self.n):
                if self.data[i]!=0:
                    if(self.data[i]<0):
                        s+=r'$-$'
                    elif len(s)!=initLen:
                        s+=r'$+$'
                    if abs(self.data[i])!=1:
                        s+=str(abs(self.data[i]))
                    s+=r'$x^{}$'.format(i)
        if len(s)==initLen:
            s+=r'$0$'
        return s

    def show(self,a,b):
        __n_samples = 101
        x = [a+(i*(b-a)/(__n_samples-1)) for i in range(__n_samples)]
        y = []
        for xi in x:
            y.append(self[xi])
        plt.plot(x,y)
        
        # plt.title('Plot of the polynomial '+''.join(r'${}{}x^{}$'.format(('+' if i>0 and ix>0 else ''),('' if (i)==1 else i if i!=-1 else '-'),ix) for ix,i in enumerate(self.data)) )
        plt.title(r'Plot of the polynomial $P(x)=$'+self.__title())
        plt.xlabel(r'$x$')
        plt.ylabel(r'$P(x)$')
        
        plt.grid()
        plt.show()
    
    
    def fitViaMatrixMethod(self, points):
        if type(points) is not list:
            raise Exception('Invalid input : expected list')
        for point in points:
            if len(point)!=2 or (type(point[0])is not int and type(point[0])is not float) or (type(point[1])is not int and type(point[1])is not float):
                raise Exception('Invalid input : list elements should be length-2 tuples of numbers')
        
        A = []
        b = []
        xpts = []
        ypts = []
        x_min,x_max = points[0][0],points[0][0]
        for x,y in points:
            A.append([x**i for i in range(len(points))])
            b.append(y)
            xpts.append(x)
            ypts.append(y)
            x_min,x_max=min(x_min,x),max(x_max,x)
        
        matmethod_poly_coeff = list(linalg.solve(A,b))
        
        for i in range(len(matmethod_poly_coeff)):
            matmethod_poly_coeff[i] = round(matmethod_poly_coeff[i],4)
        matmethod_poly=Polynomial(matmethod_poly_coeff)
        
        # print(matmethod_poly_coef)
        # print(x_min,x_max)
        plt.scatter(xpts,ypts,c='r')
        x_vals = [x/100 for x in range(100*x_min, 100*x_max)]
        y_vals = [matmethod_poly[x] for x in x_vals]
        plt.plot(x_vals, y_vals,c='b')
        plt.grid()
        plt.title('Polynomial interpolation using matrix method\nwhere '+r'$f(x)=$'+matmethod_poly.__title())
        plt.xlabel(r'$x$')
        plt.ylabel(r'$f(x)$')
        plt.show()
        
    def fitViaLagrangePoly(self, points):
        if type(points) is not list:
            raise Exception('Invalid input : expected list')
        for point in points:
            if len(point)!=2 or (type(point[0])is not int and type(point[0])is not float) or (type(point[1])is not int and type(point[1])is not float):
                raise Exception('Invalid input : list elements should be length-2 tuples of numbers')
        
        xpts = []
        ypts = []
        x_min,x_max = points[0][0],points[0][0]
        for x,y in points:
            xpts.append(x)
            ypts.append(y)
            x_min,x_max=min(x_min,x),max(x_max,x)
        
        lagrange_poly = Polynomial([0])
        
        
        
# p = Polynomial([])
# p.fitViaLagrangePoly([(1,-4), (0,1), (-1, 4), (2, 4),  (3,1)])
            
# p1 = Polynomial([1,2])
# p2 = Polynomial([1, 1, 1,5.2,25,.346,3])
# p3 = p2 * p1
# print(p3)
# p = Polynomial([1, 2, 3])
p = Polynomial([1,-1,-0.2,0,2])
p.show(-2, 2)

p = Polynomial([])
p.fitViaMatrixMethod([(1,4), (0,1), (-1, 0), (2, 15), (3,12)])
