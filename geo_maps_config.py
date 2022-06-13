#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Config file for the geospatial raster files.

@author: Thomas vergauwen
"""


#%% SET PATHS

#paths to the raster files (.tif)

s2glc_path = "/home/thoverga/Documents/github/maps/Landuse/S2GLC_EUROPE_2017/S2GLC_Europe_2017_v1.2.tif"
lcz_path = "/home/thoverga/Documents/github/maps/Landuse/EU_LCZ_map.tif"



#%% S2GLC_EUROPE_2017 Landcover map
s2glc_settings = {
    'file': s2glc_path,
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
    'data_band': 1,
    'classes': {
        0: {'color': '#0700C7', 'name': 'LCZ-G, water'}, #because seasurfaces are 0.
        1: {'color': '#141212', 'name': 'LCZ-1, compact highrise'},
        2: {'color': '#FF1100', 'name': 'LCZ-2, compact midrise'},
        3: {'color': '#E8A302', 'name': 'LCZ-3, compact lowrise'},
        4: {'color': '#6800FA', 'name': 'LCZ-4, open highrise'},
        5: {'color': '#A362FC', 'name': 'LCZ-5, open midrise'},
        6: {'color': '#CEABFF', 'name': 'LCZ-6, open lowrise'},
        7: {'color': '#0695C4', 'name': 'LCZ-7, lightweight lowrise'},
        8: {'color': '#56D3FC', 'name': 'LCZ-8, large lowrise'},
        9: {'color': '#FCF756', 'name': 'LCZ-9, sparsely built'},
        10: {'color': '#858481', 'name': 'LCZ-10, heavy industry'},
        11: {'color': '#005E1B', 'name': 'LCZ-A, dense trees'},
        12: {'color': '#02AB32', 'name': 'LCZ-B, scattered trees'},
        13: {'color': '#3BED4A', 'name': 'LCZ-C, bush, scrub'},
        14: {'color': '#C3EB57', 'name': 'LCZ-D, low plants'},
        15: {'color':'#855E03', 'name': 'LCZ-E, bare rock or paved'},
        16: {'color': '#F4A419', 'name': 'LCZ-F, bare soil or sand'},
        17: {'color': '#19D0E0', 'name': 'LCZ-G, water'},
        }
    }



# #%% predefined regions

# gent_region = {
#         'xmin': 3.6498,
#         'xmax': 3.828586,
#         'ymin': 51.0053,
#         'ymax': 51.111377
#         }

# belgium_region = {
#         'xmin': 2.521798,
#         'xmax': 6.433314,
#         'ymin': 49.475441,
#         'ymax': 51.516600
#     }

# countries = gpd.read_file(os.path.join(path_former.MAPS_DATA_PATH,'country_borders', 'WB_countries_Admin0_10m', 'WB_countries_Admin0_10m.shp'))
# belgium_exact = countries[countries['NAME_EN']=='Belgium']

# #%%

# belgium_provinces = gpd.read_file(os.path.join(path_former.MAPS_DATA_PATH,'country_borders', 'belgium', 'provinces_L08.shp'))


# #%%functions



# def rgb_to_hex(rgb_tuple):
#     """Return color as #rrggbb for the given color values."""
#     return '#%02x%02x%02x' % (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])



# def normalize_colors(settings):
#     dic = settings['classes']
#     for category in dic:
#         # dic[category]['color'] =  tuple([(float(x)/255.0) for x in dic[category]['color']])
#         dic[category]['color'] = rgb_to_hex(dic[category]['color'])
#     settings['classes'] = dic
#     return settings

# s2glc_settings = normalize_colors(s2glc_settings)
# lcz_settings = normalize_colors(lcz_settings)

# def get_color_map_dict(map_info):
#     return {value: map_info['classes'][value]['color'] for value in map_info['classes']}
# def get_color_map_dict_by_classname(map_info):
#     return {map_info['classes'][value]['name']: map_info['classes'][value]['color'] for value in map_info['classes']}
# def get_name_map_dict(map_info):
#     return {value: map_info['classes'][value]['name'] for value in map_info['classes']}
