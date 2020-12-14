######################################################
# Load fake images and add a certain noise level 
####################################################
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import os

import module_fake_img_sim

##########################################################
###### parameters of fake images
nPart = 30000 ## number of particles
dyN = 2 ## type of dynamics (1 = const speed, rand dirction, 2 = Max Boltz distr
partSpeedFac = 2 ## multiplication factor on mean speed of particles
noiseIn = 1 ## Noise added to artificial images (1 = no noise, 2 = random px noise as in experiments)
nTime = 2000 ## number of time steps, size of steps = 1

##### noise relative to signal strengt: e.g. noiseFac = 0.5 --> singal / noise = 2
noiseFacArr = [1./10., 1./5., 1./2.] 

############################### path position data of particles 
f_measIn = ('../../../ParameterScan1/runs_nPart_' + str('{:d}'.format(nPart)) +
	'_dynamics_' + str('{:d}'.format(dyN)) +
	'_speed_' + str('{:d}'.format(partSpeedFac)) +
	'_noiseLevel_' + str('{:d}'.format(noiseIn)) + '/')

f_imgIn = (f_measIn + 
	'fake_img_nPart_' + str('{:0>8d}'.format(nPart)) +
	'_nTime' + str('{:0>4d}'.format(nTime)) + '/')

####################################################
##### loop over different noise levels
for noiseFac in noiseFacArr: 
	noiseOut = int(1000 * noiseFac)

	f_measOut = ('../../runs_nPart_' + str('{:d}'.format(nPart)) +
		'_dynamics_' + str('{:d}'.format(dyN)) +
		'_speed_' + str('{:d}'.format(partSpeedFac)) +
		'_noiseLevel_' + str('{:d}'.format(noiseOut)) + '/')
	
	f_imgOut = (f_measOut + 
		'fake_img_nPart_' + str('{:0>8d}'.format(nPart)) +
		'_nTime' + str('{:0>4d}'.format(nTime)) + '/')
	
	try:
		os.stat(f_measOut)
	except: 
		os.mkdir(f_measOut)
	
	try:
		os.stat(f_imgOut)
	except: 
		os.mkdir(f_imgOut)
	
	
	######### loop over timesteps - different images
	for nt in (np.arange(nTime) + 1):
		##### read fake image without noise
		nam_img = ('fake_img_nPart' + str('{:0>8d}'.format(nPart)) +
			'_timestep' + str('{:0>4d}'.format(nt)) + '.png')
		img0 = cv2.imread(f_imgIn + nam_img, -1)
		mImg0 = np.mean(img0)
		stdImg0 = np.std(img0)
		
		#### create matrix with gaussian distribution of noise
		## std = 1, mean = 0	
		noise = module_fake_img_sim.create_gaussian_noise(img0.shape)
		noise = np.abs(noise + 5.) ## shift 5 sigmas to positive

		#### noise strength relative to signal strength (= std in image)
		noise = noiseFac*stdImg0 * noise

		#### add subtract noise from image	
		img = img0 - noise
	
		#### save noisy image
		cv2.imwrite(f_imgOut + nam_img, np.uint16(img))	
		
	
