import numpy as np
import matplotlib.pyplot as plt


def visualiseStrApprox(upto):
    # Computing log of n! for all n from 1 to `upto`
    # using the fact that log(1*2*...*n)=log(1)+log(2)+...+log(n), as in this method, RHS does not cause an overflow.
    logFactN=[0]
    for i in range(2,upto+1):
        logFactN.append(logFactN[-1]+np.log(i))
    # print("logFactN[-1] =",logFactN[-1])

    # Computing log of stirling's approx of n! for all n from 1 to `upto`.
    logStirN=[]
    for i in range(1,upto+1):
        logStirN.append((1/2)*np.log(2*np.pi*i)+i*np.log(i)-i)
    # print("logStirN[-1] =",logStirN[-1])

    # relative error = |(actual - expected)/expected| 
    #                = |(actual/expected) - 1| 
    #                = | exp( log(actual)-log(expected) ) - 1|       (because log(a/b) = log(a)-log(b) and exp(log(a)) = a)
    # 
    RelErr = []
    for i in range(1,upto+1):
        RelErr.append(abs(np.exp(logStirN[i-1]-logFactN[i-1])-1))
    # print("RelErr[-1] =",RelErr[-1])
    
    # Plotting...
    fig, axis = plt.subplots(1,2, figsize=(15,5))

    axis[0].set_title('percentage error plot')
    axis[0].set_xlabel('n')
    axis[0].set_ylabel('percentage error in stirling\'s approximation of n!')
    axis[0].plot([i+1 for i in range(len(RelErr))],[i*100 for i in RelErr])
    axis[0].grid(linestyle='--')

    axis[1].plot([i+1 for i in range(len(RelErr))],logStirN,color='r',label='logStirN', linestyle = '-')
    axis[1].plot([i+1 for i in range(len(RelErr))],logFactN,color='b',label='logFactN', linestyle = ':')
    axis[1].set_title('log plot')
    axis[1].set_xlabel('n')
    axis[1].set_ylabel('log factorial (n)')
    axis[1].legend()
    axis[1].grid(linestyle='--')
    plt.show()

visualiseStrApprox(int(1e6))