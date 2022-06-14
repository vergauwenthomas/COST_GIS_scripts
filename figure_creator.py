#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:40:26 2022

@author: thoverga
"""

import os
import gis_functions
from geo_maps_config import s2glc_settings, lcz_settings
import matplotlib.pyplot as plt
import geoplot as gplt
import geoplot.crs as gcrs
import pandas as pd
import geopandas as gpd
import rasterio

import cv2
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import geoplot as gplt
import geoplot.crs as gcrs
import pandas as pd
import geopandas as gpd
import rasterio
import rasterstats
from copy import copy
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D

import contextily as cx
    
from matplotlib_scalebar.scalebar import ScaleBar



parameters = {'axes.labelsize': 25,
              'xtick.labelsize': 15, 	
              'ytick.labelsize': 15,
              'figure.titlesize': 35,
              'legend.fontsize': 20,
              'axes.titlesize': 25}
plt.rcParams.update(parameters)


# def make_basemap_plot(basemap_radius, radius_list, lat_station, lon_station, ax, lc_map_location):
    
    
#     #extract coordinatesystem from the rasterfile so a buffer can be defined in meters
#     with rasterio.open(lc_map_location) as src:    
#         map_crs = str(src.crs)
    
#     #create a geopandas dataframe
#     df = pd.DataFrame({'lat':[lat_station], 'lon':[lon_station]})
#     gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))
#     gdf = gdf.set_crs(epsg = 4326) #inpunt are gps coordinates
#     gdf = gdf.to_crs(map_crs)

    
#     #save station location
#     gdf['center_point'] = gdf['geometry']
    

#     #Get extend
#     gdf['basemap_radius'] = gdf['geometry'].buffer(float(basemap_radius), resolution=30)
#     latlon_extent = gdf['basemap_radius'].to_crs(4326).total_bounds
    

#     #to webmercator
#     webmercator_epsg = 3857
#     gdf = gdf.to_crs(webmercator_epsg)
    
    
    
#     #create basemap
#     gplt.webmap(df = gdf,extent=latlon_extent, projection=gcrs.WebMercator(), zoom = 17, ax=ax)
    
#     #add station point
#     gdf['center_point'].to_crs(webmercator_epsg).plot(ax=ax, color='red')
    
#     #draw buffer circles
#     for radius in radius_list:
#         gdf['buffer_polygon'] = gdf['center_point'].buffer(float(radius), resolution=30)
#         gdf['buffer_polygon'].to_crs(webmercator_epsg).plot(ax=ax, facecolor='none', edgecolor='black')

#     return ax

def make_basemap_plot(basemap_radius, radius_list, lat_station, lon_station, ax, lc_map_location):
    
    
    #extract coordinatesystem from the rasterfile so a buffer can be defined in meters
    with rasterio.open(lc_map_location) as src:    
        map_crs = str(src.crs)
        # lc_map_resolution = src.transform[0]
    
    #init df
    df = pd.DataFrame()
    df['buffer_radius'] = radius_list
    df['lat'] = lat_station
    df['lon'] = lon_station
    
    #create a geopandas dataframe

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))
    gdf = gdf.set_crs(epsg = 4326) #inpunt are gps coordinates
    gdf = gdf.to_crs(map_crs)

    
    #save station location
    gdf['center_point'] = gdf['geometry']
    

    #to webmercator
    tile_provider = cx.providers.OpenStreetMap.Mapnik
    webmercator_epsg = 3857
    gdf = gdf.to_crs(webmercator_epsg)
    
    

    #add station point
    gdf = gdf.set_geometry('center_point')
    gdf = gdf.to_crs(webmercator_epsg)
    gdf['center_point'].plot(ax=ax, color='red')
    
    
    #draw buffer circles
    
    gdf['buffer_polygon'] = gdf['center_point'].buffer(gdf['buffer_radius'], resolution=30)
    gdf = gdf.set_geometry('buffer_polygon')
    gdf = gdf.to_crs(webmercator_epsg)
    gdf['buffer_polygon'].plot(ax=ax, facecolor='none', edgecolor='black')


    
    
    #text annotation location
    y_deviation = -10
    gdf['buffer_radius'] = gdf['buffer_radius'].astype(str)
    gdf['text_buffer_loc'] = gpd.points_from_xy(x=gdf['center_point'].x, y=gdf['buffer_polygon'].bounds['miny'])
    gdf = gdf.set_geometry('text_buffer_loc')
    gdf = gdf.to_crs(webmercator_epsg)
    gdf['text_x'], gdf['text_y']  = gdf['text_buffer_loc'].x, gdf['text_buffer_loc'].y + y_deviation
    
    for _idx, row in gdf.iterrows():
        ax.text(x=row['text_x'],
                    y=row['text_y'],
                    s=row['buffer_radius'] + 'm',
                    size=10,
                    va='center', 
                    ha='left', fontweight='bold')
    
    

    cx.add_basemap(ax, source=tile_provider, zoom=17)
    
    
    #add scalebar
    
    ax.add_artist(ScaleBar(1))
    
    #add source
    # ax.annotate(text='Based on OpenStreetMap (Mapnik)',
    #             xy=(0,1),
    #             xytext=(0, 20),
    #             xycoords='axes fraction',
    #             textcoords='offset points',
    #             va='top',
    #             size=10)
    
    
    #styling
    ax.axis('off')
    
    return ax




def plot_spatial_map_of_crop_and_buffer(raster_radius, lat, lon, map_info, ax,  buffer_radius_list=None, add_centerpoint=True, N_arrow_fig=None, add_N_arrow_and_scale=True):
   
    #extract coordinatesystem from the rasterfile
    with rasterio.open(map_info['file']) as src:    
        lc_map_crs = str(src.crs) 
        lc_map_resolution = src.transform[0]
    
    
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
    
    



    #crop raster 
    crop_to_buffer =  gis_functions.coordinate_to_circular_buffer_geometry(lat_center = lat,
                                                                          lon_center = lon,
                                                                          radius_m = raster_radius,
                                                                          crs = lc_map_crs)
    #make mapper to map raster classes to human classes
    namedict = {map_class: map_info['classes'][map_class]['name'] for map_class in map_info['classes']}
    zs = rasterstats.zonal_stats(vectors = crop_to_buffer,
                                  raster = map_info['file'],
                                  band_num=map_info['data_band'], 
                                  all_touched= True, #if true, inclueds the cells at the boundaries of the polygon
                                  categorical = True,
                                  category_map = namedict,
                                  raster_out= True,
                                  # prefix=str(layer)+'_'
                                  )
    cropped_raster_array = zs[0]['mini_raster_array']
    ax.imshow(cropped_raster_array, cmap=cmap, norm=norm)
    ax.set_aspect('equal')
    
    # return ax
    
    
    if not isinstance(buffer_radius_list, type(None)):
        #add circles
        circle_list = []
        for radius in buffer_radius_list:
            radius_in_array_space = radius/lc_map_resolution
            
            circle_center_x = (cropped_raster_array.shape[0]/2)
            circle_center_y = (cropped_raster_array.shape[1]/2)
        
            
            circle = plt.Circle((circle_center_x, circle_center_y), radius_in_array_space, color='black', fill=False)
            circle_list.append(circle)
            
            text_deviation = 0.5
            text = str(radius) + 'm'
            ax.text(circle_center_x, (circle_center_y + radius_in_array_space + text_deviation), text, fontweight='bold', size=10)
    
        #add circles to ax
        for c in circle_list:
            new_c=copy(c)
            ax.add_patch(new_c)    


    if add_centerpoint:
        grid_center = tuple(dim/2.0 for dim in cropped_raster_array.shape)
        circle1 = plt.Circle(grid_center, 0.2, color='r')
        ax.add_patch(circle1)
    #make legend
   

    present_classes = gis_functions.extract_non_masked_values_from_masked_array(cropped_raster_array)

    unique_classes = list(np.unique(present_classes))
    unique_classes.sort()


    legend_colors = [map_info['classes'][class_int]['color'] for class_int in unique_classes]
    legend_labels = [map_info['classes'][class_int]['name'] for class_int in unique_classes]
    
    
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
              fancybox=True, shadow=True, ncol=2, prop={'size': 13})
    
    
    
    

    if add_N_arrow_and_scale:
        
        #add north arrow
        arrow_arr_img = plt.imread(N_arrow_fig)
        arrow_RGB_img = cv2.cvtColor(arrow_arr_img, cv2.COLOR_BGR2RGB) #because matplotlib uses RGB format instead of BGR
        
        arrow_im = OffsetImage(arrow_RGB_img, zoom=.06)
        arrow_ab = AnnotationBbox(arrow_im, (1, 0.9), xycoords='axes fraction',frameon=False, box_alignment=(0.,-0.1))
    
        ax.add_artist(arrow_ab)
    
    
       
        # add scalebar
        scalebar = AnchoredSizeBar(transform=ax.transData,
                                size=250/lc_map_resolution,
                                label='250 m',
                                loc='upper right', 
                                pad=0.1,
                                color='black',
                                frameon=False,
                                size_vertical=10/lc_map_resolution)
        ax.add_artist(scalebar)    

    #add source
    # ax.annotate(text=map_info['source_text'],
    #             xy=(0,1),
    #             xytext=(0, 25),
    #             xycoords='axes fraction',
    #             textcoords='offset points',
    #             va='top',
    #             size=10)

    #styling
    ax.axis('off')
    
    return ax



def make_stacked_barplot(ax, location_data, map_info):

    #convert to dataframe
    counts_df = pd.DataFrame(location_data['landcover'])
    
    #sort from small buffers to large buffers
    bufferlist = list(counts_df.columns)
    bufferlist.sort() #from small to large
    counts_df = counts_df[bufferlist]    
    
    
    #convert columnst to strings and add 'm'
    counts_df.columns = [str(colname) + 'm' for colname in counts_df.columns]
    
    
    #create colors
    colormapper = {value['name']: value['color'] for _, value in map_info['classes'].items()}
    colors = counts_df.index.to_series().map(colormapper).to_list()
    
    #make plot
    counts_df.transpose().plot.bar(stacked=True, color=colors, ax=ax)
    
   
    
    #legend already in ax2 plot
    ax.get_legend().remove()
    
    # ax.annotate(text=map_info['source_text'],
    #             xy=(0,1),
    #             xytext=(0, 20),
    #             xycoords='axes fraction',
    #             textcoords='offset points',
    #             va='top',
    #             size=10)

    plt.xticks(rotation=0)
    return ax


#%% wrappers and combiners

def create_and_save_combined_figure(location, location_data, outputfolder, N_arrow_fig, source_list, basemap_overshoot_factor = 1.2):
    
    bufferlist = list(location_data['landcover'].keys())
    

    #create figure object
    fig = plt.figure(figsize=(35,10))
    ax1 = plt.subplot(141, projection=gcrs.WebMercator())
    ax2 = plt.subplot(142)
    ax3 = plt.subplot(143)
    ax4 = plt.subplot(144)
    # basemap plot
    
    
    ax1 = make_basemap_plot(basemap_radius = basemap_overshoot_factor * max(bufferlist),
                                            radius_list=bufferlist,
                                            lat_station=location_data['lat'],
                                            lon_station=location_data['lon'],
                                            ax=ax1,
                                            lc_map_location = s2glc_settings['file'])
    
    #geo raster plot
    ax2 = plot_spatial_map_of_crop_and_buffer(raster_radius = basemap_overshoot_factor * max(bufferlist),
                                              lat = location_data['lat'],
                                              lon = location_data['lon'],
                                              map_info = s2glc_settings,
                                              buffer_radius_list = bufferlist,
                                              ax = ax2,
                                              add_centerpoint=True,
                                              N_arrow_fig=N_arrow_fig,
                                              add_N_arrow_and_scale=True)
    
    
    # #barplot
    ax3 = make_stacked_barplot(ax = ax3,
                                          location_data=location_data,
                                          map_info=s2glc_settings)
    
    
    ax4 = plot_spatial_map_of_crop_and_buffer(raster_radius=basemap_overshoot_factor * max(bufferlist),
                                                            lat = location_data['lat'],
                                                            lon = location_data['lon'],
                                                            map_info=lcz_settings,
                                                            buffer_radius_list = bufferlist,
                                                            ax=ax4,
                                                            add_centerpoint=True,
                                                            N_arrow_fig=N_arrow_fig,
                                                            add_N_arrow_and_scale=True)
    ax4.title.set_text(location_data['lcz'])

    
    
    # create titles
    title = 'Landcover fractions for ' + location + ' (' + str(location_data['lat']) + 'N, ' + str(location_data['lon']) + 'E)'
    
    #add altitude to the figure if available
    altitude = location_data['height']['Altitude']
    if isinstance(altitude, float):
        title += ', altitude: ' + "{:.1f}".format(altitude) + 'm'
    
    
    plt.suptitle(title,fontsize=30)
    
    #add sources
    newline_space_y = 0.03
    indent_space_x = 0.02
    
    start_location_x = 0.75
    start_location_y = 0.10

    plt.figtext(x=start_location_x, y=start_location_y, s='Datasources:', fontsize=15)
    
    current_anchor_x = start_location_x + indent_space_x
    current_anchor_y = start_location_y
    for source_text in source_list:
        current_anchor_y = current_anchor_y - newline_space_y 
        plt.figtext(x=current_anchor_x,
                    y=current_anchor_y,
                    s=source_text,
                    url = 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figtext.html',
                    fontsize=13)
    
    #save figure
    
    figure_name = location + '_overview.svg'
    plt.savefig(os.path.join(outputfolder, figure_name))
    
    
    # plt.show()
    
    #close window and figure
    plt.clf()
    plt.close()
