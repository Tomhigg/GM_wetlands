########### Python Script to Calculate Compound Topographic Index from a DEM

import arcpy
from arcpy import env  
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

#if multiple cores are available allow parallel processing, the % indicates the % of cores to use (e.g. 100% = all cores)
arcpy.env.parallelProcessingFactor = "75%" 

#set workspace where outputs will be stores, don't use H:/ drive as this will take a long time, use a local drive 
arcpy.env.workspace = r"F:\Projects\Manc_wetlands\funcTest" 
arcpy.env.scratchWorkspace = r"F:\Projects\Manc_wetlands\funcTest" 

#load DEM raster
dem = Raster("F:/Projects/Manc_wetlands/lidar_mosaic_2m/lidar_mosaictiff.tif")

#cell size in metres
cellsize = 2

# calculate flow direction
fd = FlowDirection(dem, "NORMAL")

#calculate flow accumulation using the flow direction layer
#if you are using a additional layer (e.g. soil or land cover) to weight accumulation result include it in the second input
fac = FlowAccumulation(fd,landcover_2m,"FLOAT")

#calculate slope into appropriate units
slope = Slope(dem, "DEGREE") * 1.570796 / 90
tan_slp = Con( slope > 0, Tan(slope), 0.001 )

# convert flow accumulation from number of cells to area
sca_scaled = ( fac + 1 ) * cellsize

#calculate cti 
cti = Ln(sca_scaled / tan_slp) 

#if results are very noisy use focal statistics to smooth outputs whilst keeping resolution the same
cti.focal = FocalStatistics(cti, "", "MEAN","DATA")
#or aggregate the cells to a coarser resolution
ctiCoarse = Aggregate(cti, 5, "MEAN", "TRUNCATE", "DATA")





