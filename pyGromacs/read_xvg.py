import sys

try:
    import pandas
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print('\t{0}'.format(e))
    sys.exit(1)
    
class xvgData:
    
    def __init__(self, data, label, meta, legend, plotType):
        self.data = data
        self.label = label
        self.meta = meta
        self.legend = legend
        self.plotType = plotType

    def plot(self, xlab = None, ylab = None, title = None, legend = None, average=False, averageScale=20):
        if title == None :
            title = self.label['title']
        if xlab == None :
            xlab = self.label['xlab']
        if ylab == None :
            ylab = self.label['ylab']
        if legend == None :
            legend = self.data.iloc[:,1:].columns
        if self.plotType == 'xy':
            if average == True:
                averageTimeStep = averageScale * (self.data.iloc[1,0]- self.data.iloc[0,0])
            for ycol in self.legend :
                if not ycol == "x": 
                    plt.plot(self.data.iloc[:,0], self.data[ycol], label = ycol)
                    if average == True:
                        plt.plot(self.data.iloc[:,0], self.data[ycol].rolling(window=averageScale).mean(), label = ycol + " (average " + str(averageTimeStep) + ")" )
            plt.legend()
        if self.plotType == 'xydy':
            plt.errorbar(self.data.iloc[:,0], self.data.iloc[:,1], yerr = self.data.iloc[:,2], capsize=5)    
        plt.title(title)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.show()
        
    def get_pandas(self):
        return self.data
    
    def to_csv(self, filename, sep=",", dec="."):
        self.data.to_csv(filename, sep=sep, decimal=dec, index=False)
        

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
    return xvgData(dataset, label, meta, legend, plotType)
