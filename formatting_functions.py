#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:40:01 2022

@author: thoverga
"""

import pandas as pd

#%% Input format handling







#%% Output format handling

def location_info_dict_to_csv(location_info, outputfile, lc_class_to_human_mapper):
    combined_df = pd.DataFrame()    
    for location in location_info:
        
        #init location dataframe
        location_df = pd.DataFrame()
        
        # get coordinates
        lat = location_info[location]['lat']
        lon = location_info[location]['lon']
        
        # get lcz
        lcz = location_info[location]['lcz']
        
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
        
        combined_df = combined_df.append(location_df)
        
    
    lc_column_order = [lc_class['name'] for _,lc_class in lc_class_to_human_mapper.items()]
    column_order = ['station', 'lat', 'lon', 'LCZ', 'buffer_radius']
    column_order.extend(lc_column_order)
            
    return combined_df[column_order]
