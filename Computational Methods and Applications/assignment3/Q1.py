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
rr = RowVectorFloat([6,9,4,4.2])

rr1 = rr*2
print(rr1)
