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
        self.__data = data

    def __repr__(self):
        return ' '.join(map(str, self.__data))

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        return self.__data[index]

    def __setitem__(self, index, value):
        self.__data[index] = value

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Cannot add two row vectors of different lengths")
        return RowVectorFloat([self[i] + other[i] for i in range(len(self))])

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return RowVectorFloat([value * other for value in self.__data])
        raise ValueError("Invalid type for multiplication")

    def __rmul__(self, other):
        return self * other

class SquareMatrixFloat:
    def __init__(self,x:int):
        self.__size = x
        self.__data = [RowVectorFloat([0 for _ in range(x)]) for i in range(x)]
    
    def __repr__(self):
        ans = 'The matrix is:\n'
        for i in range(self.__size):
            for j in range(self.__size):
                ans+='%.2f\t' % abs(self.__data[i][j]) if ('%.2f' % self.__data[i][j] == '-0.00') else '%.2f\t' % (self.__data[i][j])
            ans+='\n'
        return ans

    # # should not be exposed to user, wrote for debugging purposes
    # def __setitem__(self, index, value):
    #     self.__data[index] = value

    def sampleSymmetric(self):
        for i in range(self.__size):
            for j in range(i,self.__size):
                if j==i:
                    self.__data[i][i]=np.random.uniform(0,self.__size)
                else:
                    self.__data[i][j]=self.__data[j][i]=np.random.uniform(0,1)
    
    def toRowEchelonForm(self):
        # check cases of div by 0
        for i in range(self.__size):
            # print("i =",i)
            for j in range(i,self.__size):
                self.__data[j]=(self.__data[j])*(1/self.__data[j][i])
                if(j>i):
                    self.__data[j]=self.__data[j]+(-1*self.__data[i])
                # for jj in range(self.__size):
                    # if(self.__data[j][jj]==-0.00):
                    #     self.__data[j][jj]=0.00
            # print(self)
    
    def isDRDominant(self,strict=False):
        for i in range(self.__size):
            cur=0
            flag=False
            for j in range(self.__size):
                cur+=abs(self.__data[i][j])
            if 2*abs(self.__data[i][i])<cur:
                return False
            if 2*abs(self.__data[i][i])>cur:
                flag = True
        if strict:
            return (True and flag)
        return True
    
    
    def jSolve(self, b,m):
        if not self.isDRDominant(strict=True):
            raise Exception('Not solving because convergence is not guranteed.')
        if len(b)!=self.__size:
            raise Exception('Not solving because b is not valid.')
        
        def __compute_error(A,x,b):
            n = self.__size
            ans=[]
            for i in range(n):
                cur=0
                for j in range(n):
                    cur += A[i][j]*x[j]
                ans.append(cur-b[i])
            return np.linalg.norm(ans,ord=2)
        errors=[]
        x_prev = [0]*self.__size
        x_curr = [0]*self.__size
        for _ in range(m):
            for i in range(self.__size):
                val=0
                for j in range(self.__size):
                    if j==i:
                        continue
                    val+=self.__data[i][j]*x_prev[j]
                x_curr[i]=(1/self.__data[i][i])*(b[i]-val)
            x_prev = x_curr
            errors.append(__compute_error(self.__data,x_curr,b))
        return errors,x_curr
    
    def gsSolve(self, b,m):
        if len(b)!=self.__size:
            raise Exception('Not solving because b is not valid.')
        
        def __compute_error(A,x,b):
            n = self.__size
            ans=[]
            for i in range(n):
                cur=0
                for j in range(n):
                    cur += A[i][j]*x[j]
                ans.append(cur-b[i])
            return np.linalg.norm(ans,ord=2)
        errors=[]
        x_prev = [0]*self.__size
        x_curr = [0]*self.__size
        
        for _ in range(m):
            for i in range(self.__size):
                val=0
                for j in range(self.__size):
                    if i<j:
                        val+=self.__data[i][j]*x_prev[j]
                    elif i>j:
                        val+=self.__data[i][j]*x_curr[j]
                        
                x_curr[i]=(1/self.__data[i][i])*(b[i]-val)
            x_prev = x_curr
            errors.append(__compute_error(self.__data,x_curr,b))
        
        return errors,x_curr

def visualisejSgsS(n:int,m:int):                                            # n: dimension of SquareMatrixFloat; m: number of iterations
    # print("findS...")
    s = SquareMatrixFloat(n)
    s.sampleSymmetric()
    while (not s.isDRDominant(strict=True)):                                # keep on sampling until strictly diagonally dominant SquareMatrixFloat is obtained
        s.sampleSymmetric()
    # print("foundS..")
    b = [random.randrange(1,n+1)]*n                                         # b is chosen from random integers from 1 to n
    jSerr,_ = s.jSolve(b,m)                                                 # call the implemented functions and plot the output
    gsSerr,_ = s.gsSolve(b,m)
    plt.plot([i+1 for i in range(m)],jSerr,label='Jacobi error')
    plt.plot([i+1 for i in range(m)],gsSerr,label='Gauss-Seidel error')
    plt.title(r'Errors $(\epsilon)$ in Jacobi and Gauss-Seidel methods')
    plt.xlabel('Number of iterations')
    plt.ylabel(r'$\epsilon$')
    plt.legend()
    plt.grid()
    plt.show()
    
visualisejSgsS(n=10,m=20)   # n: dimension of SquareMatrixFloat; m: number of iterations