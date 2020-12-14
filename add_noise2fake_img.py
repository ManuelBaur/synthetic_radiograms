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
nPart = 1000 ## number of particles
dyN = 2 ## type of dynamics (1 = const speed, rand dirction, 2 = Max Boltz distr
partSpeedFac = 2 ## multiplication factor on mean speed of particles
noiseIn = 1 ## Noise added to artificial images (1 = no noise, 2 = random px noise as in experiments)
nTime = 2000 ## number of time steps, size of steps = 1

##### noise relative to signal strengt: e.g. noiseFac = 0.5 --> singal / noise = 2
# noiseFacArr = [1./10., 1./5., 1./2.] 
flickAmpl = 3.e-4 ## global flickering on top of mean of images
### 30000 part --> noiseFac = 0.01611, 1000 part --> noiseFac = 0.010
noiseFac = 0.01 # relation of noise to gray value of px - sets width of noise relative to gray value
widNoiseFac = 0.1 # noiseFac is fluctuating by this amount

############################### path position data of particles 
f_measIn = ('../../framed_start_center_runs_nPart_' + str('{:d}'.format(nPart)) +
	'_dynamics_' + str('{:d}'.format(dyN)) +
	'_speed_' + str('{:d}'.format(partSpeedFac)) +
	'_noiseLevel_' + str('{:d}'.format(noiseIn)) + '/')

f_imgIn = (f_measIn + 
	'fake_img_nPart_' + str('{:0>8d}'.format(nPart)) +
	'_nTime' + str('{:0>4d}'.format(nTime)) + '/')

# f_measIn = ('../../runs_nPart_' + str('{:d}'.format(nPart)) +
# 	'_dynamics_' + str('{:d}'.format(dyN)) +
# 	'_speed_' + str('{:d}'.format(partSpeedFac)) +
# 	'_noiseLevel_acc_gv_2/')
# 
# f_imgIn = (f_measIn + 
# 	'static_img_no_noise/')


####################################################
##### loop over different noise levels
f_measOut = ('../../framed_start_center_runs_nPart_' + str('{:d}'.format(nPart)) +
	'_dynamics_' + str('{:d}'.format(dyN)) +
	'_speed_' + str('{:d}'.format(partSpeedFac)) +
	'_noiseLevel_acc_gv_3/')

f_imgOut = (f_measOut + 
	'fake_img_nPart_' + str('{:0>8d}'.format(nPart)) +
	'_nTime' + str('{:0>4d}'.format(nTime)) + '/')
# f_imgOut = (f_measOut + 
# 	'static_img_noise_acc_gv_3/')


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
	# nam_img = ('static_' + str('{:0>3d}'.format(nt)) + '.png')
	### multiply by 0.9 - else adding noise gives gv > 2**16 -1
	img0 = np.float64(cv2.imread(f_imgIn + nam_img, -1)) * 0.9 
	mImg0 = np.mean(img0)
	stdImg0 = np.std(img0)
	# cv2.imwrite(f_imgOut + 'or_img_' + nam_img, np.uint16(img0))	

	#### add flickering of whole image 
	#### by std(mean of all img) / mean(mean of all img) = 3.e-4
	#### ratio : std/mean of single image does not change.
	globNoise = module_fake_img_sim.create_gaussian_noise([1,1])
	img0 = img0 * (1. - flickAmpl * globNoise) 
	# cv2.imwrite(f_imgOut + 'flicker_img_' + nam_img, np.uint16(img0))	
	

	#### create matrix with gaussian distribution of noise
	## std = 1, mean = 0	
	noise = module_fake_img_sim.create_gaussian_noise(img0.shape)
	
	# ## adjust noise relative to gray value according to noiseFac
	# noise_ad0 = noise * img0 * noiseFac
	# img_simple = img0 + noise_ad0
	# # cv2.imwrite(f_imgOut + 'Noise_acc_gv_simple_' + nam_img, np.uint16(img_simple))
	
	## adjust noise relative to gray value according to noiseFac
	## width of noise is vaying by widNoiseFac
	### THIS VERSION GIVES REASONABLE NOISE!
	widNoise = module_fake_img_sim.create_gaussian_noise(img0.shape) * widNoiseFac	
	
	noise_ad = noise * img0 * (noiseFac * (1. + widNoise))
			
	#### add subtract noise from image	
	img = img0 + noise_ad

	#### save noisy image
	cv2.imwrite(f_imgOut + nam_img, np.uint16(img))	
	

