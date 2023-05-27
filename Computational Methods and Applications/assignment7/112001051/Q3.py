# Function to find the nth root of a number using binary search
def nthRoot(n, a, eps):
    # Initialize the lower and upper bounds of the search
    l = 0
    h = a

    # Perform binary search until the given tolerance is >= the difference between the bounds 
    while eps < abs(l - h):
        # Calculate the midpoint of the bounds
        c = (l + h) / 2

        # If the nth power of the midpoint is less than or equal to the input number, update the lower bound
        if c**n <= a:
            l = c
        # Otherwise, update the upper bound
        else:
            h = c

    # Return the average of the final lower and upper bounds as the estimate for the nth root
    return (l + h) / 2

# Set the tolerance and the value of n and num to find the nth root of 9^n
eps = 0.0001
n = 12
num = 99**n

# Call the nthRoot function to find the nth root of num and print the result
print(nthRoot(n, num, eps))