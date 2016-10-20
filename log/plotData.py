import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import numpy as np
import statsmodels.api as sm

#path = './timer'
path = './densities'
#path = './communication'

#http://stackoverflow.com/questions/6963035/pyplot-axes-labels-for-subplots
#One simple way using subplots
fig = plt.figure()
ax = fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
ax0 = fig.add_subplot(223)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(224)
ax.set_xlabel('index')
ax.set_ylabel('Density')
#___________________________________________________

#data = pd.DataFrame.from_csv('intersection_controller0.csv')
data0 = pd.read_csv(path+'/intersection_controller0.csv')
#individual mean: data0.segment0.mean()
print "Seg0(S) means:\n%s" %(data0.mean())
data0.plot(ax=ax0)
ax0.set_title("intersection_controller0")

x = data0.index
model = sm.formula.ols(formula='segment0 ~ np.power(x,3) + np.power(x,2) + x', data=data0)
res = model.fit()
#print res.summary()
data0.assign(fit0=res.fittedvalues).plot(x=x, y='fit0', ax=ax0)

data1 = pd.read_csv(path+'/intersection_controller1.csv')
print "Seg1(N) means:\n%s" %(data1.mean())
#ax1.plot(data1)
data1.plot(ax=ax1)
#ax1.legend(data1)
ax1.set_title("intersection_controller1")


data2 = pd.read_csv(path+'/intersection_controller2.csv')
print "Seg2(W) means:\n%s" %(data2.mean())
#ax2.plot(data2)
data2.plot(ax=ax2)
#ax2.legend(data2)
ax2.set_title("intersection_controller2")


data3 = pd.read_csv(path+'/intersection_controller3.csv')
print "Seg3(E) means:\n%s" %(data3.mean())
#ax3.plot(data3)
data3.plot(ax=ax3)
#ax3.legend(data3)
ax3.set_title("intersection_controller3")



'''

data2 = pd.read_csv(path+'/intersection_controller2.csv')
data2.plot(colormap='Spectral',lw=1.3)
plt.title("intersection_controller2")
plt.xlabel('index')
plt.ylabel('Density')

data3 = pd.read_csv(path+'/intersection_controller3.csv')
data3.plot(colormap='Spectral',lw=1.3)
plt.title("intersection_controller3")
plt.xlabel('index')
plt.ylabel('Density')
'''
plt.show()
