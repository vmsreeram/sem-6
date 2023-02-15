class RowVectorFloat:
    def __init__(self, data=None):
        # disallowing invalid data passed
        if data==None:
            raise TypeError("RowVectorFloat need to be initialised with list")
        if type(data)!=list:
            raise TypeError("Invalid argument: Expected list of numbers, found "+str(type(data)))
        for val in data:
            if type(val)!=int and type(val)!=float:
                raise TypeError("Invalid argument: Expected list of only numbers, found an element of type "+str(type(val)))
        self.__data = data

    # for print(obj)
    def __repr__(self):
        return ' '.join(map(str, self.__data))

     # for len(obj)
    def __len__(self):
        return len(self.__data)

    # for getting value of obj[index]
    def __getitem__(self, index):
        return self.__data[index]

    # for setting value of obj[index] = value
    def __setitem__(self, index, value):
        self.__data[index] = value

    # to overload + 
    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Cannot add two row vectors of different lengths")
        return RowVectorFloat([self[i] + other[i] for i in range(len(self))])

    # to overload * in post-multiplication with num, like rr*2 
    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError("Invalid type for multiplication")
        return RowVectorFloat([value * other for value in self.__data])

    # to overload * in pre-multiplication with num, like 2*rr 
    def __rmul__(self, other):
        return self * other
rr = RowVectorFloat([6,9,4,4.2])

rr1 = rr*2
print(rr1)
