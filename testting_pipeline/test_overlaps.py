# Testing phase
# For each road, find overlapping grids to be sent for prediction.
# Crete a mapping for raod and grid name. 
# After predition these grid names are used to average out the prediction for a road
# Basically creating a index of raod and corresponding grids

import geopandas as gpd
import pandas as pd
import json

# prefix = 'R4C4_'
output_dir = '/Users/kar/Documents/maps/tiles/'

# grid = gpd.read_file(r'/Users/kar/Documents/maps/tiles/R4C4/grid_R4C4.shp', crs = 'epsg:3857')

roads = gpd.read_file(r'/Users/kar/Documents/maps/tiles/road/filterted_road.shp', crs = 'epsg:3857')
roads = roads.to_crs('epsg:3857')


grid_file_list = ['/Users/kar/Documents/maps/tiles/R2C3/R2C3_grid.shp', '/Users/kar/Documents/maps/tiles/R2C4/grid_R2C4.shp','/Users/kar/Documents/maps/tiles/R3C3/R3C3_21m.shp',
                  '/Users/kar/Documents/maps/tiles/R3C4/Grid_R3C4_21m.shp','/Users/kar/Documents/maps/tiles/R4C3/grid_R4C3.shp','/Users/kar/Documents/maps/tiles/R4C4/grid_R4C4.shp' ]
prefix_list = ['R2C3','R2C4','R3C3','R3C4', 'R4C3','R4C4']


road_grids = {}
for g,p in zip(grid_file_list,prefix_list):
    print(f'Processing {p} with {g}')
    grid = gpd.read_file(g, crs = 'epsg:3857')
    grid['id'] = grid['id'].astype('int')
    grid = grid.to_crs('epsg:3857')
    
    grid['global_id'] = p + '_' + grid['id'].astype('str')


    for i in roads['full_id']:
        road_row = roads.loc[roads['full_id'] == i]
        grids_with_polygons = gpd.sjoin(left_df=road_row, right_df=grid, how='inner')
        temp_list = [x for x in grids_with_polygons['global_id'].values if x is not None]
        if temp_list:
            if i in road_grids:
                road_grids[i].extend(temp_list)
            else:
                road_grids[i] = temp_list
    print(f'len of road_grid ={len(road_grids)}')

with open(f'{output_dir}/road_grids_mapping.json', 'a') as fp:
    json.dump(road_grids,fp)


