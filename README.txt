1. src

Code is written in both R and python, organised into r and python folders.

R code is use for figure / table creation, and quarto markdown files are labelled based on the figure / table number that they produce in the manuscript. 
Some numbers are missing - these figures are maps, created in ArcGIS Pro.


1.2. code order
Python code should be run first - this takes the raw DSMs and clips and differences. 
The clipped / differenced DSMs are the inputs to the R code which creates the figures.

Within the R code, the balance_sampleZones.R script goes first. All other .qmd files may be run in any order. 

1.3. functions.r

This script contains longer functions that are used several times throughout the other .qmd files. this file is sourced to load functions.


2. folders
Original data is contained in the data folder
Processed data from the python script, and balance_sampleZones.R are saved to the outputs folder
figures from the R code are saved in the figures folder. 

2.1 data folder
For code to run, data should be placed within the data folder as below:

E:/phd_chapters/chapter_4_erosion_mapping/data/

data
├── shp
│   ├── Boolcoomatta_DeepGully_Boundary.gpkg
│   ├── Boolcoomatta_ShallowGully_Boundary.gpkg
│   └── sample_zones.gpkg
└── unprocessed_dems
    ├── lidar
    │   ├── 20210316_Deep_LiDAR_DEM.tif
    │   ├── 20210316_Shallow_LiDAR_DEM.tif
    │   ├── 20210317_Deep_LiDAR_DEM.tif
    │   ├── 20210318_Shallow_LiDAR_DEM.tif
    └── rgb
        ├── 20210316_Deep_RGB_2cm_DEM.tif
        ├── 20210317_Deep_RGB_4cm_DEM.tif
        ├── 20210317_Deep_RGB_6cm_DEM.tif
        ├── 20210505_Deep_RGB_2cm_DEM.tif
        ├── 20210505_Deep_RGB_4cm_DEM.tif
        ├── 20210505_Deep_RGB_6cm_DEM.tif
        ├── 20210506_Deep_RGB_2cm_DEM.tif
        ├── 20210506_Deep_RGB_4cm_DEM.tif
        ├── 20210506_Deep_RGB_6cm_DEM.tif
        ├── 20220301_Deep_RGB_2cm_DEM.tif
        ├── 20220301_Deep_RGB_4cm_DEM.tif
        └── 20220301_Deep_RGB_6cm_DEM.tif