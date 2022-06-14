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

# #From CSV file
# locations_file = "/home/thoverga/Documents/github/COST_GIS_scripts/testcases/Novi_Sad_stations/station_data_NS.csv"

# Location_info = formatting_functions.csv_file_to_location_info(csv_file=locations_file,
#                                                                 location_column_name='station_name',
#                                                                 lat_column_name='station_lat',
#                                                                 lon_column_name='station_long')


        


    

outputfolder = '/home/thoverga/Documents/github/COST_GIS_scripts/testcases/Novi_Sad_stations/output'

#externalfigures
north_arrow = os.path.join(wdir, 'external_figures', 'North-Arrow.jpg')






#%% Check input settings

#TODO check if keys are unique

#%% Elevation extractor



dem_bounds_gdf = gis_functions.generate_bounds_gdf_for_folder_of_tiffs(folder_path=geo_maps_config.DEM_settings['folder'],
                                                         output_crs='epsg:4326')

for location in Location_info:
    location_data = Location_info[location]
    Location_info[location]['height'] = gis_functions.extract_height_from_coordinates(location_data = Location_info[location],
                                                                                      map_bounds_geodf = dem_bounds_gdf,
                                                                                      dem_settings = geo_maps_config.DEM_settings)
    



#%% LCZ extraction


for location in Location_info:
    
    lcz = gis_functions.extract_LCZ_from_coordinates(lat=Location_info[location]['lat'],
                                                     lon=Location_info[location]['lon'],
                                                     lcz_map_band=geo_maps_config.lcz_settings['data_band'],
                                                     lcz_map_location=geo_maps_config.lcz_settings['file'],
                                                     class_to_human_mapper=geo_maps_config.lcz_settings['classes'])
    
    #update location info
    Location_info[location]['lcz'] = lcz


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
                                                   outputfolder=outputfolder,
                                                   N_arrow_fig=north_arrow,
                                                   source_list = ['OpenStreetMap Mapnik (https://mapnik.org/)',
                                                                 geo_maps_config.s2glc_settings['source_text'],
                                                                 geo_maps_config.lcz_settings['source_text'],
                                                                 geo_maps_config.DEM_settings['source_text']])
    


