# %% #############################################################################################
### Imports ######################################################################################
##################################################################################################

import os
import rasterio
import rasterio.mask
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling
import fiona
import numpy as np
from matplotlib import pyplot

# %% ##############################################################################################
### Functions #####################################################################################
###################################################################################################

### Cropping Function ###

def crop_by_polygon(raster, outpath, polygon):
    with fiona.open(polygon, 'r') as shp:
        shapes = [feature['geometry'] for feature in shp]
        
    with rasterio.open(raster) as ras:
        out_image, out_transform = rasterio.mask.mask(ras, shapes, crop=True)
        out_meta = ras.meta
        out_meta.update({'driver': 'Gtiff',
                         'height': out_image.shape[1],
                         'width': out_image.shape[2],
                         'transform': out_transform})
        
        with rasterio.open(outpath, 'w', **out_meta) as dst:
            dst.write(out_image)

### Differencing Function ###

def difference_dems(raster_a, raster_b, write_out = True, outpath=None):
    ras_a = rasterio.open(raster_a)
    np_ras_a = ras_a.read(1, masked=True)
        
    ras_b = rasterio.open(raster_b)
    np_ras_b = ras_b.read(1, masked=True)
    
    # if ras_a has a higher resolution than ras_b
    if ras_a.res[0] <= ras_b.res[0]:
        print(os.path.basename(raster_a), ' has higher resolution.')
        profile = ras_a.profile
        # create blank array to reproject lower res raster
        dst_shape = (ras_a.height, ras_a.width)
        dst_ras = np.zeros(dst_shape, np.float32)

        reproject(
            source=np_ras_b,
            destination=dst_ras,
            src_transform=ras_b.transform,
            src_crs=ras_b.crs,
            dst_transform=ras_a.transform,
            dst_crs=ras_a.crs,
            resampling=Resampling.bilinear
        )

        diff_raster = np_ras_a - dst_ras
        
        # with fiona.open(polygon, 'r') as shp:
        #     shapes = [feature['geometry'] for feature in shp]
        
        # with rasterio.open(diff_raster) as ras:
        #     diff_raster = rasterio.mask.mask(ras, shapes, crop = True)
    
    # where ras_a has a lower resolution than ras_b
    else:
        print(os.path.basename(raster_b), ' has higher resolution.')
        profile = ras_b.profile
        dst_shape = (ras_b.height, ras_b.width)
        dst_ras = np.zeros(dst_shape, np.float32)

        reproject(
            source=np_ras_a,
            destination=dst_ras,
            src_transform=ras_a.transform,
            src_crs=ras_a.crs,
            dst_transform=ras_b.transform,
            dst_crs=ras_b.crs,
            resampling=Resampling.bilinear
        )
        
        diff_raster = dst_ras - np_ras_b
        
        # with fiona.open(polygon, 'r') as shp:
        #     shapes = [feature['geometry'] for feature in shp]
        
        # with rasterio.open(diff_raster) as ras:
        #     diff_raster = rasterio.mask.mask(ras, shapes, crop = True)
    
    if write_out == True:
        with rasterio.open(outpath, 'w', **profile) as out_raster:
            out_raster.write(diff_raster, 1)
    
    return diff_raster

# %% ##############################################################################################
### Paths #########################################################################################
###################################################################################################

### Input ###
lidar_dir = r'.\data\unprocessed_dems\lidar'
rgb_dir = r'.\data\unprocessed_dems\rgb'
### Clipped ###
out_rgb = r'.\outputs\processed_dems\rgb'
out_lidar = r'.\outputs\processed_dems\lidar'
### Differenced ###
rgb_diff_dir = os.path.join(os.getcwd(), 'outputs\\processed_dems\\rgb\\differenced')
lidar_diff_dir = os.path.join(os.getcwd(), 'outputs\\processed_dems\\lidar\\differenced')
### masks ###
shp = r'.\data\shp\Boolcoomatta_DeepGully_Boundary.shp'
shp_shallow = r'.\data\shp\Boolcoomatta_ShallowGully_Boundary.shp'

# %% ##############################################################################################
### Crop Files ####################################################################################
###################################################################################################

### LiDADR Deep ###
lidar_files_deep = [file for file in os.listdir(lidar_dir) if file.endswith('tif') if ('Deep' in file)]

for file in lidar_files_deep:
    in_file = os.path.join(lidar_dir, file)
    out_file = os.path.join(out_lidar, file[:-4] + '_clipped.tif')
    crop_by_polygon(in_file, out_file, shp)

### LiDAR Shallow ###
lidar_files_shallow = [file for file in os.listdir(lidar_dir) if file.endswith('.tif') if ('Shallow' in file)]

for file in lidar_files_shallow:
    in_file = os.path.join(lidar_dir, file)
    out_file = os.path.join(out_lidar, file[:-4] + '_clipped.tif')
    crop_by_polygon(in_file, out_file, shp_shallow)

### RGB Deep ###
RGB_files = [file for file in os.listdir(rgb_dir) if file.endswith('.tif')]

