import serial as sr
import time
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import savgol_filter


s = sr.Serial('/dev/ttyACM0', 9600);
start = time.time()

data = np.array([]);
i = 0
target = 361
try:
    while True:
        while i<10000:           
            a = s.readline()
            a.decode();
            if a ==  b'\r\n':                        # To handle null value recieved
                #print("Got Blank!")
                continue
            b = float(a[0:4]);
            data = np.append(data, b);
            if len(data) > target:
                end = time.time()
                print("Data Length: ", len(data), "Time Elapsed: ", end-start)
                break
            i = i+1
        break
except KeyboardInterrupt:
        print("Press CTRL-C to terminate statement")
        end = time.time()
        print("Data Length: ", len(data), "Time Elapsed: ", end-start)
        pass
s.close()
