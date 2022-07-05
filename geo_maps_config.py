#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Config file for the geospatial raster files.

@author: Thomas vergauwen
"""
from os.path import exists, isdir
import logging
#%% SET PATHS
logging.info("Loading module geo_maps_config.py")
#paths to the raster files (.tif)

s2glc_path = "/home/thoverga/Documents/github/maps/Landuse/S2GLC_EUROPE_2017/S2GLC_Europe_2017_v1.2.tif"
lcz_path = "/home/thoverga/Documents/github/maps/Landuse/EU_LCZ_map.tif"
dem_dir_path = "/home/thoverga/Documents/github/maps/DEM" #all files with .tif extension in the directory will be used. 

#check if paths exists
if exists(s2glc_path):
    logging.info('S2glc file exists: %s', s2glc_path)
else:
    logging.critical('S2glc file ( %s ) not found! ', s2glc_path)

if exists(lcz_path):
    logging.info('lcz-map file exists: %s', lcz_path)
else:
    logging.critical('lcz-map file ( %s ) not found! ', lcz_path)

if isdir(dem_dir_path):
    logging.info('DEM folder exists: %s', dem_dir_path)
else:
    logging.critical('DEM folder ( %s ) not found! ', dem_dir_path)

#%% S2GLC_EUROPE_2017 Landcover map
s2glc_settings = {
    'file': s2glc_path,
    'source_text': 'S2GLC-2017 V1.2 product (https://s2glc.cbk.waw.pl/)',
    'data_band': 1,
    'classes': {
        0: {'color': '#FFFFFF', 'name': 'clouds'},
        62: {'color': '#D20000', 'name': 'Artificial surfaces and constructions'},
        73: {'color': '#FDD327', 'name': 'Cultivated areas'},
        75: {'color': '#B05B10', 'name': 'Vineyards'},
        82: {'color': '#239800', 'name': 'Broadleaf tree cover'},
        83: {'color': '#086200', 'name': 'Coniferious tree cover'},
        102: {'color': '#F99627', 'name': 'Herbaceous vegetation'},
        103: {'color': '#8D8B00', 'name': 'Moors and heathland'},
        104: {'color': '#5F3506', 'name': 'Sclerophyllous vegetation'},
        105: {'color': '#956BC4', 'name': 'Marshes'},
        106: {'color': '#4D256A', 'name': 'Peatbogs'},
        121: {'color': '#9A9A9A', 'name': 'Natural material surfaces'},
        123: {'color': '#6AFFFF', 'name': 'Permanent snow covered surfaces'},
        162: {'color': '#1445F9', 'name': 'Water bodies'},
        255: {'color': '#FFFFFF', 'name': 'No data'}
        }
    }

lcz_settings = {
    'file': lcz_path,
    'source_text': 'WUDAPT European LCZ map (https://www.wudapt.org/lcz-maps/)',
    'data_band': 1,
    'classes': {
        0: {'color': '#646bf9', 'name': 'LCZ-G, water'}, #because seasurfaces are 0.
        1: {'color': '#690406', 'name': 'LCZ-1, compact highrise'},
        2: {'color': '#ce0100', 'name': 'LCZ-2, compact midrise'},
        3: {'color': '#fa0100', 'name': 'LCZ-3, compact lowrise'},
        4: {'color': '#ad5c01', 'name': 'LCZ-4, open highrise'},
        5: {'color': '#fd7207', 'name': 'LCZ-5, open midrise'},
        6: {'color': '#fe9953', 'name': 'LCZ-6, open lowrise'},
        7: {'color': '#f4ef01', 'name': 'LCZ-7, lightweight lowrise'},
        8: {'color': '#bcb9b6', 'name': 'LCZ-8, large lowrise'},
        9: {'color': '#f9cfad', 'name': 'LCZ-9, sparsely built'},
        10: {'color': '#545454', 'name': 'LCZ-10, heavy industry'},
        11: {'color': '#026804', 'name': 'LCZ-A, dense trees'},
        12: {'color': '#00aa00', 'name': 'LCZ-B, scattered trees'},
        13: {'color': '#618526', 'name': 'LCZ-C, bush, scrub'},
        14: {'color': '#b6d978', 'name': 'LCZ-D, low plants'},
        15: {'color': '#000000', 'name': 'LCZ-E, bare rock or paved'},
        16: {'color': '#fbf7ae', 'name': 'LCZ-F, bare soil or sand'},
        17: {'color': '#646bf9', 'name': 'LCZ-G, water'},
        }
    }


DEM_settings = {
    'folder': dem_dir_path,
    'source_text': 'European Digital Elevation Model (EU-DEM), V1.1 (https://land.copernicus.eu/imagery-in-situ/eu-dem)',
    'data_band': 1,
    'no_suitable_map_found': {'file_text': 'Not contained by current available maps.',
                              'value': None}
    
    
    
    }


