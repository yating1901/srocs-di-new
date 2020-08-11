import tables
import pandas

dataset = pandas.read_hdf('dcp.hdf', 'table')

# TODO
# figure whether an experiment finished sucessfully automatically
# add code to plot trajectories
# for the successful cases, calculate standard dev, median etc of runtime


