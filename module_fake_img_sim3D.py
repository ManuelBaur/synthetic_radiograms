##########################################
## Modules for the fake image simulations
##########################################


import cv2
import numpy as np
import os
import scipy.io


#### create output folders
def func_dir_out(dir_Sim, nPart, nTime, dyN, partSpeedFac):
	
	### subfolder :: thickness Map 	
	dir_thicknessMap = (dir_Sim + 'thickness_Map_nPart' + 
		str('{:0>8d}'.format(nPart)) +
		'_nTime' + str('{:0>4}'.format(nTime)) + '/')
    
	try:
		os.stat(dir_thicknessMap)
	except:
		os.mkdir(dir_thicknessMap)
	
	### subfolder :: fake images 	
	dir_fake_img = (dir_Sim + 'fake_img_nPart_' + 
		str('{:0>8d}'.format(nPart)) +
		'_nTime' + str('{:0>4d}'.format(nTime)) + '/') 
	try:
		os.stat(dir_fake_img)
	except:
		os.mkdir(dir_fake_img)
	
	

	return dir_thicknessMap, dir_fake_img
		
#######################################################################
### Function to read parameters used in simulation
def load(fSimName):
	f = open(fSimName,'r')
	
	SimParams = []
	for line in f.readlines():
	    SimParams.append(line.replace('\n','').split(' '))
	
	f.close()

	return SimParams


def func_readSimParams(fSimName):
	SimParams = load(fSimName)
	### extract dimensions of simulation box
	strBoxDim = SimParams[0]
	BoxDim = np.int32(np.array(strBoxDim[1:]))

	return BoxDim



########################################################################
#### Function to generate distribution of particle sizes
def diamPart_distribution(nPart,diamPartRange):
	randDiam = np.random.rand(nPart)
	diamPart = diamPartRange[0] +\
		 randDiam * (diamPartRange[1] - diamPartRange[0])
	diamPart = np.uint16(np.floor(diamPart))
	
	return diamPart
	

#################################################
### Funktion to create fake image
def create_fake_img(xPosPx,yPosPx,diamPart,maskPart,nPxImg,nt,dir_thicknessMap,dir_fake_img):
	### min and max particle sizes
	minPart = np.min(diamPart)
	maxPart = np.max(diamPart)
	nPart = len(xPosPx)
	
	## framed fake image with mask full inside the image
	dFrame = np.int(np.ceil(maxPart/2.) * 2.) # 2 times frame thickness -- must be even
	dimF = nPxImg + dFrame # dimensions of framed image
	thicknessMapFramed = np.zeros([dimF,dimF])


	## upper left corner indices to anchor mask to
	# start_time = time.time()
	for nnPart in range(len(xPosPx)):
		### select mask for specific particle size
		PartSize = diamPart[nnPart]
		nMask = PartSize-minPart ## index of maskPart for this size
		mask = maskPart[:,:,nMask]
	
		### add up masks of particles
		thicknessMapFramed\
			[(yPosPx[nnPart]):(yPosPx[nnPart]+len(mask[:,0])),\
			(xPosPx[nnPart]):(xPosPx[nnPart]+len(mask[0,:]))] \
			= thicknessMapFramed [(yPosPx[nnPart]):(yPosPx[nnPart]+len(mask[:,0])),\
			(xPosPx[nnPart]):(xPosPx[nnPart]+len(mask[0,:]))] \
			+ mask
	
	# ######### time measurement filling particles	
	# total_time = time.time() - start_time
	# print ('filling of nPart: ' + str(len(xPosPx)) + \
	# 	' particles took ' + str(total_time) + ' seconds')

	## dont crop frame	
	# thicknessMap = thicknessMapFramed

	#### crop frame from thickness map
	thicknessMap = thicknessMapFramed\
		[dFrame-1:len(thicknessMapFramed[:,0])-dFrame-1,\
		dFrame-1:len(thicknessMapFramed[0,:])-dFrame-1]


	###############################################
	### call function to calculate x-ray attenuation of thickness map
	### thickness of spherical particles in beam direction
	fake_img = attenuation_BeerLambert(thicknessMap, maxPart)
	
	#### save images
	saveImg(thicknessMap,fake_img,dir_thicknessMap,dir_fake_img,nPart,nt)

	return fake_img