for file in RGB_files:
    in_file = os.path.join(rgb_dir, file)
    out_file = os.path.join(out_rgb, file[:-4] + '_clipped.tif')
    crop_by_polygon(in_file, out_file, shp)

### RGB Shallow ###

# RGB_shallow_files = [file for file in os.listdir(working_dir_shallow) if file.endswith('.tif')]

# for file in RGB_shallow_files:
#     in_file = os.path.join(working_dir_shallow, file)
#     out_file = os.path.join(out_dir, file[:-4] + '_clipped.tif')
#     crop_by_polygon(in_file, out_file, shp_shallow)

# %% ##############################################################################################
### Clipped file paths ############################################################################
###################################################################################################

### LiDAR ###
lidar_0316_deep = os.path.join(out_lidar, '20210316_Deep_LiDAR_DEM_clipped.tif')
lidar_0317_deep = os.path.join(out_lidar, '20210317_Deep_LiDAR_DEM_clipped.tif')

lidar_0316_shallow = os.path.join(out_lidar, '20210316_Shallow_LiDAR_DEM_clipped.tif')
lidar_0318_shallow = os.path.join(out_lidar, '20210318_Shallow_LiDAR_DEM_clipped.tif')

### Resolution comparisons ###
### Graeme trip 1 day 1 ###
rgb_0505_deep_35m = os.path.join(out_rgb, '20210505_Deep_RGB_2cm_DEM_clipped.tif')
rgb_0505_deep_70m = os.path.join(out_rgb, '20210505_Deep_RGB_4cm_DEM_clipped.tif')
rgb_0505_deep_110m = os.path.join(out_rgb, '20210505_Deep_RGB_6cm_DEM_clipped.tif')

### Graeme trip 1 day 2 ###
rgb_0506_deep_35m = os.path.join(out_rgb, '20210506_Deep_RGB_2cm_DEM_clipped.tif')
rgb_0506_deep_70m = os.path.join(out_rgb, '20210506_Deep_RGB_4cm_DEM_clipped.tif')
rgb_0506_deep_110m = os.path.join(out_rgb, '20210506_Deep_RGB_6cm_DEM_clipped.tif')

### Graeme trip 2 - only one date ###
rgb_0301_deep_35m = os.path.join(out_rgb, '20220301_Deep_RGB_2cm_DEM_clipped.tif')

### URAF trip ###
rgb_0316_deep_35m = os.path.join(out_rgb, '20210316_Deep_RGB_2cm_DEM_clipped.tif')
rgb_0317_deep_70m = os.path.join(out_rgb, '20210317_Deep_RGB_4cm_DEM_clipped.tif')
rgb_0317_deep_110m = os.path.join(out_rgb, '20210317_Deep_RGB_6cm_DEM_clipped.tif')

### URAF trip shallow ###
rgb_0316_shallow_35m = os.path.join(out_rgb, '20210316_Shallow_RGB_2cm_DEM_clipped.tif')
rgb_0318_shallow_70m = os.path.join(out_rgb, '20210318_Shallow_RGB_4cm_DEM_clipped.tif')
rgb_0318_shallow_110m = os.path.join(out_rgb, '20210318_Shallow_RGB_6cm_DEM_clipped.tif')

# %% ##############################################################################################
### Output paths ##################################################################################
###################################################################################################

rgb_0505_deep_35_70_out = os.path.join(rgb_diff_dir, '20210505_Deep_RGB_35_70_diff.tif')
rgb_0505_deep_35_110_out = os.path.join(rgb_diff_dir, '20210505_Deep_RGB_35_110_diff.tif')
rgb_0505_deep_70_110_out = os.path.join(rgb_diff_dir, '20210505_Deep_RGB_70_110_diff.tif')

rgb_0506_deep_35_70_out = os.path.join(rgb_diff_dir, '20210506_Deep_RGB_35_70_diff.tif')
rgb_0506_deep_35_110_out = os.path.join(rgb_diff_dir, '20210506_Deep_RGB_35_110_diff.tif')
rgb_0506_deep_70_110_out = os.path.join(rgb_diff_dir, '20210506_Deep_RGB_70_110_diff.tif')

rgb_0506_0505_deep_35_out = os.path.join(rgb_diff_dir, '20210506_20210505_Deep_RGB_35_diff.tif')
rgb_0506_0505_deep_70_out = os.path.join(rgb_diff_dir, '20210506_20210505_Deep_RGB_70_diff.tif')
rgb_0506_0505_deep_110_out = os.path.join(rgb_diff_dir, '20210506_20210505_Deep_RGB_110_diff.tif')

rgb_0301_0505_deep_35_out = os.path.join(rgb_diff_dir, '20220301_20210505_Deep_RGB_35_diff.tif')

rgb_URAF_deep_35_70_out = os.path.join(rgb_diff_dir, '202103_Deep_RGB_35_70_diff.tif')
rgb_URAF_deep_35_110_out = os.path.join(rgb_diff_dir, '202103_Deep_RGB_35_110_diff.tif')
rgb_URAF_deep_70_110_out = os.path.join(rgb_diff_dir, '202103_Deep_RGB_70_110_diff.tif')

