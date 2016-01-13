#Code to merge all Lidar DTM layers into a single GeoTiff mosaiced raster
#Mainly copied from stackoverflow disscussion 
#"http://stackoverflow.com/questions/22109774/r-raster-mosaic-from-list-of-rasters"

# Preliminaries -----------------------------------------------------------
#packages
library(raster)

#function to make a list of actual raster from a list of raster file paths
ListRasters <- function(list_names) {
  raster_list <- list() # initialise the list of rasters
  for (i in 1:(length(list_names))){ 
    grd_name <- list_names[i] # list_names contains all the names of the images in .grd format
    raster_file <- raster(grd_name)
  }
  raster_list <- append(raster_list, raster_file) # update raster_list at each iteration
}

# Mosaic Generation ------------------------------------------------------
#setwd as the folder containing all of the DTM files or folders
setwd("D:\\Projects_new\\NE_wetlands\\Lidar_DTM_tiles\\")

#list all DTM files present, recursive= T to ensure sub folders are examined
dtm.list <- list.files(pattern=glob2rx("*.asc"), full.names=TRUE,recursive=TRUE)

#make a blank objects
list_names <- NULL

#not sure why this is used of list.files..?
for (i in 1:length(dtm.list)) {
  list_names <- c(list_names, dtm.list[i])
}

#convert every raster path to a raster object and create list of the results
raster.list <-sapply(list_names, FUN = ListRasters)

# edit settings of the raster list for use in do.call and mosaic
names(raster.list) <- NULL
raster.list$fun <- mean

#run do call to implement mosaic over the list of raster objects.
mos <- do.call(mosaic, raster.list)

#set crs as BNG
crs(mos) <- "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +datum=OSGB36 +units=m +no_defs "

#write the completed raster to file
writeRaster(mos,"lidar_2mDTM.tif",overwrite=TRUE)






