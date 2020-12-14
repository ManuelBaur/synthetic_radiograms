###########################################################################
####### Read particle positons.
####### Create artificial radiogram.
###########################################################################
import numpy as np
import os
import time

import module_fake_img_sim3D # contains functions to create fake images
#### start run time measurement
start_time = time.time()



############ Need parameters to read particle position files
##################################################################################################
### set parameters as used in simulation
nTime = 10000 # number of time steps
dt = 1.0 # step size of time step
dyN = 2 ## type of dynamics
nPart = 113445 ## corresponds to volumefraction of 0.4
speed = 2

################################
### Directories
dir_Sim = ('../../Sim_sedimentation/' +
	'4_dvx_dvy_not_eq_brownian_sedimentation_cv20_daytime_1559905433/') 

### create folder for fake-images and thickness map
dir_thicknessMap, dir_fake_img = \
	module_fake_img_sim3D.func_dir_out(dir_Sim, nPart, nTime, dyN, speed)	


### subfolder :: positions of particles	- (periodic boundary conditions)
dir_pos_data = (dir_Sim + 'positions_nPart_' + 
	str('{:0>8d}'.format(nPart)) +
	'_nTime' + str('{:0>4d}'.format(nTime)) + '/') 
	
time.sleep(60*60)
	
#################################################
### read simulation parameters
fSimName = dir_Sim + 'simulation_parameters.txt'
BoxDim = module_fake_img_sim3D.func_readSimParams(fSimName)

######## define size of images - must be adjusted if cone beam distortion is implemented
nPxImg = BoxDim[0] ## should be the same as BoxDim[1]
print nPxImg
##################################################################
#### DISTORTION PARAMETERS DUE TO CONE BEAM GEOMETRY CAN BE ADDED HERE
#### input size range of particle sizes - paricles of this range will be generated
diamPartRange = [19,19] # diameter of particles in Px (choose value as in experiments)


### add rim to image - cut off later to ensure particles appearing step by step in image
# nPxImg = int(nPxImg0 + (np.ceil(np.max(diamPartRange)/2.)) * 2.)
# import pdb;pdb.set_trace()
#### generate particle size distribution 
diamPart = module_fake_img_sim3D.diamPart_distribution(nPart,diamPartRange)


##########################################
### penetration length of x-ray beam in a sphere
### mask for all particle sizes, according to penetration length in sphere
maskPart = module_fake_img_sim3D.penLength(diamPart)




###################### loop over timesteps
for nt in (np.arange(nTime+1)):
###############################################################
	#### time processed
	if nt % 5 == 0:
		print ('working on timestep ' + str(nt) +
			' out of ' + str(nTime+1))
		elapsed_time = time.time() - start_time
		el_min, el_sec = divmod(elapsed_time, 60)
		el_hrs, el_min = divmod(el_min, 60) 
		print ('elapsed time: %d:%02d:%02d' % (el_hrs,el_min,el_sec))
	
	#########################################################
	#### read particle positions	
	nam_pos_data = ('particle_positions_nPart' +  str('{:0>8d}'.format(nPart)) + 
	'_timestep' + str('{:0>8d}'.format(nt)) + '.dat')
	
	pos_xyz = np.loadtxt((dir_pos_data + nam_pos_data))
	xPos = pos_xyz[:,0]
	yPos = pos_xyz[:,1]
	zPos = pos_xyz[:,2]
	
	#### round to integer values
	xPosPx = np.int32(np.round(xPos))
	yPosPx = np.int32(np.round(yPos))

	
	#### call module to create fake image (output range [0,1])
	fake_img = module_fake_img_sim3D.create_fake_img\
		(xPosPx,yPosPx,diamPart,maskPart,nPxImg,nt,dir_thicknessMap,dir_fake_img)
	        


###################################################################################################
##########  END OF PROGRAM 
total_time = time.time() - start_time
tot_min, tot_sec = divmod(total_time, 60)
tot_hrs, tot_min = divmod(tot_min,60)
print ('total time: %d:%02d:%02d' % (tot_hrs,tot_min,tot_sec))


