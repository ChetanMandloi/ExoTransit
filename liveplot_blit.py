import time
import serial as sr
from matplotlib import pyplot as plt
import numpy as np

s = sr.Serial('/dev/ttyACM0', 9600);

def live_update_demo(blit = False):
    size = 300
    x = np.linspace(0,1,size+1)[0:-1]
    y_vec = np.zeros(len(x))

    fig = plt.figure()
    ax2 = fig.add_subplot(1, 1, 1)


    line, = ax2.plot([], lw=3)

    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim([15, 40])

    fig.canvas.draw()   # note that the first draw comes before setting data 


    if blit:
        # cache the background
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

    plt.show(block=False)


    t_start = time.time()
    k=0.

    while True:

        a = s.readline()
        a.decode();
        if a ==  b'\r\n' or a == b'\n':               # To handle null value recieved
        #    #print("Got Blank!")
            continue
        #print('a = ', a);
        b = float(a[0:4]);
        y_vec[-1] = b
        y_vec = np.append(y_vec[1:],0.0)

        print(x)
        line.set_data(x, y_vec)

        #print tx
        k+=0.11
        if blit:
            # restore background
            fig.canvas.restore_region(ax2background)

            # redraw just the points
            ax2.draw_artist(line)


            # fill in the axes rectangle
            fig.canvas.blit(ax2.bbox)

            # in this post http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
            # it is mentionned that blit causes strong memory leakage. 
            # however, I did not observe that.

        else:
            # redraw everything
            fig.canvas.draw()

        fig.canvas.flush_events()
        #alternatively you could use
        #plt.pause(0.000000000001) 
        # however plt.pause calls canvas.draw(), as can be read here:
        #http://bastibe.de/2013-05-30-speeding-up-matplotlib.html


live_update_demo(True)   # 70+ fps
#live_update_demo(False) # 25 fps

s.close()

