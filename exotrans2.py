import serial as sr
import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.ndimage.filters import gaussian_filter1d
#from scipy.signal import savgol_filter
import liveplot as lp

s = sr.Serial('/dev/ttyACM0', 9600);       # Change the serial port according to device
start = time.time()
plt.close('all');
# plt.figure();
# plt.ion();
# plt.show();

data = np.array([]);

size = 250
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.zeros(len(x_vec))
plot_line = []

while True:	
	try:           
		a = s.readline()
		a.decode();
		if a ==  b'\r\n' or a == b'\n':               # To handle null value recieved
			#print("Got Blank!")
			continue
		#print('a = ', a);
		b = float(a[0:4]);
		#print('b = ' , b)
		y_vec[-1] = b
		plot_line = lp.live_plot(x_vec,y_vec,plot_line)
		y_vec = np.append(y_vec[1:],0.0)

	except KeyboardInterrupt:
		print("Press CTRL-C to terminate statement")
		end = time.time()
		print("Data Length: ", len(data), "Time Elapsed: ", end-start)
		break
s.close()
