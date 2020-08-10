#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 09:52:21 2020

@author: yating
"""

import xml.etree.ElementTree
import tempfile
import threading
import subprocess
import tables
import pandas
import glob
import os
import sys
import csv
from copy import deepcopy
from time import sleep

# create a lock for writing to the terminal
terminal_lock = threading.Lock()

# define an ARGoS job (subclass of Thread)
class ARGoSJob(threading.Thread):
   def __init__(self, desc, config, seed, dataset):
      self.desc = desc
      self.config = deepcopy(config)
      self.seed = seed
      self.dataset = dataset
      with self.dataset['lock']:
         self.dataset['jobs'] += 1
      # create an output file
      #self.output_file = tempfile.NamedTemporaryFile(mode='r', suffix='.csv', delete=False)
      # set the output file
      #self.config.find('./loop_functions').attrib['output'] = self.output_file.name
      # set the seed
      self.config.find('./framework/experiment').attrib['random_seed'] = str(self.seed)
      # create the configuration file
      self.config_file = tempfile.NamedTemporaryFile(mode='w+b', suffix='.argos', delete=False)
      self.config_file.write(xml.etree.ElementTree.tostring(self.config))
      self.config_file.flush()
      # call the super class constructor
      super().__init__()
      
   def run(self):
      subprocess.run(['argos3', '-c', self.config_file.name], capture_output=True)
      #import pandas
      #import glob
      #import os
      #import csv
      #import subprocess
      path = os.getcwd()
      file = glob.glob(os.path.join(path, "*.csv"))
      data = []
      for file_index in file:
          with open(file_index,'r') as f:
              data.append(csv.reader(f))
      #data.insert(0, self.seed)
      os.system("mkdir data" + str(self.seed))
      os.system("cp -f *.csv data" + str(self.seed))
      # acquire the lock
      with self.dataset['lock']:
         self.dataset['data'] = self.dataset['data'].append(data)
         self.dataset['jobs'] -= 1
         # if we were the last job
         if self.dataset['jobs'] == 0:
            with terminal_lock:
               print('writing data to %s.hdf' % self.dataset['name'])
            self.dataset['data'].to_hdf('%s.hdf' % self.dataset['name'], 'table', append=False)

# run the argos jobs in parallel
def run_argos_jobs(jobs, threads):
   total_jobs = len(jobs)
   current_job = 0
   active_jobs = {}
   for thread in range(0, threads):
      if jobs:
         active_jobs[thread] = jobs.pop()
         current_job += 1
         with terminal_lock:
            print('starting job (%d/%d): %s (seed = %d)' % (current_job, total_jobs, active_jobs[thread].desc, active_jobs[thread].seed)) 
            print('  command: argos3 -c %s' % active_jobs[thread].config_file.name)
         active_jobs[thread].start()
         sleep(0.1)
   while active_jobs:
      for thread, active_job in active_jobs.items():
         if active_job.is_alive():
            continue
         else:
            if jobs:
               active_jobs[thread] = jobs.pop()
               current_job += 1
               with terminal_lock:
                  print('starting job (%d/%d): %s (seed = %d)' % (current_job, total_jobs, active_jobs[thread].desc, active_jobs[thread].seed))
                  print('  command: argos3 -c %s' % active_jobs[thread].config_file.name)
                  #print('  output file: %s' % active_jobs[thread].output_file.name)
               active_jobs[thread].start()
               sleep(0.1)
            else:
               active_jobs.pop(thread)
               break;

# create a new dataset
def create_dataset(name):
   return {
      'name': name,
      'lock': threading.Lock(),
      'data': pandas.DataFrame(),
      'jobs': 0,
   }


# list of jobs for ARGoS
jobs = []

# open the template configuration file
config = xml.etree.ElementTree.parse('template.argos').getroot()
framework = config.find('./framework')
experiment = framework.find('./experiment')
visualization = config.find('./visualization')
loop_functions = config.find('./loop_functions')
parameters = loop_functions.find('./condition')
experiment.attrib['length'] = '0'

# remove the qtopengl visualization
if visualization.find('./qt-opengl') is not None:
   visualization.remove(visualization.find('./qt-opengl'))
   
#len = 20000
test_number = 2

#dataset = create_dataset('mfdi%s_cl%s_cf%s_td%s' % (mean_foraging_duration_initial, construction_limit, confidence, target_density))
dataset = create_dataset('Data')
for run in range(1, test_number + 1):
    experiment.attrib['random_seed'] = str(run)
    seed = run
    desc = ('[length: %s]' % (experiment.attrib['length']))
    job = ARGoSJob(desc, config, seed, dataset)
    jobs.append(job)
           

# execute all jobs
run_argos_jobs(jobs, test_number)