############################################
## Penetration length of x-ray beam in a spherical particle
## INPUT: 
## diamPart :: all particle diameters (size distribution)
## OUTPUT: 
## z_sphere :: maks of particle size, value according to pentration length
def penLength(diamPart):
	maxPart = np.max(diamPart)
	minPart = np.min(diamPart)
	
	### allocate arrays
	img_dist_px = np.zeros([maxPart, maxPart]) # distance on pixelgrid of circle
	z_sphere = np.zeros([maxPart, maxPart]) # thickness of sphere projected to 2D
	# to stack up mask types
	maskPart = np.zeros([maxPart, maxPart, maxPart-minPart+1]) # thickness of sphere projected to 2D

	### loop over particle sizes	
	for nSize in range(maxPart-minPart+1):
		PartSize = minPart + nSize 
		
		# print PartSize	
		# import pdb; pdb.set_trace()	

		## matrix of distances from center of mask 
		center = ([PartSize / 2. - 0.5, PartSize / 2. - 0.5])
		y, x = np.indices((PartSize,PartSize))	
		img_dist_px0 = np.sqrt((x - center[0])**2. + (y - center[1])**2.)

		anchor = np.int((maxPart - PartSize) / 2.) # upper left pixel position
		img_dist_px[anchor:anchor+PartSize, anchor:anchor+PartSize] = img_dist_px0
		
		Ones0 = np.ones([PartSize, PartSize])
		Ones1 = np.zeros([maxPart, maxPart])
		Ones1[anchor:anchor+PartSize, anchor:anchor+PartSize] = Ones0
		## calculate thickness of sphere along beam in distance from center 
		## z_min = 0, z_max = diameter
		z_sphere = (Ones1*PartSize/2.)**2 - img_dist_px**2 # square of the distance
		z_sphere = 2. * np.sqrt(z_sphere.clip(min=0)) # set negative values = 0, sqrt
		maskPart[:,:,nSize] = z_sphere

	return maskPart 


##########################################
### Function to create particle mask shaped according to x-ray attenuation.
## INPUT: 
## maxPart :: diameter of particles == size of the mask in (px)
## thicknessMap :: penetration length through particles in (px)
##
## OUTPUT:
## fake_img :: fake radiogram with attenuation of glass beads
def attenuation_BeerLambert(thicknessMap, maxPart):
	##### gauge attenuation an particle type to experiments
	# densitiy boro (glass g/cm^3), https://physics.nist.gov/PhysRefData/XrayMassCoef/tab2.html
	rho_glass = 2.23 
	partDiamCM = 0.0165 # 200. * 10.**(-4.) # paticle diameter in cm (200 mum)
	 	
	# PixelSize = 1.25 / 1495. # outer diameter cuvette = 1.25 cm = 1495 px
	thicknessCM = partDiamCM / maxPart * thicknessMap 	
	
	## mass-attenuation per density (mu/rho), for 60keV
	muRho = 0.2417 # https://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/pyrex.html
	
	## attenuation
	fake_img = np.exp(-muRho * rho_glass * thicknessCM) 
	
	## adjust to get good contrast
	fake_img = (fake_img - 0.2) * 2.
	

	return fake_img 


