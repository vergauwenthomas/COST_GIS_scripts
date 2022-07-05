#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:40:01 2022

@author: thoverga
"""
import os
import json
import pandas as pd
import logging

logging.info("Loading module formatting_functions.py")

#%% Input format handling

def csv_file_to_location_info(csv_file, location_column_name='name', lat_column_name='lat', lon_column_name='lon'):
    #Basic checks
    from os.path import exists
    import sys

    if not exists(csv_file):
        sys.exit("File: ", csv_file, ' Not found! Abord')
    
    
    try: 
        locations_df = pd.read_csv(csv_file)
    except:
        sys.exit('could not read this file: '+ csv_file + ' Are you shure this is a .csv file? Abord')
    
    
    if not location_column_name in locations_df:
        sys.exit(location_column_name + ' not found in csv file (' +
                 str(list(locations_df.columns)) + ')! Abord')
    
    if not lat_column_name in locations_df:
        sys.exit(lat_column_name + ' not found in csv file (' +
                 str(list(locations_df.columns)) + ')! Abord')
    
    if not lon_column_name in locations_df:
        sys.exit(lon_column_name + ' not found in csv file (' +
                 str(list(locations_df.columns)) + ')! Abord')
    
    
    locations_df = locations_df.rename(columns={location_column_name: 'location',
                                                lat_column_name: 'lat',
                                                lon_column_name: 'lon'})
    
    locations_df[['lat', 'lon']] = locations_df[['lat', 'lon']].apply(pd.to_numeric, errors='coerce') 
    
    locations_df = locations_df.drop_duplicates(subset='location') #keep only unique location identifiers
    
    #to nested dictionary
    locations_dict = dict(zip(locations_df['location'], zip(locations_df['lat'], locations_df['lon'])))
    locations_dict = {key: {'lat': value[0], 'lon': value[1]} for key, value in locations_dict.items()}
    
    return locations_dict


def format_buffer_input_string(bufferstr):
    bufferlist = [float(buf) for buf in bufferstr.split(',')]
    bufferlist.sort(reverse=True)
    return bufferlist

def validate_input(location_info, outputfolder, bufferlist, north_arrow):
    
    # ------- validate location info -------- #
    #typecheck
    if not isinstance(location_info, dict):
        logging.warning('The location info is not a dictionary but %s', type(location_info))
    #unique locations check
    # if len(location_info) != len(set(location_info.values())):
    #     logging.warning('The coordinates for the locations are not unique! Probably a type in the input file... See: %s ', location_info)
    
    #-------- validate output folder ----------#
    #folder exist check
    if not os.path.exists(outputfolder):
        logging.warning('Outputfolder: %s does not exist!', outputfolder)
    if not os.path.isdir(outputfolder):
        logging.warning('Outputfolder: %s is not a folder!', outputfolder)
        
    #------- validate bufferlist --------#
    #typecheck
    if not isinstance(bufferlist, list):
        logging.warning('Bufferlist: %s , is not of type list but of type %s', bufferlist, type(bufferlist))
    if not (all([isinstance(buf, float) for buf in bufferlist])):
        logging.warning('Not all elements in the bufferlist are floats! %s --> %s', bufferlist, [type(buf) for buf in bufferlist])

    # ------ validate north_arrow --------

    if not os.path.exists(north_arrow):
        logging.warning('north_arrow figure: %s does not exist!', north_arrow)
    if not os.path.isfile(north_arrow):
        logging.warning('north_arrow: %s is not a file!', north_arrow)




#%% Output format handling

def location_info_dict_to_dataframe(location_info, lc_class_to_human_mapper):
    logging.info('Converting output to tabular form.')
    combined_df = pd.DataFrame()    
    for location in location_info:
        
        #init location dataframe
        location_df = pd.DataFrame()
        
        # get coordinates
        lat = location_info[location]['lat']
        lon = location_info[location]['lon']
        
        # get lcz
        lcz = location_info[location]['lcz']
        altitude = location_info[location]['height']['Altitude']
        
        #get landcoverfractions
        for buffer_radius in location_info[location]['landcover']:
            buffer_df = pd.DataFrame.from_dict(location_info[location]['landcover'][buffer_radius],
                                                 orient='index').transpose()
            buffer_df['buffer_radius'] = buffer_radius
            location_df = location_df.append(buffer_df)
            
        location_df['station'] = location
        location_df['lat'] = lat
        location_df['lon'] = lon
        location_df['LCZ'] = lcz
        location_df['altitude'] = altitude
        
        combined_df = combined_df.append(location_df)
        
    
    lc_column_order = [lc_class['name'] for _,lc_class in lc_class_to_human_mapper.items()]
    column_order = ['station', 'lat', 'lon', 'LCZ', 'altitude', 'buffer_radius']
    column_order.extend(lc_column_order)
            
    return combined_df[column_order]

def write_output_to_json(location_info, outputfolder):
    outputfile = os.path.join(outputfolder, 'json_data.json')
    logging.info("Exporting output to json file: %s", outputfile)
    with open(outputfile, "w") as outfile:
        json.dump(location_info, outfile)
