#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:03:35 2020

@author: yating
"""

import os
import sys

#testfolder = sys.argv[1]
#print("testfolder = " + testfolder)

def generate_argos_file(i, len):
	#read in the file
	with open('experiment/template.argos', 'r') as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('RANDOM_SEED', str(i))
	filedata = filedata.replace('TEST_LENGTH', str(len))

	# Write the file out again
	with open('experiment/srocs.argos', 'w') as file:
		file.write(filedata)



#os.system("mkdir data/" + testfolder + "/random")
len = 100000
test_number = 5
#make -C ../&& argos3 -c srocs.argos 
#for i in range(83, 84):
for i in range(1, test_number + 1):
	print("running test" + str(i))
	generate_argos_file(i, len)
	os.system("make && argos3 -c experiment/srocs.argos")
	#os.system("argos3 -c data/" + testfolder + "/vns_test.argos")
	#os.system("./data/" + testfolder + "/error_calculator/build/main " + str(len) + " ./")
	os.system("mkdir data" + str(i))
	os.system("cp -f *.csv data" + str(i))
	#os.system("mv result.txt data/" + testfolder + "/random/run" + str(i))
	#os.system("mv srocs.argos data" + str(i))