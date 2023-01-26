import matplotlib.pyplot as plt
import random

class Dice:
    def __init__(self, numSides=6):
        if type(numSides)!=int and type(numSides)!=float:
            raise Exception("Cannot construct the dice : Number of sides should be an integer")
        if (numSides//1 != numSides):
            raise Exception("Cannot construct the dice : Number of sides should not be a floating point number")
        if numSides < 4:
            raise Exception("Cannot construct the dice : Number of sides should be an integer greater than or equal to 4")
        numSides=int(numSides)
        self.numSides = numSides
        self.prob = [1/numSides for i in range(numSides)]
        
    def setProb(self, prob_tuple):
        if len(prob_tuple) != self.numSides:
            raise Exception("Invalid probability distribution: Tuple should have exactly {} elements".format(self.numSides))
        if abs(sum(prob_tuple) - 1) > 1e-6:
            raise Exception("Invalid probability distribution: Sum is not equal to 1")
        self.prob = prob_tuple
        
    def __str__(self):
        ans="Dice with {} sides with probability distribution {{".format(self.numSides)
        for i in range(len(self.prob)):
            ans+=(str(self.prob[i]))
            if i != len(self.prob)-1:
                ans+=(', ')
        ans+="}"
        return ans
    
    def roll(self, n):
        outcome = [random.choices(range(self.numSides), self.prob, k=n).count(i) for i in range(self.numSides)]
        expected_outcome = [n*p for p in self.prob]
        print("outcome =",outcome)
        print("expected_outcome =",expected_outcome)
        barWidth=0.3
        plt.bar([x+1-(barWidth/2) for x in range(self.numSides)], outcome,width=barWidth,color='b',label='Actual')
        plt.bar([x+1+(barWidth/2) for x in range(self.numSides)], expected_outcome,width=barWidth,color='r',label='Expected')
        plt.xlabel('Sides')
        plt.ylabel('Occurrences')
        plt.title('Outcome of {} throws of a {}-faced dice'.format(n,self.numSides))
        plt.xticks([x+1 for x in range(self.numSides)])
        plt.legend()
        plt.show()

d = Dice(5.0)
# d.setProb((0.1, 0.2, 0.1, 0.4,0.1))
print(d)
d.roll(10000)