import liveplot as lp
import numpy as np


size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.random.randn(len(x_vec))
line1 = []
while True:
    try:
        rand_val = np.random.randn(1)
        y_vec[-1] = rand_val
        line1 = lp.live_plot(x_vec,y_vec,line1)
        y_vec = np.append(y_vec[1:],0.0)
    except KeyboardInterrupt:
        break
