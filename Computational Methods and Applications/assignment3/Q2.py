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
    
    def isDRDominant(self):
        for i in range(self.size):
            cur=0
            for j in range(self.size):
                cur+=abs(self.data[i][j])
            if 2*abs(self.data[i][i])<cur:
                return False
        return True
    
    ## TODO 1: implement jSolve
    ## TODO 2: implement gsSolve