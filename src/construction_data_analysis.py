#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:21:21 2020

@author: yating
"""

import sys
import matplotlib.pyplot as plt
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
test_num=3
data_num=25
for test_index in range(1, test_num):
    data = []
    for data_index in range(1, data_num):
        a_path = os.path.join(path, "test"+str(test_index)+"/data"+str(data_index)+"/block0.csv")
        with open (a_path,'r') as csvfile:
            reader = csv.reader(csvfile) 
            lines = [line for line in reader]
            data.append(len(lines))
    Data[str(test_index)] = data
    
df = pd.DataFrame(data)
df.plot.box(title="Consumer spending in each country")
plt.grid(linestyle="--", alpha=0.3)
plt.show()

import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame(data)
#df.plot.box(title="hua tu")
plt.grid(linestyle="--", alpha=0.3)
plt.show()

plt.legend()
plt.grid()



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
data = [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100]
 
df = pd.DataFrame(data)
df.plot.box(title="hua tu")
plt.grid(linestyle="--", alpha=0.3)
plt.show()