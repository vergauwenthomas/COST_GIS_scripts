#!/bin/bash


#This script set the environment variables for the main.py

# ------------ Settings ---------------

#Note: because bash can not (yet) export arrays, list the buffer radii as a string seperated by comma.

export COST_BUFFER_RADII="20,50,100,250,500"



# ------------ output -----------------

export COST_OUTPUT_FOLDER="/home/thoverga/Documents/github/COST_GIS_scripts/testcases/Novi_Sad_stations/output"

# ------------ input -----------------

#option 1: by csv file

#export COST_INPUT_FILE="/home/thoverga/Documents/github/COST_GIS_scripts/testcases/Novi_Sad_stations/station_data_NS.csv"
#export COST_LAT_IDENTIFIER="station_lat" #name of latitude column in the csv file
#export COST_LON_IDENTIFIER="station_long" #name of longitude column in the csv file
#export COST_STATION_IDENTIFIER="station_name" #name of column containing the unique station names


#option 2 by JSON file (Preferable):
export  COST_INPUT_FILE="/home/thoverga/Documents/github/COST_GIS_scripts/input_coordinates.json"



# -------------Logging ---------------------

export COST_LOG_FILE="/home/thoverga/Documents/github/COST_GIS_scripts/logfile.log"
