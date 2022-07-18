import serial as sr
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import savgol_filter
#import liveplot

s = sr.Serial('/dev/ttyACM0', 9600);       # Change the serial port according to device
start = time.time()
plt.close('all');
plt.figure();
plt.ion();
plt.show();

data = np.array([]);

file1 = open('transit.xls', 'w')
i = 0
while True:	
	try:           
		a = s.readline()
		try:
			a.decode()
		except UnicodeDecodeError:
			continue
		if a == b'\r\n' or a == b'\n':  # To handle null values received without dying
			continue
		print('a = ', a);
		b = float(a[0:4]);
		print('b = ' , b)
		data = np.append(data, b);
		string_value=str(b);
		file1.write(string_value)
		file1.write("\n")
		plt.cla();
		plt.title('Demonstration of Planet Transit')
		plt.xlabel('Time (/s)');
		plt.ylabel('Intensity (/Lux)');
		y_fil = data
		#y_fil = gaussian_filter1d(data, sigma=1)
		y_fil = savgol_filter(data, 3, 1, mode='nearest')
		plt.plot(10*y_fil, color = "brown", linewidth = "1")
		plt.pause(0.001);
		i = i+1
	except KeyboardInterrupt:
		print("Press CTRL-C to terminate statement")
		end = time.time()
		print("Data Length: ", len(data), "Time Elapsed: ", end-start)
		break
file1.close();
s.close()
