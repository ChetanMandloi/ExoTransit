#
#  liveplot to plot data as it comes along
#
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')     # use ggplot style because it looks better

def live_plot(x_time,y_lux,line1,identifier='',pause_time=0.001):
    if line1==[]: # first time plot with empty data
        plt.ion()
        fig = plt.figure(figsize=(15,7))
        ax = fig.add_subplot(111)
        # live plot is just starting, so create a variable so we can keep updating it to plot
        line1, = ax.plot(x_time,y_lux,'b-o',alpha=0.8)        
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # Be lazy and efficient. instead of replotting whole dataset, only update y data.
    line1.set_ydata(y_lux)
    # move plot axis limits if new data goes beyond bounds
    if np.min(y_lux)<=line1.axes.get_ylim()[0] or np.max(y_lux)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y_lux)-np.std(y_lux),np.max(y_lux)+np.std(y_lux)])
    # pause the data so the figure/axis can catch up
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1


# New and Improved! Actually same as above but for updating both axis instead of only Y.
def live_plotter_xy(x_time,y_lux,line1,identifier='',pause_time=0.001):
    if line1==[]:
        plt.ion()
        fig = plt.figure(figsize=(15,7))
        ax = fig.add_subplot(111)
        line1, = ax.plot(x_time,y_lux,'r-o',alpha=0.8)
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
        
    line1.set_data(x_time,y_lux)
    plt.xlim(np.min(x_time),np.max(x_time))  # X and Y lim should be same as before
    if np.min(y_lux)<=line1.axes.get_ylim()[0] or np.max(y_lux)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y_lux)-np.std(y_lux),np.max(y_lux)+np.std(y_lux)])

    plt.pause(pause_time)
    
    return line1

