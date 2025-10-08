import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import style

style.use("ggplot")
from scipy.fftpack import fft, fftfreq, ifft

# First create some toy data:
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x**2)

# Plotting
fig, ax = plt.subplots(1)

# Daten plotten
ax.plot(x, y)

# Ticks auf der x-Achse in 0.5er Schritten setzen
# np.arange(start, stop, step) erzeugt die gewünschten Werte
ax.set_xticks(np.arange(0, 2 * np.pi, 0.5))

plt.show()
