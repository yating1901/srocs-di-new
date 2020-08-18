import xml.etree.ElementTree
import tempfile
import threading
import subprocess
import tables
import pandas
import os
from copy import deepcopy
from time import sleep
import re

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
      # create an output directory
      self.output_dir = tempfile.TemporaryDirectory()
      # set the output dir
      self.config.find('./loop_functions').attrib['output_directory'] = self.output_dir.name
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
      Data = []
      for dir_entry in os.listdir(self.output_dir.name):
         if dir_entry.endswith(".csv"):
            output_file = os.path.join(self.output_dir.name, dir_entry)
            data = pandas.read_csv(output_file, header = None)
            object_id = os.path.basename(os.path.splitext(output_file)[0])
            o_id = re.findall(r"\d+\.?\d*", object_id)[0]
            if not(object_id.find('freeblock')):
                #print(o_id)
                #data.drop([4],axis=1,inplace=True)
                data.insert(4,4, self.seed)
                data.insert(5,5, o_id)
                data.columns=['STEP','X','Y','Z','SEED','ID']
                Data.append(data)
      # acquire the lock
      with self.dataset['lock']:
         self.dataset['data'] = self.dataset['data'].append(Data)
         self.dataset['jobs'] -= 1
         # if we were the last job
         if self.dataset['jobs'] == 0:
            with terminal_lock:
               print('writing Data to %s.hdf' % self.dataset['name'])
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
            print('  output directory: %s' % active_jobs[thread].output_dir.name)
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
                  #print('  output directory: %s' % active_jobs[thread].output_dir.name)
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
config = xml.etree.ElementTree.parse('@CMAKE_BINARY_DIR@/experiment/dcp_template.argos').getroot()
framework = config.find('./framework')
experiment = framework.find('./experiment')
visualization = config.find('./visualization')
loop_functions = config.find('./loop_functions')

# experiment parameters
# TODO set maximum experiment length here
experiment.attrib['length'] = '60000'

# remove the qtopengl visualization
if visualization.find('./qt-opengl') is not None:
   visualization.remove(visualization.find('./qt-opengl'))

dataset = create_dataset('dcp')
for run in range(0,25):
   seed = run + 1
   desc = 'no description'
   job = ARGoSJob(desc, config, seed, dataset)
   jobs.append(job)
           

# execute all jobs (second number should be how many CPUs you want to use)
run_argos_jobs(jobs, 2)
