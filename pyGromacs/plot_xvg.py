import sys

try:
    import pandas
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print('\t{0}'.format(e))
    sys.exit(1)

def plot_xvg(xvgdata, xlab = None, ylab = None, title = None, legend = None, average=False, averageScale=20):
    if title == None :
        title = xvgdata['label']['title']
    if xlab == None :
        xlab = xvgdata['label']['xlab']
    if ylab == None :
        ylab = xvgdata['label']['ylab']
    if legend == None :
        legend = xvgdata['data'].iloc[:,1:].columns
    if xvgdata['plotType'] == 'xy':
        if average == True:
            averageTimeStep = averageScale * (xvgdata['data'].iloc[1,0]- xvgdata['data'].iloc[0,0])
        for ycol in xvgdata['legend']:
            if not ycol == "x": 
                plt.plot(xvgdata['data'].iloc[:,0], xvgdata['data'][ycol], label = ycol)
                if average == True:
                    plt.plot(xvgdata['data'].iloc[:,0], xvgdata['data'][ycol].rolling(window=20).mean(), label = ycol + " (average " + str(averageTimeStep) + ")" )
        plt.legend()
    if xvgdata['plotType'] == 'xydy':
        plt.errorbar(xvgdata['data'].iloc[:,0], xvgdata['data'].iloc[:,1], yerr = xvgdata['data'].iloc[:,2], capsize=5)    
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()  
