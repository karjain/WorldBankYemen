"""
Break the satellite image into grids 
Only consider grids that represent roads
Intersecting grids data comes from get_test_grid file
"""

import os
import fiona
from glob import glob
import os
from subprocess import Popen

grid_file_dir = '/Users/kar/Documents/maps/tiles/intersecting_grids'
# sat_img_list = ['/Users/kar/Documents/maps/tiles/R2C3/R2C3_img.tif','/Users/kar/Documents/maps/tiles/R2C4/Img_R2C4.tif','/Users/kar/Documents/maps/tiles/R3C3/test_02.tif',
#                 '/Users/kar/Documents/maps/tiles/R3C4/R3C4_img_02.tif','/Users/kar/Documents/maps/tiles/R4C3/Img_R4C3.tif','/Users/kar/Documents/maps/tiles/R4C4/Img_R4C4.tif']
# prefix_list = ['R2C3','R2C4','R3C3','R3C4', 'R4C3','R4C4']

sat_img_list = ['/Users/kar/Documents/maps/tiles/R2C4/Img_R2C4.tif']
prefix_list = ['R2C4']



def PolyTiles(input_shp, output_shp, quality,  prefix=None):
    ''''
    Function for extracting polygon tiles
    params: input_shp = shapefile or geojson, prefix is the prefix to save shape
    output: Shapefiles
    '''
    
    with fiona.open (input_shp) as dst_in:
        for index, feature in enumerate(dst_in):
            # print('inside')
            if feature['properties']['intersect'] == 1:
                # print(f'{output_shp}/{prefix}_area{index}.shp')
                with fiona.open(f'{output_shp}/{prefix}_{index}.shp', 'w', **dst_in.meta) as dst_out:
                    # print(feature)
                    dst_out.write(feature)
    return None
    

 
# for i in range(len(sat_img_list)):
#     os.makedirs(f'{grid_file_dir}/{prefix_list[i]}_intersecting_grids/{prefix_list[i]}_step1/', exist_ok=True)
#     PolyTiles(f'{grid_file_dir}/{prefix_list[i]}_intersecting_grids/{prefix_list[i]}_intersecting_grids.shp',
#                f'{grid_file_dir}/{prefix_list[i]}_intersecting_grids/{prefix_list[i]}_step1', i, prefix=prefix_list[i])



for i in range(len(sat_img_list)):
   
    outfile_step2 = f'{grid_file_dir}/{prefix_list[i]}_intersecting_grids/{prefix_list[i]}_step2'
    os.makedirs(outfile_step2, exist_ok=True)

    polygons = sorted(glob(f'{grid_file_dir}/{prefix_list[i]}_intersecting_grids/{prefix_list[i]}_step1/*.shp'))
    print(len(polygons))

    for polygon in polygons:
        feat = fiona.open(polygon, 'r')
        # add output file name
        base, name = os.path.split(polygon)
        name=name[:-4]
        # print(name)
        # command = f'gdalwarp -dstnodata -9999 -cutline {polygon} -crop_to_cutline -of Gtiff {sat_img_list[i]} "{outfile_step2}/{name}.tif"'

        # Popen(command, shell=True)
    print(f'Done cropping {prefix_list[i]}')    
    

