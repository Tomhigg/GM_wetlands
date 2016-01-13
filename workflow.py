#load arcpy and spatial analyst extensions
import arcpy
from arcpy import env  
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

#set parallel processing 
arcpy.env.parallelProcessingFactor = "75%" 

#set temp directory
arcpy.env.workspace = r"D:\Temps" 
arcpy.env.scratchWorkspace = r"D:\Temps" 

#load dem and set initial parameters
lidarDTM = Raster("D:/Projects_new/NE_wetlands/Lidar_DTM_tiles/lidar_2mDTM.tif")
lidarcell = 2
lidarAgg = 5

#run 10m CTI 
CTI10m = CompTopoIndex (lidarDTM, lidarcell, "",lidarAgg)

#run CTUI with no aggregation 
cti = CompTopoIndex (lidarDTM, lidarcell, "","")

#for loop to test impact of changing aggregation factor
for i in range(6,25):
		#change i to output resolution for output name
		res= i*2
		#concatante output folder with resolution values
		outname = r"D:\Projects_new\NE_wetlands\Outputs\SpatialAggTests\cti_raw"+ str(res)
		#run aggregation
		outAggreg = Aggregate(cti, i, "MEAN", "TRUNCATE", "DATA")
		#save output
		outAggreg.save(outname)