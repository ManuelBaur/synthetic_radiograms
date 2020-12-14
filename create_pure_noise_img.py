##############################################################################################
# Create images consisting of pure noise
# Aim : Check output of DDM 
#############################################################################################


import cv2
import numpy as np
import math
# from matplotlib import pyplot as plt
import os
import time

#### start run time measurement
start_time = time.time()


##################################################################################################
### set system parameters
nPxImg0 = 512 # number of pixel of fake image (image has square shape)
nTime = 2000 # number of time steps
dt = 1.0 # step size


#### folder of this run
dir_out = ('../../pure_noise_ImgWid' + 
	str('{:d}'.format(nPxImg0)) + 
	'_nTime_' + str('{:d}'.format(nTime)) + '/') 

try:
	os.stat(dir_out)
except:
	os.mkdir(dir_out)
	


for nt in range(nTime):
	#### time processed
	if nt % 20 == 0:
		print ('working on timestep ' + str(nt) +
			' out of ' + str(nTime+1))
		elapsed_time = time.time() - start_time
		el_min, el_sec = divmod(elapsed_time, 60)
		el_hrs, el_min = divmod(el_min, 60) 
		print ('elapsed time: %d:%02d:%02d' % (el_hrs,el_min,el_sec))

	### create matrix of random numbers
	img = np.random.rand(nPxImg0,nPxImg0) 	
	### transform to uint16 image
	img = (np.floor(img * (2.**16 - 1.))).astype(int)
	img = np.uint16(img)
	
	#### save as uint16 png	
	cv2.imwrite(dir_out + 
	'pure_noise_timestep' + str('{:0>4d}'.format(nt)) + '.png',img)
		
	
###################################################################################################
##########  END OF PROGRAM 
total_time = time.time() - start_time
tot_min, tot_sec = divmod(total_time, 60)
tot_hrs, tot_min = divmod(tot_min,60)
print ('total time: %d:%02d:%02d' % (tot_hrs,tot_min,tot_sec))


