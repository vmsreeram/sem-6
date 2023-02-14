import numpy as np
import random
import matplotlib.pyplot as plt

class RowVectorFloat:
    def __init__(self, data=None):
        if data==None:
            raise TypeError("RowVectorFloat need to be initialised with list")
        if type(data)!=list:
            raise TypeError("Invalid argument: Expected list of numbers, found "+str(type(data)))
        for val in data:
            if type(val)!=int and type(val)!=float:
                raise TypeError("Invalid argument: Expected list of only numbers, found an element of type "+str(type(val)))
        # Handle more than 1 argument
        self.data = data

    def __repr__(self):
        return ' '.join(map(str, self.data))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Cannot add two row vectors of different lengths")
        return RowVectorFloat([self[i] + other[i] for i in range(len(self))])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return RowVectorFloat([value * other for value in self.data])
        raise ValueError("Invalid type for multiplication")

    def __rmul__(self, other):
        return self * other

class SquareMatrixFloat:
    def __init__(self,x:int):
        self.size = x
        self.data = [RowVectorFloat([0 for _ in range(x)]) for i in range(x)]
    
    def __repr__(self):
        ans = 'The matrix is:\n'
        for i in range(self.size):
            for j in range(self.size):
                # ans+=str('%.2f' % self.data[i][j])+'\t'
                ans+=str('%.2f' % abs(self.data[i][j]) if self.data[i][j] == 0 else '%.2f' % self.data[i][j])+'\t'
            ans+='\n'
        return ans

    def __setitem__(self, index, value):
        self.data[index] = value

    def sampleSymmetric(self):
        for i in range(self.size):
            for j in range(i,self.size):
                if j==i:
                    self.data[i][i]=np.random.uniform(0,self.size)
                else:
                    self.data[i][j]=self.data[j][i]=np.random.uniform(0,1)
    
    def toRowEchelonForm(self):
        # check cases of div by 0
        for i in range(self.size):
            # print("i =",i)
            for j in range(i,self.size):
                self.data[j]=(self.data[j])*(1/self.data[j][i])
                if(j>i):
                    self.data[j]=self.data[j]+(-1*self.data[i])
                # for jj in range(self.size):
                    # if(self.data[j][jj]==-0.00):
                    #     self.data[j][jj]=0.00
            # print(self)
    
    def isDRDominant(self,strict=False):
        for i in range(self.size):
            cur=0
            flag=False
            for j in range(self.size):
                cur+=abs(self.data[i][j])
            if 2*abs(self.data[i][i])<cur:
                return False
            if 2*abs(self.data[i][i])>cur:
                flag = True
        if strict:
            return (True and flag)
        return True
    
    
    ## TODO 1: implement jSolve
    def jSolve(self, b,m):
        if not self.isDRDominant(strict=True):
            raise Exception('Not solving because convergence is not guranteed.')
        if len(b)!=self.size:
            raise Exception('Not solving because b is not valid.')
        
        def __compute_error(A,x,b):
            n = self.size
            ans=[]
            for i in range(n):
                cur=0
                for j in range(n):
                    cur += A[i][j]*x[j]
                ans.append(cur-b[i])
            return np.linalg.norm(ans,ord=2)
        errors=[]
        x_prev = [0]*self.size
        x_curr = [0]*self.size
        for _ in range(m):
            for i in range(self.size):
                val=0
                for j in range(self.size):
                    if j==i:
                        continue
                    val+=self.data[i][j]*x_prev[j]
                x_curr[i]=(1/self.data[i][i])*(b[i]-val)
            x_prev = x_curr
            errors.append(__compute_error(self.data,x_curr,b))
        return errors,x_curr
    
    ## TODO 2: implement gsSolve
    def gsSolve(self, b,m):
        if len(b)!=self.size:
            raise Exception('Not solving because b is not valid.')
        
        def __compute_error(A,x,b):
            n = self.size
            ans=[]
            for i in range(n):
                cur=0
                for j in range(n):
                    cur += A[i][j]*x[j]
                ans.append(cur-b[i])
            return np.linalg.norm(ans,ord=2)
        errors=[]
        x_prev = [0]*self.size
        x_curr = [0]*self.size
        
        for _ in range(m):
            for i in range(self.size):
                val=0
                for j in range(self.size):
                    if i<j:
                        val+=self.data[i][j]*x_prev[j]
                    elif i>j:
                        val+=self.data[i][j]*x_curr[j]
                        
                x_curr[i]=(1/self.data[i][i])*(b[i]-val)
            x_prev = x_curr
            errors.append(__compute_error(self.data,x_curr,b))
        
        return errors,x_curr

def visualisejSgsS(n:int,m:int):
    # print("findS...")
    s = SquareMatrixFloat(n)
    s.sampleSymmetric()
    while (not s.isDRDominant(strict=True)):
        s.sampleSymmetric()
    # print("foundS..")
    b = [random.randrange(1,n+1)]*n
    jSerr,_ = s.jSolve(b,m)
    gsSerr,_ = s.gsSolve(b,m)
    plt.plot([i+1 for i in range(m)],jSerr,label='Jacobi error')
    plt.plot([i+1 for i in range(m)],gsSerr,label='Gauss-Siedel error')
    plt.title('Errors in Jacobi and Gauss-Siedel methods')
    plt.xlabel(r'$x$')
    plt.ylabel(r'$\epsilon$')
    plt.legend()
    plt.grid()
    plt.show()
    
visualisejSgsS(n=8,m=20)