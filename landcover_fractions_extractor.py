#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 10:25:58 2022

@author: thoverga
"""


import sys 
import os
import rasterio
import pandas as pd
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from copy import copy

import geoplot as gplt
import geoplot.crs as gcrs
import geopandas as gpd


import matplotlib.ticker as mtick

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import gis_functions
import geo_maps_config

#%% open raster

#s2glc dataset
raster_info = geo_maps_config.s2glc_settings
src = rasterio.open(raster_info['file'])
raster_crs = str(src.crs) #coordinate system of raster

#lcz dataset
lcz_info = geo_maps_config.lcz_settings
src_lcz = rasterio.open(lcz_info['file'])
lcz_crs = str(src_lcz.crs)
# gis_functions.geo_map_info(src)

#%% settings
coordinate_dict = {'station1': [51.1226, 4.3665],
                    'VonRoll PH': [46.9529, 7.4225],
                    # 'Europaplatz': [46.9433, 7.4063],
                    # 'Uettligen Umland': [46.9804, 7.3873],
                    # 'Novi Sad - Limanski Park': [45.239286, 19.841227]
                    }



#%% LCZ testing
lat = 51.1226
lon = 4.3665




test = extract_LCZ_from_coordinates(lat=lat,
                                    lon=lon,
                                    lcz_map_band=lcz_info['data_band'],
                                    lcz_map_location=lcz_info['file'],
                                    class_to_human_mapper=lcz_info['classes'])

#%% Use csv as input
# filename = '/home/thoverga/Downloads/all_stations_ZUE_BAS_ZHAW.csv'

# df = pd.read_csv(filename)


# coordinate_dict = {}
# for idx, row in df.iterrows():
#     coordinate_dict[row['name']] = [row['lat'], row['lon']]


#%%output

outputfolder = '/home/thoverga/Desktop/lc_figs_v2_run'


#%%

buffer_list = [500, 250, 100, 50, 20]

#%% make barplot

def make_stacked_barplot(ax, lc_counts, raster_info):

   
    
    
    
    counts_df = pd.DataFrame()
    counts_df['classes'] = raster_info['classes'].keys()
    
    #find all available classes
    max_radius = max(lc_counts.keys())
    available_classes = list(np.unique(lc_counts[max_radius]))
    
    for buffer in lc_counts:
        counts = pd.Series(lc_counts[buffer]).value_counts()
        tot_counts = sum(counts)
        counts = (counts/tot_counts) * 100.0
        
        counts.name = str(buffer) + 'm'
        counts_df = counts_df.merge(counts.to_frame(), how='left', left_on='classes', right_index=True)
        
    
    counts_df = counts_df.fillna(0)
    
    counts_df['labels'] = counts_df['classes'].map(geo_maps_config.get_name_map_dict(raster_info))
    
    
    counts_df = counts_df[counts_df['classes'].isin(available_classes)]
    colors = counts_df['classes'].map(geo_maps_config.get_color_map_dict(raster_info)).to_list()
    
    
    
    counts_df = counts_df.drop('classes', axis='columns')
    
    
    counts_df = counts_df.set_index('labels')
    counts_df = counts_df.transpose()
    
    counts_df.plot.bar(stacked=True, color=colors, ax=ax)
    
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    
    ax.get_legend().remove()

    
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 + box.height * 0.1,
    #                  box.width, box.height * 0.9])
    
    # # Put a legend below current axis
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
    #           fancybox=True, shadow=True, ncol=3)
    
    plt.xticks(rotation=0)
    return ax, counts_df




#%%


def extract_non_masked_values_from_masked_array(masked_array):
     
     
     one_dimensional_data = masked_array.flatten()
     return one_dimensional_data[one_dimensional_data.mask == False].data

def plot_spatial_map_of_crop_and_buffer(max_raster_array, src_map, map_info,  buffer_radius_list, ax):
   

    
    #make color mapper
    classes = map_info['classes']
    lowest_boundary = min(classes.keys())-0.5
    listed_colors = []
    listed_boundaries = [lowest_boundary]
    for class_int in classes:
        listed_boundaries.append(class_int + 0.5)
        listed_colors.append(classes[class_int]['color'])    
    
    
    cmap = ListedColormap(listed_colors)
    norm = BoundaryNorm(listed_boundaries, cmap.N, clip=True)
    
    



    # ax.set_title(title)
    ax.imshow(max_raster_array, cmap=cmap, norm=norm)
    ax.set_aspect('equal')
    
    
    
    #add circles
    circle_list = []
    for radius in buffer_radius_list:
        radius_in_array_space = radius/src_map.transform[0]
        
        circle_center_x = (max_raster_array.shape[0]/2)-1.0
        circle_center_y = (max_raster_array.shape[1]/2)-1.0
        
        circle = plt.Circle((circle_center_x, circle_center_y), radius_in_array_space, color='black', fill=False)
        circle_list.append(circle)
        
        text_deviation = 0.5
        text = str(radius) + 'm'
        ax.text(circle_center_x, (circle_center_y + radius_in_array_space + text_deviation), text, style='italic')

    #add circles to ax
    for c in circle_list:
        new_c=copy(c)
        ax.add_patch(new_c)    



    #make legend
   

    present_classes = extract_non_masked_values_from_masked_array(max_raster_array)

    unique_classes = list(np.unique(present_classes))
    unique_classes.sort()

    legend_colors = [geo_maps_config.get_color_map_dict(map_info)[clas] for clas in unique_classes]
    legend_labels = [geo_maps_config.get_name_map_dict(map_info)[clas] for clas in unique_classes]

    legend_list = list(zip(legend_colors, legend_labels))
    legend_elements = []
    for item in legend_list:
        legend_elements.append(Line2D([0], [0], color=item[0], lw=4, label=item[1]))
    
    
    
    
    
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    
    # Put a legend below current axis
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=3, prop={'size': 13})
    

    #styling
    ax.axis('off')
    
    return ax







#%%

def make_basemap_plot(basemap_radius, radius_list, lat_station, lon_station, raster_crs, ax):

    

    df = pd.DataFrame({'lat':[lat_station], 'lon':[lon_station]})
    gdf = gis_functions.df_to_geodf(df, raster_crs, 'lat', 'lon')
    
    #save station location
    gdf['center_point'] = gdf['geometry']
    

    
    #Get extend
    gdf['basemap_radius'] = gdf['geometry'].buffer(float(basemap_radius), resolution=30)
    latlon_extent = gdf['basemap_radius'].to_crs(4326).total_bounds
    

    #to webmercator
    webmercator_epsg = 3857
    gdf = gdf.to_crs(webmercator_epsg)
    
    
    
    #create basemap
    gplt.webmap(df = gdf,extent=latlon_extent, projection=gcrs.WebMercator(), zoom = 17, ax=ax)
    
    #add station point
    gdf['center_point'].to_crs(webmercator_epsg).plot(ax=ax, color='red')
    
    #draw buffer circles
    for radius in radius_list:
        gdf['buffer_polygon'] = gdf['center_point'].buffer(float(radius), resolution=30)
        gdf['buffer_polygon'].to_crs(webmercator_epsg).plot(ax=ax, facecolor='none', edgecolor='black')

    return ax




def combine_plots_of_station(station_lat, station_lon, raster_crs, radius_list, basemap_radius, stationname, max_raster_array, map_info, raster, lc_counts):
    fig = plt.figure(figsize=(35,10))

    ax1 = plt.subplot(131, projection=gcrs.WebMercator())
    ax2 = plt.subplot(132)
    ax3 = plt.subplot(133)

    #basemap plot
    ax1 = make_basemap_plot(basemap_radius = 105, radius_list=radius_list, lat_station=lat, lon_station=lon, raster_crs=raster_crs, ax=ax1)

    #geo raster plot
    ax2 = plot_spatial_map_of_crop_and_buffer(max_raster_array=max_raster_array,
                                              src_map= raster,
                                              map_info = map_info,
                                              buffer_radius_list = radius_list,
                                              ax = ax2)
    
    #barplot
    ax3, counts_df = make_stacked_barplot(ax = ax3,
                               lc_counts=lc_counts,
                               raster_info=map_info)
    
    
    
    title = 'Landcover fractions for ' + stationname + ' (' + str(station_lat) + ', ' + str(station_lon) + ')' 
    
    plt.suptitle(title,fontsize=30)
    
    return counts_df
    # plt.show()



#%%


countsdict = {}

for station in coordinate_dict:
    lc_counts = {}
    
    lat=coordinate_dict[station][0]
    lon=coordinate_dict[station][1]
    for radius in np.sort(buffer_list):
        
        buffer = gis_functions.coordinate_to_circular_buffer_geometry(lat_center=lat,
                                                                      lon_center=lon, 
                                                                      radius_m = radius,
                                                                      crs=raster_crs)

    
        namedict = geo_maps_config.get_name_map_dict(raster_info)
        
        raster_array, affine = gis_functions.get_stats_and_crop_raster_to_region(raster_info, region=buffer, namedict=namedict)
        
        
        present_classes = extract_non_masked_values_from_masked_array(raster_array)
        # unique, counts = np.unique(present_classes, return_counts=True)
        lc_counts[radius] = present_classes
        
        
        
        
        if radius == max(buffer_list):
            counts_df = combine_plots_of_station(station_lat = lat,
                                     station_lon = lon,
                                     raster_crs = raster_crs,
                                     radius_list = buffer_list,
                                     basemap_radius = max(buffer_list) + 5.0,
                                     stationname=station,
                                     max_raster_array = raster_array,
                                     map_info= raster_info,
                                     raster = src,
                                     lc_counts=lc_counts)
    
    figname = station + '_lc_fractions_s2glc.png'
    file = os.path.join(outputfolder, figname)
    plt.savefig(file)
    plt.close()
    

    countsdict[station] = counts_df 
    
    
    
#%%
tot_counts = pd.DataFrame()
for station in countsdict:
    stationdf = countsdict[station]
    stationdf['name'] = station
    tot_counts = tot_counts.append(stationdf)


tot_counts.index.name = 'buffer_radius'
tot_counts = tot_counts.reset_index()

tot_counts = tot_counts.set_index('name')
tot_counts = tot_counts.fillna(0)

outputfile = 'LC_fractions_tabular.csv'
tot_counts.to_csv(os.path.join(outputfolder, outputfile))
