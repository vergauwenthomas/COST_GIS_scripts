#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 15:42:09 2021

Collection of GIS functions


@author: thoverga
"""
import rasterio
import rasterstats
import pandas as pd
import geopandas as gpd




#%% LCZ functions
def extract_LCZ_from_coordinates(lat, lon, lcz_map_location, class_to_human_mapper, lcz_map_band=1, interpolate='nearest'):
    
    #extract coordinatesystem from the rasterfile
    with rasterio.open(lcz_map_location) as src:    
        lcz_map_crs = str(src.crs) 
    
    #transform that lat-lon coordinates to the coordinatesystem of the rasterfile, and make geometry point object.
    point = coordinate_to_point_geometry(lat=lat,
                                         lon=lon,
                                         crs=lcz_map_crs)

    #extract raster value for the point object
    lcz_raster_value = rasterstats.point_query(vectors=point,
                                               raster=lcz_map_location,
                                               band=lcz_map_band,
                                               nodata=None,
                                               affine=None,
                                               interpolate=interpolate, #nearest or bilinear (beliniear --> no direct mapping to a class possible)
                                               geojson_out=False)
    lcz_class = class_to_human_mapper[lcz_raster_value[0]]['name']
    return lcz_class




#%% Geometry functions

def coordinate_to_point_geometry(lat, lon, crs):
    """ This function returns a shapely point object in the given coordinate referece frame. """
    
    point_geo = gpd.GeoDataFrame(pd.DataFrame(data={'lat': [lat], 'lon': [lon]}), geometry=gpd.points_from_xy([lon], [lat])) #to geopandas df
    point_geo = point_geo.set_crs(epsg = 4326) #inpunt are gps coordinates
    point_geo = point_geo.to_crs(crs) #coordinate transform
    
    return point_geo.iloc[0]['geometry']


def coordinate_to_circular_buffer_geometry(lat_center, lon_center, radius_m, crs):
    """ This function returns a shapely (circular) polygon object with a given radius in meter, in the given coordinate referece frame. """

    
    circ_geo = gpd.GeoDataFrame(pd.DataFrame(data={'lat': [lat_center], 'lon': [lon_center]}), geometry=gpd.points_from_xy([lon_center], [lat_center]))
    circ_geo = circ_geo.set_crs(epsg = 4326) #inpunt are gps coordinates
    circ_geo = circ_geo.to_crs(crs)
  
    circ_geo['polygon'] = circ_geo['geometry'].buffer(float(radius_m), resolution=30)
    
    return circ_geo.iloc[0]['polygon']

def df_to_geodf(df, crs, lat_identifier, lon_identifier):
    """ This function returns a geopandas dataframe with a geometry column in the given crs coordinates. """

    geo_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_identifier], df[lat_identifier]))
    geo_df = geo_df.set_crs(epsg = 4326) #inpunt are gps coordinates
    geo_df = geo_df.to_crs(crs)
    return geo_df
#%% raster extraction functions


def extract_non_masked_values_from_masked_array(masked_array):

     one_dimensional_data = masked_array.flatten() #To 1D
     return one_dimensional_data[one_dimensional_data.mask == False].data

def extract_landfractions_from_from_coordinate(lat, lon, buffer_radius, raster_map_location, class_to_human_mapper, raster_map_band=1):
    #extract coordinatesystem from the rasterfile
    with rasterio.open(raster_map_location) as src:    
        raster_map_crs = str(src.crs) 
    
    buffer = coordinate_to_circular_buffer_geometry(lat_center = lat,
                                                    lon_center = lon,
                                                    radius_m= buffer_radius,
                                                    crs=raster_map_crs)
    
    #make mapper to map raster classes to human classes
    namedict = {map_class: class_to_human_mapper[map_class]['name'] for map_class in class_to_human_mapper}
    
    #extract raster values in the buffer
    zs = rasterstats.zonal_stats(vectors = buffer,
                                  raster = raster_map_location,
                                  band_num=raster_map_band, 
                                  all_touched= True, #if true, inclueds the cells at the boundaries of the polygon
                                  categorical = True,
                                  category_map = namedict,
                                  raster_out= True,
                                  # prefix=str(layer)+'_'
                                  )
    cropped_raster_array = zs[0]['mini_raster_array']
   
   
    #convert to 1D array with unmasked values
    # present_classes = cropped_raster_array.flatten() #to 1D
    # present_classes = present_classes[present_classes.mask == False].data #extract unmasked values
    present_classes = extract_non_masked_values_from_masked_array(cropped_raster_array)
    #fractions counts
    freq_table = pd.Series(present_classes).value_counts()
    frac_table = (freq_table/sum(freq_table)).rename('fraction')
    
    #map raster classes to human
    frac_table.index = freq_table.index.to_series().map(namedict)
    
    #Init fraction dict with all possible classes
    frac_dict = {human_class: 0 for human_class in namedict.values()}
    
    #update frac_dict with calculated fractions
    frac_dict.update(frac_table.to_dict())
    

    return frac_dict


