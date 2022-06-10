#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:07:44 2022

@author: thoverga
"""

import os, sys

wdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wdir)

import geo_maps_config
import gis_functions
import formatting_functions
import figure_creator

#%% Settings

buffer_list = [500, 250, 100, 50, 20]


#%% IO

#The location info dict will be updated by the GIS functions
Location_info = {'station1': 
                     {'lat': 51.1226, 'lon': 4.3665},
                'VonRoll PH': 
                    {'lat': 46.9529, 'lon': 7.4225},
                    # 'Europaplatz': [46.9433, 7.4063],
                    # 'Uettligen Umland': [46.9804, 7.3873],
                    # 'Novi Sad - Limanski Park': [45.239286, 19.841227]
                }

#From CSV file
locations_file = "/home/thoverga/Downloads/all_stations_ZUE_BAS_ZHAW.csv"

# Location_info = formatting_functions.csv_file_to_location_info(csv_file=locations_file,
#                                                                location_column_name='name',
#                                                                lat_column_name='lat',
#                                                                lon_column_name='lon')


        


    

outputfolder = '/home/thoverga/Desktop/lc_figs_test_2'

#%% Check input settings

#TODO check if keys are unique


#%% LCZ extraction


for station in Location_info:

    lcz = gis_functions.extract_LCZ_from_coordinates(lat=Location_info[station]['lat'],
                                                     lon=Location_info[station]['lon'],
                                                     lcz_map_band=geo_maps_config.lcz_settings['data_band'],
                                                     lcz_map_location=geo_maps_config.lcz_settings['file'],
                                                     class_to_human_mapper=geo_maps_config.lcz_settings['classes'])
    
    #update location info
    Location_info[station]['lcz'] = lcz


#%% landcover extraction


for location in Location_info:
    Location_info[location]['landcover'] = {}
    for buffer_radius in buffer_list:        
        fractions = gis_functions.extract_landfractions_from_from_coordinate(lat=Location_info[location]['lat'],
                                                  lon=Location_info[location]['lon'],
                                                  buffer_radius=buffer_radius,
                                                  raster_map_location=geo_maps_config.s2glc_settings['file'],
                                                  class_to_human_mapper=geo_maps_config.s2glc_settings['classes'])
        
        #update location info
        Location_info[location]['landcover'][buffer_radius] = fractions


#%% save output
df = formatting_functions.location_info_dict_to_dataframe(location_info=Location_info,
                                                            lc_class_to_human_mapper = geo_maps_config.s2glc_settings['classes'])

df.to_csv(os.path.join(outputfolder, 'tabular_data.csv'), index=False)


#%% make figure
for location in Location_info:
    figure_creator.create_and_save_combined_figure(location=location,
                                                   location_data = Location_info[location],
                                                   outputfolder=outputfolder)
    
    

