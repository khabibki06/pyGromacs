# pyGromacs

these are some useful script for Gromacs preparation and simulation

## pyXVG
this script for read and plot xvg file
how to use :
1. read_xvg to read xvg file
cluster = read_xvg("filename.xvg")
by default, this function stores the metadata infomation. it can be disabled by set save_metadata = False

the output variable is a dictionary containing three keys:
1. data = a dataframe of numeric data
2. label = the label infomation about title, xlab, ylab, plot type
3. meta = metadata

2. plot_xvg 
this function is used to plot the output of read_xvg
example: plot_xvg(cluster)
by default, it will be used xlab, title, and other informations from the output read_xvg. It can be adjut manually using xlab, ylab, title setting
example : plot_xvg(cluster, ylab = "number of molecules")
