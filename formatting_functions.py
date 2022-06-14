#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:40:01 2022

@author: thoverga
"""

import pandas as pd

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





#%% Output format handling

def location_info_dict_to_dataframe(location_info, lc_class_to_human_mapper):
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
            print(location_info[location]['landcover'][buffer_radius])
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
