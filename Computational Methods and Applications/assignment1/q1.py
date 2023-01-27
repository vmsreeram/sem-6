import numpy as np
import matplotlib.pyplot as plt


def visualiseStrApprox(upto):
    upto+=1
    logFactN=[0]
    for i in range(2,upto+1):
        logFactN.append(logFactN[-1]+np.log(i))
    # print(logFactN)

    logStirN=[]
    for i in range(1,upto+1):
        logStirN.append((1/2)*np.log(2*np.pi*i)+i*np.log(i)-i)
    # print(logStirN)

    RelErr = []
    for i in range(1,upto+1):
        RelErr.append(abs(np.exp(logStirN[i-1]-logFactN[i-1])-1))
        
    figure, axis = plt.subplots(2)

    # axis[0].set_title('relative error plot')
    # axis[0].set_xlabel('n')
    # axis[0].set_ylabel('relative error')
    # axis[0].plot([i for i in range(len(RelErr))],RelErr)

    axis[0].set_title('percentage error plot')
    axis[0].set_xlabel('n')
    axis[0].set_ylabel('percentage error')
    axis[0].plot([i for i in range(len(RelErr))],[i*100 for i in RelErr])


    axis[1].plot([i for i in range(len(RelErr))],logFactN,color='b',label='logFactN')
    axis[1].plot([i for i in range(len(RelErr))],logStirN,color='r',label='logStirN')
    axis[1].set_title('log plot')
    axis[1].set_xlabel('n')
    axis[1].set_ylabel('log factorial (n)')
    axis[1].legend()
    plt.show()

visualiseStrApprox(1000000)