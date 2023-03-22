#%%
import rasterio
import geopandas as gpd
from rasterio import features
import matplotlib.pyplot as plt
import numpy as np
import array
#%%
raster = '/Users/kar/Documents/maps/merge_all.tif'
vector = '/Users/kar/Documents/maps/trainset_polygon_2m.shp'
df = gpd.read_file(vector)

with rasterio.open(raster, mode="r") as src:
            out_arr = src.read(1)
            out_profile = src.meta.copy()
            out_profile.update(count=1,
                            nodata=0,
                            dtype='int8',
                            width=src.width,
                            height=src.height,
                            compress='lzw',
                            crs=src.crs)
            dst_height = src.height
            dst_width = src.width
            shapes = ((geom,value) for geom, value in zip(df.geometry, df.Class))
            print(shapes)
            burned = features.rasterize(shapes=shapes, out_shape=(dst_height, dst_width),fill=0, transform=src.transform)
            plt.imshow(burned) 


# %%
file_name = '/Users/kar/Documents/maps/test.tiff'
with rasterio.Env():
    with rasterio.open(file_name, 'w', **out_profile) as dst:
        dst.write(1, burned)
    # %%
    with rasterio.open("test2.titf", 
                    mode="w", 
                    **out_profile,) as update_dataset:
        update_dataset.write(burned, 1)
# %%

with rasterio.Env():
    profile = src.profile
    profile.update(rasterio.uint8,
    count=1,
    compress='lzw')

    with rasterio.open ('test.tif', 'w', **profile) as dst:
        dst.write(burned.astype(rasterio.uint8), 1)
# %%
with rasterio.open('raster_Aoo.tif', 'w', **out_profile) as dst:
    dst.write(burned, 1)
# %%
with rasterio.open('raster_Aoo.tif', mode="r") as src:
            out_arr = src.read(1)






# %%
import fiona
def PolyTiles(input_shp, output_shp, prefix=None):
    ''''
    Function for extracting polygon tiles
    params: input_shp = shapefile or geojson, prefix is the prefix to save shape
    output: Shapefiles
    '''
    with fiona.open (input_shp) as dst_in:
        for index, feature in enumerate(dst_in):
            with fiona.open(f'{output_shp}/{prefix}_area{index}.shp', 'w', **dst_in.meta) as dst_out:
                dst_out.write(feature)
    return None
# filename = r'Users/kar/Documents/maps/test_grid1.shp'
filename = '/Users/kar/Documents/maps/test_grid1.shp'
output = r'/Users/kar/Documents/maps/gridstest'
PolyTiles(filename, output, prefix='test')
# %%
from glob import glob
import os
from subprocess import Popen
VRT = r'/Users/kar/Documents/maps/OrginalData/Aden_4_18_2022/Aden_4_18_2022_R3C3.tif'
outfile = '/Users/kar/Documents/maps/gridtest2'

# print(polygons)
polygons = sorted(glob(f'{output}/*.shp'))
print(polygons)
for polygon in polygons:
    # print(polygon)
    feat = fiona.open(polygon, 'r')
    # add output file name
    head, tail = os.path.split(polygon)
    name=tail[:-4]
    print(name)
    # command = f'gdalwarp -dstnodata -9999 -ts 215 215 -cutline {polygon} -crop_to_cutline -of Gtiff {VRT} "{outfile}/{name}.tif"'
    command = f'gdalwarp -dstnodata -9999 -cutline {polygon} -crop_to_cutline -of Gtiff {VRT} "{outfile}/{name}.tif"'

    Popen(command, shell=True)
# %%
