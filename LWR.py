# IIT2019088 Ritik Kumar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def kernel(point, xmat, k):
    m,n = np.shape(xmat)
    weights = np.mat(np.eye((m)))
    for j in range(m):
        diff = point - X[j]
        weights[j,j] = np.exp(diff*diff.T/(-2.0*k**2))
    return weights

def localWeight(point, xmat, ymat, k):
    wei = kernel(point,xmat,k)

    XT_WX = np.matmul(xmat.T * wei, xmat)
    I_XT_WX = np.linalg.pinv(XT_WX)
    I_XT_WXXT_W = np.matmul(I_XT_WX, xmat.T * wei)
    I_XT_WXXT_WY = np.matmul(I_XT_WXXT_W, ymat.T)
    return I_XT_WXXT_WY 
     
def localWeightRegression(xmat, ymat, k):
    m,n = np.shape(xmat)
    ypred = np.zeros(m)
    for i in range(m):
        ypred[i] = xmat[i]*localWeight(xmat[i],xmat,ymat,k)
    return ypred
       
# load data points
data = pd.read_csv('Housing Price data set.csv')
Area = np.array(data.lotsize)
Price = np.array(data.price)
 
#preparing and add 1 in Area
mArea = np.mat(Area)
mPrice = np.mat(Price)

m= np.shape(mArea)[1]
one = np.mat(np.ones(m))
X = np.hstack((one.T,mArea.T))

#set k here
ypred = localWeightRegression(X,mPrice,5)

print(ypred)

error=np.array(abs(mPrice-ypred))
# print("Mean absolute percentage error : " + error)


SortIndex = X[:,1].argsort(0)
xsort = X[SortIndex][:,0]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(Area,Price)
ax.plot(xsort[:,1],ypred[SortIndex], color = 'red')
plt.xlabel('Total Area')
plt.ylabel('Price')
plt.show();
