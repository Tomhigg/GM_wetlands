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
		#concatenate output folder with resolution values
		outname = r"D:\Projects_new\NE_wetlands\Outputs\SpatialAggTests\cti_raw"+ str(res)
		#run aggregation
		outAggreg = Aggregate(cti, i, "MEAN", "TRUNCATE", "DATA")
		#save output
		outAggreg.save(outname)
		
#load and clip landcover data
extent = str(lidarDTM.extent)
LandcoverClip =  arcpy.Clip_management(in_raster="D:/Projects_new/NE_wetlands/Landcover/lcm-2007-25m_1201493/lcm2007_25m_gb.tif",
										rectangle="330000 380000 390000 430000",
										out_raster="D:/Temps/LandcoverClip",
										clipping_geometry="NONE",
										maintain_clipping_extent="NO_MAINTAIN_EXTENT")
LandcoverClip= Raster("D:/Temps/LandcoverClip")

#reclassify landcover into VH,M,L,VL drainage categories 
landcoverClass = Reclassify(Landcover, "VALUE", 
                         RemapValue([["0","NoData"],["1",3],["2",3],["3",2],["4",2],["5",2],["6",2],["8",2], ["9", 4], ["10",3],
						 ["11",3],["12", 4],["14", 1],["15",3],["16",3],["18",3],["19",3],["20",3],["21",4],["22",1],["23" ,1]]))

#resamples to match the 2m of the lidarDTM						 
landcover2m = arcpy.Resample_management(landcoverClass , "landcover2m.tif", "2")

#run CTI using landcover as a weighting variable 
CTI10mLC = CompTopoIndex(lidarDTM,lidarcell,landcover2m,lidarAgg)


