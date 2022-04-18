########################################################################################################################
#
#   liveplot_blit.py
#   Takes data live from serial port and uses bliting to produce graphs at frame rates 5-6 times faster than regular
#   WARNING: Bliting can cause memory leak issues in some configurations, although I didn't observe any yet.
#   Chetan Mandloi
#   HBCSE
#
########################################################################################################################

import time
import serial as sr
from matplotlib import pyplot as plt
import numpy as np
# plt.style.use('ggplot')               # Select your favourite plot style. or don't
SERIAL_PORT = '/dev/ttyACM0'            # Enter Serial port name
s = sr.Serial(SERIAL_PORT, 9600)


def graph_live_blit(blit=False):
    """
    If blit is true, uses bliting to generate graphs faster. Otherwise generate traditional live plot
    :param blit: Boolean. True if bliting is desired
    :return: Draws matplotlib graphs in figure window
    """
    SIZE = 300                          # Number of data points to show in graph
    x = np.linspace(0, 1, SIZE+1)[0:-1]
    y_vec = np.zeros(len(x))
    fig = plt.figure()
    ax2 = fig.add_subplot(1, 1, 1)
    line, = ax2.plot([], lw=3)
    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim([0, 40])               # Set ylims here. blit graph cannot change limits
    fig.canvas.draw()                   # Draw the first graph even without data
    if blit:
        # cache the background
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)
    plt.show(block=False)
    t_start = time.time()
    while True:

        a = s.readline()
        a.decode()
        if a == b'\r\n' or a == b'\n':               # To handle null values received without dying
            continue
        # print('a = ', a);
        b = float(a[0:4])                            # Each data point is suffixed by \r\n and other stuff. ignore
        y_vec[-1] = b
        y_vec = np.append(y_vec[1:], 0.0)
        print(x)
        line.set_data(x, y_vec)                     # Only update new y data on graph
        # print tx
        if blit:
            fig.canvas.restore_region(ax2background)    # restore background
            ax2.draw_artist(line)                   # redraw just the points, not entire graph
            fig.canvas.blit(ax2.bbox)               # fill in the axes rectangle
        else:
            # redraw everything
            fig.canvas.draw()
        fig.canvas.flush_events()
    t_end = time.time()
    print("Time Elapsed: ", t_end-t_start)


graph_live_blit(True)

s.close()       # Close the serial port like an upstanding citizen
