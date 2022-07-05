#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:07:44 2022

In order to run this script, first run the set_env_var.sh script and than launch this (in the same terminal).


@author: thoverga
"""

import os, sys
import logging
logging.basicConfig(filename=os.environ.get("COST_LOG_FILE"),
                    level=logging.INFO)

wdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(wdir)

import geo_maps_config
import gis_functions
import formatting_functions
import figure_creator



#%% Elevation extractor
def main(Location_info, outputfolder, buffer_list, north_arrow):
    
    #extract bound for all DEM.tif files, so only the relevant will be opend later
    dem_bounds_gdf = gis_functions.generate_bounds_gdf_for_folder_of_tiffs(folder_path=geo_maps_config.DEM_settings['folder'],
                                                             output_crs='epsg:4326')
    
    for location in Location_info:
        logging.info('Extracting hight from DEM for station %s', location)
        height = gis_functions.extract_height_from_coordinates(location_data = Location_info[location],
                                                                                          map_bounds_geodf = dem_bounds_gdf,
                                                                                          dem_settings = geo_maps_config.DEM_settings)
        #update location info
        Location_info[location]['height'] = height
    
    
    # LCZ extraction
    for location in Location_info:
        logging.info('Extracting LCZ for station %s', location)
        lcz = gis_functions.extract_LCZ_from_coordinates(lat=Location_info[location]['lat'],
                                                         lon=Location_info[location]['lon'],
                                                         lcz_map_band=geo_maps_config.lcz_settings['data_band'],
                                                         lcz_map_location=geo_maps_config.lcz_settings['file'],
                                                         class_to_human_mapper=geo_maps_config.lcz_settings['classes'])
        
        #update location info
        Location_info[location]['lcz'] = lcz
    
    
    # landcover extraction
    for location in Location_info:
        logging.info('Extracting LCZ for station %s', location)
        Location_info[location]['landcover'] = {}
        for buffer_radius in buffer_list:        
            fractions = gis_functions.extract_landfractions_from_from_coordinate(lat=Location_info[location]['lat'],
                                                      lon=Location_info[location]['lon'],
                                                      buffer_radius=buffer_radius,
                                                      raster_map_location=geo_maps_config.s2glc_settings['file'],
                                                      class_to_human_mapper=geo_maps_config.s2glc_settings['classes'])
            
            #update location info
            Location_info[location]['landcover'][buffer_radius] = fractions
    
    
    # save output as tabular data
    formatting_functions.write_output_to_json(location_info=Location_info, outputfolder=outputfolder) #write output to JSON in the outputfolder
    
    #convert nested output dict to tabular form 
    df = formatting_functions.location_info_dict_to_dataframe(location_info=Location_info,
                                                                lc_class_to_human_mapper = geo_maps_config.s2glc_settings['classes'])
    
    logging.info("Writing tabular data to %s ", str(os.path.join(outputfolder, 'tabular_data.csv')))
    df.to_csv(os.path.join(outputfolder, 'tabular_data.csv'), index=False)
    
    
    # make figure
    for location in Location_info:
        logging.info("Creating figure for %s", location)
        figure_creator.create_and_save_combined_figure(location=location,
                                                        location_data = Location_info[location],
                                                        outputfolder=outputfolder,
                                                        N_arrow_fig=north_arrow,
                                                        source_list = ['OpenStreetMap Mapnik (https://mapnik.org/)',
                                                                      geo_maps_config.s2glc_settings['source_text'],
                                                                      geo_maps_config.lcz_settings['source_text'],
                                                                      geo_maps_config.DEM_settings['source_text']])
    

    logging.info('Done!!')


if __name__ == '__main__':
    
    
    bufferlist = formatting_functions.format_buffer_input_string(bufferstr = os.environ.get("COST_BUFFER_RADII"))
    outputfolder = os.environ.get('COST_OUTPUT_FOLDER')
    north_arrow = os.path.join(wdir, 'external_figures', 'North-Arrow.jpg')
    
    
    inputfile = os.environ.get("COST_INPUT_FILE")
    if inputfile[-4:] == ".csv":
        logging.info('Detection of %s as a csv file.', inputfile)
        Location_info = formatting_functions.csv_file_to_location_info(csv_file=inputfile,
                                                                        location_column_name=os.environ.get("COST_STATION_IDENTIFIER"),
                                                                        lat_column_name=os.environ.get("COST_LAT_IDENTIFIER"),
                                                                        lon_column_name=os.environ.get("COST_LON_IDENTIFIER"))
    elif inputfile[-5:] == '.json':
        logging.info('Detection of %s as a json file.', inputfile)
        import json
        with open(inputfile) as json_file:
            Location_info = json.load(json_file)
    else:
        logging.critical('Format of inputfile %s not recoginized, Abort', inputfile)
        sys.exit()
    
    formatting_functions.validate_input(Location_info, outputfolder, bufferlist, north_arrow)

    main(Location_info, outputfolder, bufferlist, north_arrow)
