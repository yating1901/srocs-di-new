import tables
import pandas
import numpy 
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
dataset = pandas.read_hdf('dcp.hdf', 'table')
# TODO
# figure whether an experiment finished sucessfully automatically
# add code to plot trajectories
# for the successful cases, calculate standard dev, median etc of runtime
#fix_blocks_id = ['0','1','2','3','4','5','6','7','8']
#free_blocs_id = ['00','01','11','12','21','22','31','32']


def draw_trajectory(dataset, SEED):
    Set = dataset[dataset["SEED"] == SEED]
    freeblock = ['00','01','11','12','21','22','31','32']
    for block_index in range(0, len(freeblock)):
        print(block_index)
        datum = []
        datum = Set[Set['ID']==freeblock[block_index]][['X','Y','Z']]
        datum = datum.values
        x_data = []
        y_data = []
        for xy_index in range(0,len(datum)):
            x_data.append(datum[xy_index][0])
            y_data.append(datum[xy_index][1])
        plt.title('Data1 in test1 (two builderbot)')
        plt.plot(x_data, y_data, label='freeblock'+freeblock[block_index])
        #plt.legend()
    plt.xlabel('X axes')
    plt.ylabel('Y axes')
    plt.savefig('Arena.png',bbox_inches = 'tight')
    plt.show()




def box_plot(steps):
    print(steps)
    Data={}
    Data['two builderbot'] = steps
    df = pandas.DataFrame(Data)
    #def formatnum(x, pos):
    #return '$%d$$k$' % (x/1000)
    #formatter = FuncFormatter(formatnum)
    df.plot.box(title="Dynamic construction paths ")
    plt.grid(linestyle="--", alpha=0.5)
    
    #label
    plt.ylabel('Number of steps')
    plt.xlabel('Number of BuilderBots')
#    plt.gca().yaxis.set_major_formatter(formatter)
#    plt.savefig('Dcps.png',bbox_inches = 'tight')
    plt.show()


def calculate_length(Data):
    freeblock_id = '00'
    freeblock_data = Data[Data["ID"] == freeblock_id]
    step = numpy.array(freeblock_data.iloc[-1:]["STEP"])[0]   
    return step



Max_seed = 10
data=[]
steps = []
for seed in range(1,Max_seed+1):
    data.append(dataset[dataset["SEED"] == seed])
    steps.append(calculate_length(data[seed-1]))
    
steps[3] = 100
steps[4] = 0
box_plot(steps)
draw_trajectory(dataset,1)
