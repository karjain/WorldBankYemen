import json
import geopandas as gpd
import pandas as pd



grid_file_list = ['/Users/kar/Documents/maps/tiles/R2C3/R2C3_grid.shp', '/Users/kar/Documents/maps/tiles/R2C4/grid_R2C4.shp','/Users/kar/Documents/maps/tiles/R3C3/R3C3_21m.shp',
                  '/Users/kar/Documents/maps/tiles/R3C4/Grid_R3C4_21m.shp','/Users/kar/Documents/maps/tiles/R4C3/grid_R4C3.shp','/Users/kar/Documents/maps/tiles/R4C4/grid_R4C4.shp' ]
prefix_list = ['R2C3','R2C4','R3C3','R3C4', 'R4C3','R4C4']


# Creating a dictionary of tile and corresponding grids. Used in next step to label grid if they are intersecting with roads 
with open(f'/Users/kar/Documents/maps/tiles/road_grids_mapping.json') as fp:
    parsed_json = json.load(fp)
grids_ = list(parsed_json.values())
grids_names = [element for sublist in grids_ for element in sublist]
tile_grid = {}

for i in grids_names:
    tile = i.split('_')[0]
    name = int(i.split('_')[1])
    if tile in tile_grid.keys():
        # print(f'grid = {i}, tile={tile}, name={name}')
        tile_grid[tile].extend([name])
    else:
        tile_grid[tile] = [name]


# labelling intersecting grids and appending the grid files with 2 new columns: global_id, intersect
for g,p in zip(grid_file_list, prefix_list):

    grid_df = gpd.read_file(g, crs = 'epsg:3857')
    grid_df = grid_df.to_crs('epsg:3857')
    grid_df['id'] = grid_df['id'].astype('int')

    for i in tile_grid[p]:
        # Set column `intersect` to 1 if intersecting grid intersects a road 
        grid_df.loc[grid_df['id'] == i,'intersect'] = 1 

    # Adding a new column global_id
    grid_df['global_id'] = p + '_' + grid_df['id'].astype('str')
    # print(grid_df)
    grid_df.to_file(f'/Users/kar/Documents/maps/tiles/intersecting_grids/{p}_intersecting_grids', driver='ESRI Shapefile')


