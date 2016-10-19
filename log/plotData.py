import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

#data = pd.DataFrame.from_csv('intersection_controller0.csv')
data = pd.read_csv('intersection_controller0.csv')
data.plot(colormap='winter',lw=1.3)

plt.show()
