## Guidelines
1. This project requires the latest versions of argos3 and argos3-srocs to be installed
2. To build this repository, run:
```bash
mkdir build
cd build
cmake ../src
make
```
3. All files in the src directory are copied and configured automatically to the build directory when running `cmake` and `make` above. There is no need to manually specify any paths.
4. The project can be run manually with `argos3 -c path/to/build/experiment/dcp_template.argos`. In manual mode, robot activity is recorded in CSV files which are written to a directory specified by the loop function attribute `output_directory`. If this attribute is not provided, the CSV files are stored in the folder from which you started ARGoS. 
5. The project can also be run automatically (sweeping accross different seeds) with `python path/to/build/experiment/dcp_generate_data.py`. This script will output the CSV reports from different instances of ARGoS (running concurrently) into temporary directories and will parse the results at the end of each simulation run. The output of this script is a file `dcp.hdf` which is a HDF5 table. This table can be loaded into python with the following commands.
```python
import tables
import pandas

dataset = pandas.read_hdf('dcp.hdf', 'table')
```
