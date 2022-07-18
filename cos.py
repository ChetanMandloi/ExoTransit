import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#from utils import period2freq, freq2period

xdat = []
for i in range(0,181,2):
    xdat.append(i)
ydat = [0.425	,0.425	,0.425	,0.425	,0.424	,0.424	,0.424	,0.423	,0.423	,0.422	,0.421	,0.419	,0.418	,0.417	,0.416	,0.414	,0.412	,0.41	,0.408	,0.406	,0.403	,0.4	,0.398	,0.397	,0.393	,0.388	,0.384	,0.38	,0.378	,0.374	,0.366	,0.36	,0.354	,0.348	,0.343	,0.333	,0.328	,0.32	,0.31	,0.304	,0.291	,0.278	,0.267	,0.256	,0.235	,0.212	,0.184	,0.185	,0.206	,0.222	,0.25	,0.266	,0.28	,0.289	,0.299	,0.311	,0.321	,0.327	,0.334	,0.341	,0.348	,0.355	,0.361	,0.366	,0.37	,0.375	,0.379	,0.384	,0.387	,0.39	,0.395	,0.398	,0.401	,0.403	,0.405	,0.407	,0.41	,0.413	,0.415	,0.416	,0.418	,0.419	,0.421	,0.422	,0.423	,0.424	,0.425	,0.425	,0.426,	0.427,	0.428]

def cos_func(times, amplitude, frequency):
    xyz = []
    for i in times:
        xyz.append(i*frequency)
    return amplitude * np.cos(xyz)

popt, pcov = curve_fit(cos_func,  # our function
                       xdat,  # measured x values
                       ydat,  # measured y values
                       p0=(3.0, 90))  # the initial guess for the two parameters


print(xdat, ydat)

fig, ax = plt.subplots(1, 1)
ax.plot(xdat, ydat, '.', label='Measured')
ax.plot(xdat, cos_func(xdat, popt[0], popt[1]), label='Best Fit')
ax.legend()
plt.show()
