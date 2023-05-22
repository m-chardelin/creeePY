import matplotlib.pyplot as plt
import numpy as np
  
# unit value1 ellipse


x, y, s, c= np.random.rand(4, 99)
s *= 10**2.

def plot(x, y, color, c, cmap):
      
    fig, ax = plt.subplots()
    ax.scatter(x, y, facecolor = color, c = c, cmap = cmap, marker = 'o')
    ax.set_title("matplotlib.axes.Axes.scatter Example1")
    plt.show()

plot(x, y, 'red', None, False)
