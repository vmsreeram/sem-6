import numpy as np

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
        # class data members are made private for protection from malicious users
        self.__size = x
        self.__data = [RowVectorFloat([0 for _ in range(x)]) for _ in range(x)]     # we fill with 0s on initialisation, as asked in qn
    
    # for print(obj)
    def __repr__(self):
        ans = 'The matrix is:\n'
        for i in range(self.__size):
            for j in range(self.__size):
                #                  print 0.00 instead of -0.00,                                         else print self.__data[i][j]
                ans+='%.2f\t' % abs(self.__data[i][j]) if ('%.2f' % self.__data[i][j] == '-0.00') else '%.2f\t' % (self.__data[i][j])
            ans+='\n'
        return ans

    # # should not be exposed to general user, wrote for debugging purposes
    # def __setitem__(self, index, value):
    #     self.__data[index] = value

    def sampleSymmetric(self):
        for i in range(self.__size):
            for j in range(i,self.__size):
                if j==i:
                    self.__data[i][i]=np.random.uniform(0,self.__size)              # as asked in qn
                else:
                    self.__data[i][j]=self.__data[j][i]=np.random.uniform(0,1)      # as asked in qn
    
    def toRowEchelonForm(self):                                                     #reduce self with reduced row echelon form
        for i in range(self.__size):                                                # for each row r1
            # print("i =",i)
            for j in range(i,self.__size):                                          #   for each (r1 || subsequent row) r2
                self.__data[j]=(self.__data[j])*(1/self.__data[j][i])               #       set the diag entry to 1, by dividing r2 with the ele at r1's index
                if(j>i):                                                            #       if r2!=r1   
                    self.__data[j]=self.__data[j]+(-1*self.__data[i])               #           use r1 to apply subtraction operation to get 0 in rows below diag ele of r1
            # print(self)
    
    def isDRDominant(self,strict=False):                                            # function to check if it is (strictly or not strictly) diagonally row dominant
        for i in range(self.__size):
            cur=0
            flag=False
            for j in range(self.__size):
                cur+=abs(self.__data[i][j])
            if 2*abs(self.__data[i][i])<cur:
                return False                                                        # not diagonally dominant if at least one row has 2*abs(row_diag_val)<row_sum
            if 2*abs(self.__data[i][i])>cur:
                flag = True                                                         # found at least one row which follows 2*abs(row_diag_val)>row_sum (necessary condition for strict diagonal row dominance)
        if strict:
            return (True and flag)                                                  # if we are interested in finding strict dominance,we return True if flag is True
        return True                                                                 # if not, return True (we are not interested in finding strict dominance)
    
    def __compute_error(self,x,b):                                                  # helper function for jSolve and gsSolve to compute error ||Ax^(k) − b||_2 
        n = self.__size
        ans=[]
        for i in range(n):
            cur=0
            for j in range(n):
                cur += self.__data[i][j]*x[j]
            ans.append(cur-b[i])
        return np.linalg.norm(ans,ord=2)
        
    def jSolve(self, b,m):
        if not self.isDRDominant(strict=True):                                      # ***Given in slides that it has to be strictly diagonally dominant for jSolve to work***
            raise Exception('Not solving because convergence is not guranteed.')
        if len(b)!=self.__size:                                                     # reject cases where b is invalid
            raise Exception('Not solving because b is not valid.')
        
        errors=[]
        x_prev = [0]*self.__size
        x_curr = [0]*self.__size
        for _ in range(m):                                                          # for each iteration, run the algorithm, append computed error
            for i in range(self.__size):
                val=0
                for j in range(self.__size):
                    if j==i:
                        continue
                    val+=self.__data[i][j]*x_prev[j]
                x_curr[i]=(1/self.__data[i][i])*(b[i]-val)
            x_prev = x_curr
            errors.append(self.__compute_error(x_curr,b))
        return errors,x_curr
    
    def gsSolve(self, b,m):
        if len(b)!=self.__size:                                                     # reject cases where b is invalid
            raise Exception('Not solving because b is not valid.')
        
        errors=[]
        x_prev = [0]*self.__size
        x_curr = [0]*self.__size
        
        for _ in range(m):                                                          # for each iteration, run the algorithm, append computed error
            for i in range(self.__size):
                val=0
                for j in range(self.__size):
                    if i<j:
                        val+=self.__data[i][j]*x_prev[j]
                    elif i>j:
                        val+=self.__data[i][j]*x_curr[j]
                        
                x_curr[i]=(1/self.__data[i][i])*(b[i]-val)
            x_prev = x_curr
            errors.append(self.__compute_error(x_curr,b))
        
        return errors,x_curr

s = SquareMatrixFloat(4)
s.sampleSymmetric()
(e, x) = s.gsSolve([1, 2, 3, 4], 10)
print(x)
print(e)
# (e1, x1) = s.jSolve([1, 2, 3, 4], 10)
# print(x1)
# print(e1)

# s = SquareMatrixFloat(4)
# rvf1=RowVectorFloat([3,     0.2,    0.3,    0.1])
# rvf2=RowVectorFloat([0.2,   2,      0.1,    0.4])
# rvf3=RowVectorFloat([0.3,   0.1,    3,      0.3])
# rvf4=RowVectorFloat([0.1,   0.4,    0.3,    1  ])
# s[0]=rvf1                                           # uncomment 53-55 for this to be supported
# s[1]=rvf2                                           #   "           "
# s[2]=rvf3                                           #    "           "
# s[3]=rvf4                                           #     "           "
# print(s)
# s.toRowEchelonForm()
# print(s)
# (e, x) = s.gsSolve([1, 2, 3, 4], 10)
# print(x)
# print(e)
# (e1, x1) = s.jSolve([1, 2, 3, 4], 10)
# print(x1)
# print(e1)