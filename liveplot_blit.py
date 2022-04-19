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
CALIB_TIME = 10                         # Wait CALIB seconds to figure out y axis lims to use for graph


def calibrate_lims(s_port, calib_time=5):
    """
    returns upper and lower Y axis lims for graphs after 5 seconds of data
    :param s_port: serial port that gives data
    :param calib_time: time allocated for calib in seconds
    :return: list containing [Y_lower_limit, Y_upper_limit]
    """
    time_elapsed = 0
    time_start = time.time()
    y_max = 30
    y_min = 20
    while time_elapsed <= calib_time:
        curr_time = time.time()
        time_elapsed = curr_time - time_start
        a = s_port.readline()
        a.decode()
        if a == b'\r\n' or a == b'\n':               # To handle null values received without dying
            continue
        # print('a = ', a);
        b = float(a[0:4])
        y_max = max(b, y_max)
        y_min = min(b, y_min)
    return [y_min*0.8, y_max*1.3]


def graph_live_blit(s_port, blit=False):
    """
    If blit is true, uses bliting to generate graphs faster. Otherwise generate traditional live plot
    :param blit: Boolean. True if bliting is desired
    :param s_port: serial port that gives data
    :return: Draws matplotlib graphs in figure window
    """
    graph_y_lims = calibrate_lims(s_port, CALIB_TIME)   # Wait CALIB seconds to figure out y axis lims to use for graph
    x_size = 300                          # Number of data points to show in graph
    x = np.linspace(0, 1, x_size+1)[0:-1]
    y_vec = np.zeros(len(x))
    fig = plt.figure()
    ax2 = fig.add_subplot(1, 1, 1)
    line, = ax2.plot([], lw=3)
    ax2.set_xlim(x.min(), x.max()-2/x_size)
    ax2.set_ylim(graph_y_lims)          # Set ylims here. blit graph cannot change limits dynamically
    fig.canvas.draw()                   # Draw the first graph even without data
    if blit:
        # cache the background
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)
    plt.show(block=False)
    t_start = time.time()
    while True:

        a = s_port.readline()
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


s = sr.Serial(SERIAL_PORT, 9600)
graph_live_blit(s, True)

s.close()       # Close the serial port like a good upstanding citizen
