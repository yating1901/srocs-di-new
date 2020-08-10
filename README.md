## Guidelines
1. Install argos3 and argos3-srocs (make sure you install with the updatest version)
2. Change line 9 of CMakeLists.txt to your argos3-srocs folder position
3. Steps for making:
   `mkdir build`
   
   `cd build`
   
   `cmake ../src`
   
    `make`
    
4. If you want to run .argos file, using command: argos3 -c filename.argos 
5. If you want to run the simulations, run my_generation_data.py by using command: 

   `python my_generation_data.py`
   This python script will help run the argos file and save the output .csv files into different sub folder,as well as compress all the data into hdf5.
6. To deal with hdf5, you have to install package h5py by using command:

    `pip install h5py`
