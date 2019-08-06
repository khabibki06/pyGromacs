import sys


try:
    import pandas
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print('\t{0}'.format(e))
    sys.exit(1)

def math_exp(text):
    output = []
    txt_split = text.split(" ")
    for string in txt_split:
        stringmath = "$" + string + "$"
        output.append(stringmath)
    return(" ".join(output))

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
            elif line.startswith("#"):
                if save_metadata == True: 
                    meta.append(line.strip())
            else :
                line = line.strip()
                splitRowData =  list(filter(None, line.split(" ")))
                data.append(splitRowData)
    dataset = pandas.DataFrame(data, columns=legend, dtype='float64')
    return({'data' : dataset, 'label' : label, 'meta' : meta})

def plot_xvg(xvgdata, xlab = None, ylab = None, title = None, legend = None):
    if title == None :
        title = xvgdata['label']['title']
    if xlab == None :
        xlab = xvgdata['label']['xlab']
    if ylab == None :
        ylab = xvgdata['label']['ylab']
    if legend == None :
        legend = xvgdata['data'].iloc[:,1:].columns
    plt.plot(xvgdata['data'].iloc[:,0], xvgdata['data'].iloc[:,1:])
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.gca().legend(legend)
    plt.show()  
