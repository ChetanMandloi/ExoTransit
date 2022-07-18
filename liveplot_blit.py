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
from scipy.signal import savgol_filter
from scipy.ndimage.filters import gaussian_filter1d
import pandas as pd
import numpy as np

# plt.style.use('ggplot')               # Select your favourite plot style. or don't
SERIAL_PORT = '/dev/ttyACM0'            # Enter Serial port name
CALIB_TIME = 0.1                         # Wait CALIB seconds to figure out y-axis lims to use for graph


def calibrate_lims(s_port, calib_time=5):
    """
    returns upper and lower Y axis lims for graphs after 5 seconds of data
    :param s_port: serial port that gives data
    :param calib_time: time allocated for calib in seconds
    :return: list containing [Y_lower_limit, Y_upper_limit]
    """
    time_elapsed = 0
    time_start = time.time()
    y_max = 8.5
    y_min = 4

    while time_elapsed <= calib_time:
        curr_time = time.time()
        time_elapsed = curr_time - time_start
        a = s_port.readline()
        try:
            a.decode()
        except UnicodeDecodeError:
            continue
        if a == b'\r\n' or a == b'\n':               # To handle null values received without dying
            continue
        # print('a = ', a);

        b = float(a[0:6])

        y_max = max(b, y_max)
        y_min = min(b, y_min)
    return [4, 8.5]


def graph_live_blit(s_port, blit=False):
    """
    If blit is true, uses bliting to generate graphs faster; otherwise generate traditional live plot
    :param blit: Boolean. True if bliting is desired
    :param s_port: serial port that gives data
    :return: Draws matplotlib graphs in figure window
    """
    graph_y_lims = calibrate_lims(s_port, CALIB_TIME)   # Wait CALIB seconds to figure out y-axis lims to use for graph
    export_df = pd.DataFrame(columns=['flux', 'unix_time'])     # For storing data with time and exporting at the end
    x_size = 300                 #single 300  multiple 1000       # Number of data points to show in graph
    x = np.linspace(0, 1, x_size+1)[0:-1]
    y_vec = np.zeros(len(x))
    fig = plt.figure()
    ax2 = fig.add_subplot(1, 1, 1)
    fig.set_figwidth(12)
    ax2.minorticks_on()
    ax2.grid(which='major', axis='y', color='green', linestyle='-', linewidth=0.5)
    ax2.grid(which='minor', axis='y', color='green', linestyle='--', linewidth=0.25)
    line, = ax2.plot([], lw=1)
    ax2.set_xlim(x.min(), x.max()-2/x_size)     # reducing x-limits by 2 data points because of leading zeros issue
    ax2.set_ylim(graph_y_lims)          # Set y-limits here. blit graph cannot change limits dynamically
    fig.canvas.draw()                   # Draw the first graph even without data
    if blit:
        # cache the background
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)
    plt.show(block=False)
    t_start = time.time()
    while True:
        try:
            a = s_port.readline()
            a.decode()
            if a == b'\r\n' or a == b'\n':               # To handle null values received without dying
                continue
            # print('a = ', a);
            b = float(a[0:6])                            # Each data point is suffixed by \r\n and other stuff. ignore
            print("a:", a, "b:", b)
            y_vec[-1] = b
            y_vec = np.append(y_vec[1:], 0.0)
            y_vec[-10:] = gaussian_filter1d(y_vec[-10:], sigma=1)
            #y_vec[-10:] = savgol_filter(y_vec[-10:], 3, 1, mode='nearest')

            new_row = pd.DataFrame([{'flux': b, 'unix_time': time.time()}])
            export_df = pd.concat([export_df, new_row], ignore_index=True)
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
        except KeyboardInterrupt:
            print(export_df.describe())
            t_end = time.time()
            print("Press CTRL-C to terminate statement")
            print("Time Elapsed: ", t_end - t_start)
            export_df.to_csv("data.csv")
            break


s = sr.Serial(SERIAL_PORT, 9600)
graph_live_blit(s, True)

s.close()       # Close the serial port like a good upstanding citizen
