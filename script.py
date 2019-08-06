try:
    import pandas
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print('[!] The required Python libraries could not be imported:', file=sys.stderr)
    print('\t{0}'.format(e))
    sys.exit(1)


def read_xvg(filename) :
    label = []
    data = []
    with open(filename) as f:
        lineList = f.readlines()
        for line in lineList :
            if line.startswith("@") :
                if "title" in line :
                    title = line.split("title")[1].replace('\"','').strip()
                    label.insert(0, title )
                if "xaxis" in line :
                    xlab = line.split("label")[1].replace('\"','').strip()
                    label.insert(1, xlab )
                if "yaxis" in line :
                    ylab = line.split("label")[1].replace('\"','').strip()
                    label.insert(2, ylab)
            else :
                if not line.startswith("#"):
                    line = line.strip()
                    splitRowData =  list(filter(None, line.split(" ")))
                    data.append(splitRowData)
    dataset = pandas.DataFrame(data, columns=label[1:], dtype='float64')
    return([dataset, label])
 
 def plot_xvg(xvgdata, xlab = None, ylab = None, title = None):
    if title == None :
        title = xvgdata[1][0]
    if xlab == None :
        xlab = xvgdata[1][1]
    if ylab == None :
        ylab = xvgdata[1][2]
    plt.plot(xvgdata[0].iloc[:,0], xvgdata[0].iloc[:,1])
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.show()
    
    
