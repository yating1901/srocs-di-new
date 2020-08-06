#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:21:21 2020

@author: yating
"""

import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import numpy as np
import pandas as pd
test_index=1
data_index=1
lines = []
Data = {}
path = os.getcwd()
#print(a_path)
test_num=4
data_num=25
for test_index in range(1, test_num+1):
    if test_index == 3:
            continue
    data = []
    for data_index in range(1, data_num+1):
        a_path = os.path.join(path, "test"+str(test_index)+"/data"+str(data_index)+"/block0.csv")
        with open (a_path,'r') as csvfile:
            reader = csv.reader(csvfile) 
            lines = [line for line in reader]
            data.append(len(lines))
    Data[str(test_index)] = data

df = pd.DataFrame(Data)

def formatnum(x, pos):
    return '$%d$$k$' % (x/1000)
formatter = FuncFormatter(formatnum)
#ax.yaxis.set_major_formatter(formatter)

df.plot.box(title="Dynamic construction paths ")
plt.grid(linestyle="--", alpha=0.5)

#label
plt.ylabel('Number of steps')
plt.xlabel('Number of BuilderBots')
plt.gca().yaxis.set_major_formatter(formatter)
plt.savefig('Dcps.png',bbox_inches = 'tight')
plt.show()

