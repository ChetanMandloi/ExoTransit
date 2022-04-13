import serial as sr
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import savgol_filter


s = sr.Serial('/dev/cu.usbmodem14101', 9600);
plt.close('all');
plt.figure();
plt.ion();
plt.show();

data = np.array([]);

file1 = open('transit.xls', 'w')
i = 0
try:
    while True:
        while i<10000:           
            a = s.readline()
            a.decode();
            b = float(a[0:4]);
            data = np.append(data, b);
            string_value=str(b);
            file1.write(string_value)
            file1.write("\n")
            plt.cla();
            plt.title('Demonstration of Planet Transit')
            plt.xlabel('Time (/s)');
            plt.ylabel('Intensity (/Lux)');
            #y_fil = gaussian_filter1d(data, sigma=1)
            y_fil = savgol_filter(data, 3, 1, mode='nearest')
            plt.plot(10*y_fil, color = "brown", linewidth = "1")
            plt.pause(0.001);
            i = i+1
except KeyboardInterrupt:
        print("Press CTRL-C to terminate statement")
        pass
file1.close();
s.close()
