import tables
import pandas
import numpy 
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
dataset1 = pandas.read_hdf('dcp.hdf', 'table')
#dataset2 = pandas.read_hdf('dcp.hdf', 'table')
#dataset3 = pandas.read_hdf('dcp_four_builderbots.hdf', 'table')

def draw_trajectory(dataset, SEED):
    Set = dataset[dataset["SEED"] == SEED]
    freeblock = ['00','01','10','11','20','21','30','31']
    for block_index in range(0, len(freeblock)):
        datum = []
        datum = Set[Set['ID']==freeblock[block_index]][['X','Y','Z']]
        datum = datum.values
        x_data = []
        y_data = []
        for xy_index in range(0,len(datum)):
            x_data.append(datum[xy_index][0])
            y_data.append(datum[xy_index][1])
        plt.title('Dynamic Construction paths(two builderbot)')
        plt.plot(x_data, y_data, label='freeblock'+freeblock[block_index])
        #plt.legend()
    plt.xlabel('X axes')
    plt.ylabel('Y axes')
    plt.savefig('Arena.png',bbox_inches = 'tight')
    plt.show()

def Is_ended_automatically(dataset,SEED,steps):
    #print("total steps:", steps)
    #print("seed:",SEED)
    Is_Ended = False
    Set = dataset[dataset["SEED"] == SEED] 
    freeblock = ['00','01','10','11','20','21','30','31']
    num = 0
    for block_index in range(0, len(freeblock)):
        datum = []
        datum = Set[Set['ID']==freeblock[block_index]][['X','Y','Z']]
        datum = datum.values
        #print(len(datum))
        x = datum[steps-1][0]
        y = datum[steps-1][1]
        z = datum[steps-1][2]
        #print(x,y,z)
        if (round(z,3) == 0.055):
            num = num +1
        if num == 2:
            Is_Ended = True
    #print( "Is_ended_automatically:", Is_Ended)
    return Is_Ended

def box_plot(steps):
    #print(steps)
    Data={}
    Data['One Builderbots'] = steps
    df = pandas.DataFrame(Data)
    def formatnum(x, pos):
        return '$%d$$k$' % (x/1000)
    formatter = FuncFormatter(formatnum)
    df.plot.box(title="Dynamic construction paths ")
    plt.grid(linestyle="--", alpha=0.5)
    
    #label
    plt.ylabel('Number of Steps')
    plt.xlabel('Number of BuilderBots')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('Dcps_One_Builderbots.png',bbox_inches = 'tight')
    plt.show()


def calculate_length(Data):
    freeblock_id = '00'
    freeblock_data = Data[Data["ID"] == freeblock_id]
    step = numpy.array(freeblock_data.iloc[-1:]["STEP"])[0]   
    return step



Max_seed = 25
data=[]
steps = []
freeblock = ['00','01','10','11','20','21','30','31']
for seed in range(1,Max_seed+1):
    data.append(dataset1[dataset1["SEED"] == seed])
    steps.append(int(len(data[seed-1])/len(freeblock)))
    #steps.append(calculate_length(data[seed-1]))
    
    
box_plot(steps)
#draw_trajectory(dataset3,9)


Is_all_ended = True
for seed in range(1, Max_seed+1):
    print("seed:", seed,"steps:",steps[seed-1])
    Is_ended = Is_ended_automatically(dataset1,seed,steps[seed-1])
    Is_all_ended = Is_all_ended and Is_ended
    
print("Is_All_Ended:", Is_all_ended)
