def CompTopoIndex (DEM, cellsize, weights,aggfactor):
	#calculate flow direction
	fd = FlowDirection(DEM, "NORMAL")
	#calculate flow accumulation using the flow direction layer
	#if you are using a additional layer (e.g. soil or land cover) to weight accumulation result include it in the second input
	if weights is None:
		fac = FlowAccumulation(fd,None,"FLOAT")
	else:
		fac = FlowAccumulation(fd,weights,"FLOAT")
	#calculate slope into appropriate units
	slope = Slope(DEM, "DEGREE") * 1.570796 / 90
	tan_slp = Con( slope > 0, Tan(slope), 0.001 )
	# convert flow accumulation from number of cells to area
	sca_scaled = ( fac + 1 ) * cellsize
	#calculate cti 
	cti = Ln(sca_scaled / tan_slp) 
	if aggfactor is None: 
		#savefile
		return (cti)
	else:
		#aggregate the cells to a coarser resolution
		ctiCoarse = Aggregate(cti, aggfactor, "MEAN", "TRUNCATE", "DATA")
		#save file
		return(ctiCoarse)