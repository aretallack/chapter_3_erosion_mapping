This project contains code used for processing and producing figures from digital surface models created using both LiDAR and SfM.

1. Folders
 - src: contains source code, written in both R (.r/.qmd) and Python
 - data: contains original data that is used in r and python scripts
 - outputs: outputs of data processing (files from data folder modified by script)
 - figures: figure outputs for produced manuscript (produced from r .qmd files)

2. Languages
Code in the src folder is written in both R and Python.
R code is in the form of either .r files or quarto markdown files (.qmd)*

*install.packages("quarto") may need to be run if facing issues.

3. Scripts
R scripts are contained within src/r.

R is used for figure / table creation. Scripts are named based on the figure / table number that they produce in the manuscript. Some numbers are missing - these figures are maps, created in ArcGIS Pro.

A single Python script is contained within src/python

This python code is used to process the raw DSMs. Processing includes cropping to the erosion gully boundary, and differencing DSMs.

4. Code Order
Python code should be run first - as R code relies on its outputs to produce figures
Of the R code, balance_sampleZones.R should be run first. All other scripts ay be run in any order. 
 - functions.r contains longer functions that are used several times throughout the .qmd files

2.1 DATA STRUCTURE
For code to run, data should be placed within the data folder as below:

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