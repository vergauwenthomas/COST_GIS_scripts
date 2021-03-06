# COST_GIS_scripts
Scripts to extract geospatial information for a given coordinate. The output is visualised in an overview figure and a tabular .csv file. 

Output overview figure example
![Alt text](examples/station1_overview.svg?raw=true "Title")

Output tabular data example:
![Alt text](examples/tabular_data.csv?raw=true "Title")
![Alt text](examples/tabular_data_example.png?raw=true "Title")

# Installation
All packages and the used python version are stored in a conda environment. To install this environment execute `conda env create -f environment.yml`.

# Required software and running
To run :
* Check if the paths are correct in the `set_env_variables.sh`.
* Activate conda environment: `conda activate cost_scripts_env`. (Make sure the environment is installed.) 
* Then execute `source set_env_variables` and (in the same shell) `./main.py`.
* To read the log files: `tail logfile.log`.


# Required Geo maps
For all these maps only the .tif file is required.

* S2glc map (7.8G): [website](https://s2glc.cbk.waw.pl/) and [download link](http://users.cbk.waw.pl/~mkrupinski/S2GLC_Europe_2017_v1.2_grey.zip)
* DEM map (4G per dataset) a login is required to download the maps, but you are free to register: [website](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1) and [download link](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1?tab=download)
* LCZ map (150 Mb): [website](https://www.wudapt.org/) and [download link](https://figshare.com/articles/dataset/European_LCZ_map/13322450) 


# Contributors
Thomas Vergauwen - Royal Meteorolgical Instituut (RMI) Belgium - thomas.vergauwen@meteo.be

Sara Top - Ghent University - sara.top@ugent.be

Steven Caluwaerts - Royal Meteorolgical Instituut (RMI) Belgium / Ghent University - steven.caluwaerts@ugent.be
