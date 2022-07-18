import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


def objective(x, a, b):
	#return a * x + b


#x = [0.6, 0.9, 1.6, 1.8, 3.1, 4.2, 5.0, 6.0, 7.0, 8.1, 8.8]
#y = [1.32, 2.05, 3.72, 4.25, 7.45, 10.05, 11.84, 14.29, 16.15, 18.37, 19.91]
lol, _ = curve_fit(objective, x, y)
a, b = lol
print(a, b)

#xline = np.linspace(min(x), max(x), 200)

#yline = objective(xline, a, b)
plt.plot(xline, yline, '--', color='red')

plt.scatter(x, y)
plt.minorticks_on()
plt.grid(which='major', axis='y', color='green', linestyle='-', linewidth=0.5)
plt.grid(which='major', axis='x', color='green', linestyle='-', linewidth=0.5)
plt.grid(which='minor', axis='x', color='green', linestyle='--', linewidth=0.25)
plt.grid(which='minor', axis='y', color='green', linestyle='--', linewidth=0.25)
plt.show()
