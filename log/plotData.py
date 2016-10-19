import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

#data = pd.DataFrame.from_csv('intersection_controller0.csv')
data0 = pd.read_csv('intersection_controller0.csv')
data0.plot(colormap='Spectral',lw=1.3)
plt.title("intersection_controller0")
plt.xlabel('index')
plt.ylabel('Density')

#plt.figure()
data1 = pd.read_csv('intersection_controller1.csv')
data1.plot(colormap='Spectral',lw=1.3)
plt.title("intersection_controller1")
plt.xlabel('index')
plt.ylabel('Density')

plt.show()