################################################
### save thicknessMap and fake_img and save as images and datafiles
def saveImg(thicknessMap,fake_img,dir_thicknessMap,dir_fake_img,nPart,nt):
	
	## thickness map - stretched to uint16 image	
	cv2.imwrite(dir_thicknessMap + 'thicknessMap_imgNr_nPart_' + \
		str('{:0>8d}'.format(nPart)) + \
		'_timestep' + str('{:0>8d}'.format(nt)) + '.png', 
		np.uint8(thicknessMap/np.amax(thicknessMap)*(2**8-1)))	
		# np.uint16(thicknessMap/np.amax(thicknessMap)*(2**16-1)))	
		

	## save pure data as .mat file
	scipy.io.savemat(dir_thicknessMap + 'thicknessMaps_imgNr_nPart_' + \
		str('{:0>8d}'.format(nPart)) + \
		'_timestep' + str('{:0>8d}'.format(nt)) + '.mat',\
		mdict={'out':thicknessMap},oned_as='row')


	##### save fake images as uint16 png (not stretched!)
	cv2.imwrite(dir_fake_img + 'fake_img_nPart' +
		str('{:0>8d}'.format(nPart)) +
		'_timestep' + str('{:0>8d}'.format(nt)) + '.png',
		np.uint8(fake_img*(2**8-1)))	
		# np.uint16(fake_img*(2**16-1)))	
		
		

################################################
#### save positions and velocities
def savePos_Vel(xPos,yPos, \
	xPosPx,yPosPx, \
	xPosCon,yPosCon, \
	xPosConPx,yPosConPx, \
	vx,vy,speed, \
	nt,nPart, \
	dir_pos_data,dir_posCon_data,dir_vel_data):

	#### save positions to data file (accurate)
	file_pos_out = (dir_pos_data + 'particle_positions_nPart' +
		str('{:0>8d}'.format(nPart)) +
		'_timestep' + str('{:0>8}'.format(nt)) + '.dat')
	
	np.savetxt(file_pos_out, np.transpose((xPos,yPos)), \
	fmt='%.10f', delimiter=' ', newline='\n')

	#### save positions to data file (rounded to pixel grid)
	file_posPx_out = (dir_pos_data + 'particle_positions_PxGrid_nPart' +
		str('{:0>8d}'.format(nPart)) +
		'_timestep' + str('{:0>8}'.format(nt)) + '.dat')
	
	np.savetxt(file_posPx_out, np.transpose((xPosPx,yPosPx)), \
	fmt='%d', delimiter=' ', newline='\n')


	#### save positions to data file (accurate) - periodic boundary conditions
	file_posCon_out = (dir_posCon_data + 'particle_positionsCon_nPart' +
		str('{:0>8d}'.format(nPart)) +
		'_timestep' + str('{:0>8d}'.format(nt)) + '.dat')
	
	np.savetxt(file_posCon_out, np.transpose((xPosCon,yPosCon)), \
	fmt='%.10f', delimiter=' ', newline='\n')

	#### save positions to data file (rounded to pixel grid)
	file_posCon_out = (dir_posCon_data + 'particle_positionsCon_PxGrid_nPart' +
		str('{:0>8d}'.format(nPart)) +
		'_timestep' + str('{:0>8d}'.format(nt)) + '.dat')
	
	np.savetxt(file_posCon_out, np.transpose((xPosConPx,yPosConPx)), \
	fmt='%d', delimiter=' ', newline='\n')




	#### save velocities to data file  time step == 1
	file_vel_out = (dir_vel_data + 'particle_velocities_nPart' +
		str('{:0>8d}'.format(nPart)) +
		'_timestep' + str('{:0>8}'.format(nt)) + '.dat')
	
	np.savetxt(file_vel_out, np.transpose((vx,vy,speed)), \
	fmt='%.10f', delimiter=' ', newline='\n')



############################################
#### Create noise of gaussian distribution
#### - used to add noise to fake images
### INPUT:
### dim :: dimensions of noise array
### 
### OUTPUT:
### noise :: array of dimensions dim, with gaussian noise
def create_gaussian_noise(dim):
	# arr = np.zeros((dim[0],dim[1]))
	arr1 = np.random.rand(dim[0],dim[1])
	arr2 = np.random.rand(dim[0],dim[1])
	noise = np.sqrt(-2. * np.log(arr1)) * np.cos(2. * np.pi * arr2)
	
	return noise




