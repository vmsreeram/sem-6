import matplotlib.pyplot as plt

class Polynomial:
    def __init__(self,data=None):
        if data==None:
            raise TypeError("Polynomial need to be initialised with list")
        if type(data)!=list:
            raise TypeError("Invalid argument: Expected list of numbers, found "+str(type(data)))
        for val in data:
            if type(val)!=int and type(val)!=float:
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
            print("Warning: Only pre multiplication with number is asked in question")
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
        s = r'Plot of the polynomial $P(x)=$'
        initLen=len(s)
        if self.n>0:
            if self.data[0]!=0:
                if(self.data[0]>0):
                    s+=r'$+$'
                else:
                    s+=r'$-$'
                s+=str(abs(self.data[0]))
        if self.n>1:
            if self.data[1]!=0:
                if(self.data[1]>0):
                    s+=r'$+$'
                else:
                    s+=r'$-$'
                if abs(self.data[1])!=1:
                    s+=str(abs(self.data[1]))
                s+=r'$x$'
        if self.n>2:
            for i in range(2,self.n):
                if self.data[i]!=0:
                    if(self.data[i]>0):
                        s+=r'$+$'
                    else:
                        s+=r'$-$'
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
        plt.title(self.__title())
        plt.xlabel(r'$x$')
        plt.ylabel(r'$P(x)$')
        
        plt.grid()
        plt.show()
            
# p1 = Polynomial([1.2])
# p2 = Polynomial([1, 1, 1,5.2,25,.346,3])
# p3 = p2 * 4
# print(p3)
# p = Polynomial([1, 2, 3])
p = Polynomial([-1,2,0,-1,2,-3,4])
p.show(-2, 2)
