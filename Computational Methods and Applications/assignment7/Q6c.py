import numpy as np
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = np.array(coeffs, dtype=np.float64)
        self.degree = len(coeffs) - 1
        
    def evaluate(self, x):
        y = self.coeffs[-1]
        for i in range(self.degree - 1, -1, -1):
            y = y * x + self.coeffs[i]
            if abs(y) > 1e12:
                y /= abs(y)
                self.coeffs /= abs(y)
        return y
    
    def derivative(self):
        dcoeffs = self.coeffs[:-1] * np.arange(self.degree, 0, -1)
        return Polynomial(dcoeffs)
    
    def __str__(self):
        terms = []
        for i in range(self.degree, -1, -1):
            if np.abs(self.coeffs[i]) > 1e-10:
                if i == self.degree:
                    terms.append("{:.2f}x^{}".format(self.coeffs[i], i))
                elif i == 1:
                    terms.append("{:.2f}x".format(self.coeffs[i]))
                else:
                    terms.append("{:.2f}x^{}".format(self.coeffs[i], i))
        return " + ".join(terms)

    def printRoots(self):
        # Initialize the guess array with zeros
        guess = np.zeros((self.degree,), dtype=np.complex128)
        
        # Iterate until convergence
        while True:
            print(".",end="")
            # Compute the Jacobian matrix
            J = np.zeros((self.degree, self.degree), dtype=np.complex128)
            for i in range(self.degree):
                for j in range(self.degree):
                    if i == j:
                        J[i][j] = 1.0
                    else:
                        J[i][j] = guess[i] - guess[j]
            
            # Compute the function values and the error vector
            f = np.zeros((self.degree,), dtype=np.complex128)
            e = np.zeros((self.degree,), dtype=np.complex128)
            for i in range(self.degree):
                f[i] = self.evaluate(guess[i])
                e[i] = f[i] / np.prod([guess[i] - guess[j] + 1e-10 for j in range(self.degree) if j != i])
            
            # Compute the update vector
            delta = np.linalg.solve(J, -e)
            
            # Update the guesses
            for i in range(self.degree):
                guess[i] += delta[i]
            
            # Check for convergence
            if np.max(np.abs(delta)) < 1e-3:
                break
        
        # Output the roots
        roots = []
        for g in guess:
            if np.abs(g.imag) < 1e-3:
                roots.append(g.real)
            else:
                roots.append(g)
        print("Roots:", roots)

        
p = Polynomial([1, -4, -5, 14, 0, -3])
p.printRoots()
