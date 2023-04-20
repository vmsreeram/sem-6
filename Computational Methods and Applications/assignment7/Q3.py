def nthRoot(n,a,eps):
    l=0
    h=a
    # binary searching
    while abs(l - h) > eps:
        c = (l + h) / 2      # mid point
        if c**n <= a:        # if nth power of mid point <= a
            l = c
        else:                #              "            >
            h = c
    return(l + h) / 2

eps = 0.0001
n = 12
num = 9**n

print(nthRoot(n,num,eps))