import sys


try:
    import pandas
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print('\t{0}'.format(e))
    sys.exit(1)

def math_exp(text):
    if "\\xl\\f{}" in text:
        text = text.replace("\\xl\\f{}", "$\\lambda$")
    if "\\xD\\f{}" in text:
        text = text.replace("\\xD\\f{}", "$\\Delta$")
    return text

def read_xvg(filename, save_metadata = True) :
    label = dict()
    data = []
    meta = []
    legend = ["x"]
    with open(filename) as f:
        lineList = f.readlines()
        for line in lineList :
            if line.startswith("@") :
                if "title" in line :
                    title = line.split("title")[1].replace('\"','').strip()
                    label['title'] = title
                if "xaxis" in line :
                    xlab = line.split("label")[1].replace('\"','').strip()
                    label['xlab'] = math_exp(xlab)
                if "yaxis" in line :
                    ylab = line.split("label")[1].replace('\"','').strip()
                    label['ylab'] = math_exp(ylab)
                if "@ s" in line : 
                    y_legend = line.split("legend")[1].replace('\"','').strip()
                    legend.append(y_legend)
                if "TYPE" in line :
                    plotType = line.split(" ")[1].replace('\"','').strip()
                    
            elif line.startswith("#"):
                if save_metadata == True: 
                    meta.append(line.strip())
            else :
                line = line.strip()
                splitRowData =  list(filter(None, line.split(" ")))
                data.append(splitRowData)
    if plotType == "xydy" :
        legend = legend + ["y", "dy"]
    dataset = pandas.DataFrame(data, columns=legend, dtype='float64')
    return({'data' : dataset, 'label' : label, 'meta' : meta, 'legend' : legend, "plotType" : plotType})

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