rgb_URAF_shallow_35_70_out = os.path.join(rgb_diff_dir, '202103_Shallow_RGB_35_70_diff.tif')
rgb_URAF_shallow_35_110_out = os.path.join(rgb_diff_dir, '202103_Shallow_RGB_35_110_diff.tif')
rgb_URAF_shallow_70_110_out = os.path.join(rgb_diff_dir, '202103_Shallow_70_110_diff.tif')
# %% ##############################################################################################
### Difference RGB ################################################################################
###################################################################################################

rgb_0505_deep_35_70_diff = difference_dems(rgb_0505_deep_35m, rgb_0505_deep_70m, write_out=True, outpath = rgb_0505_deep_35_70_out)
rgb_0505_deep_35_110_diff = difference_dems(rgb_0505_deep_35m, rgb_0505_deep_110m, write_out=True, outpath = rgb_0505_deep_35_110_out)
rgb_0505_deep_70_110_diff = difference_dems(rgb_0505_deep_70m, rgb_0505_deep_110m, write_out=True, outpath = rgb_0505_deep_70_110_out)

rgb_0506_deep_35_70_diff = difference_dems(rgb_0506_deep_35m, rgb_0506_deep_70m, write_out=True, outpath = rgb_0506_deep_35_70_out)
rgb_0506_deep_35_110_diff = difference_dems(rgb_0506_deep_35m, rgb_0506_deep_110m, write_out=True, outpath = rgb_0506_deep_35_110_out)
rgb_0506_deep_70_110_diff = difference_dems(rgb_0506_deep_70m, rgb_0506_deep_110m, write_out=True, outpath = rgb_0506_deep_70_110_out)

rgb_0506_0505_deep_35_diff = difference_dems(rgb_0506_deep_35m, rgb_0505_deep_35m, write_out=True, outpath = rgb_0506_0505_deep_35_out)
rgb_0506_0505_deep_70_diff = difference_dems(rgb_0506_deep_70m, rgb_0505_deep_70m, write_out=True, outpath = rgb_0506_0505_deep_70_out)
rgb_0506_0505_deep_110_diff = difference_dems(rgb_0506_deep_110m, rgb_0505_deep_110m, write_out=True, outpath = rgb_0506_0505_deep_110_out)

rgb_0301_0505_deep_35_diff = difference_dems(rgb_0505_deep_35m, rgb_0301_deep_35m, write_out=True, outpath = rgb_0301_0505_deep_35_out)

rgb_URAF_deep_35_70_diff = difference_dems(rgb_0317_deep_70m, rgb_0316_deep_35m, write_out=True, outpath = rgb_URAF_deep_35_70_out)
rgb_URAF_deep_35_110_diff = difference_dems(rgb_0317_deep_110m, rgb_0316_deep_35m, write_out=True, outpath = rgb_URAF_deep_35_110_out)
rgb_URAF_deep_70_110_diff = difference_dems(rgb_0317_deep_110m, rgb_0317_deep_70m, write_out=True, outpath = rgb_URAF_deep_70_110_out)

# rgb_URAF_shallow_35_70_diff = difference_dems(rgb_0318_shallow_70m, rgb_0316_shallow_35m, write_out=True, outpath = rgb_URAF_shallow_35_70_out)
# rgb_URAF_shallow_35_110_diff = difference_dems(rgb_0318_shallow_110m, rgb_0316_shallow_35m, write_out=True, outpath = rgb_URAF_shallow_35_110_out)
# rgb_URAF_shallow_70_110_diff = difference_dems(rgb_0318_shallow_110m, rgb_0318_shallow_70m, write_out=True, outpath = rgb_URAF_shallow_70_110_out)


# %% ##############################################################################################
### Difference LiDAR ##############################################################################
###################################################################################################

lidar_0317_0316_deep_out = os.path.join(lidar_diff_dir, '20210317_20210316_Deep_LiDAR_diff.tif')
lidar_0317_0316_deep_diff = difference_dems(lidar_0317_deep, lidar_0316_deep, write_out=True, outpath=lidar_0317_0316_deep_out)

lidar_0318_0316_shallow_out = os.path.join(lidar_diff_dir, '20210318_20210316_Shallow_LiDAR_diff.tif')
lidar_0318_0316_shallow_diff = difference_dems(lidar_0318_shallow, lidar_0316_shallow, write_out=True, outpath=lidar_0318_0316_shallow_out)

# rgb_lidar_0316_deep_out = os.path.join(lidar_diff_dir, '20210316_Deep_LiDAR_RGB_4cm_diff.tif')
# rgb_lidar_0316_deep_diff = difference_dems(rgb_0316_deep_70m, lidar_0316_deep, write_out=True, outpath=rgb_lidar_0316_deep_out)

# rgb_lidar_0317_deep_out = os.path.join(lidar_diff_dir, '20210317_Deep_LiDAR_RGB_4cm_diff.tif')
# rgb_lidar_0317_deep_out = difference_dems(rgb_0316_deep_70m, lidar_0317_deep, write_out=True, outpath=rgb_lidar_0317_deep_out)