################################################################
#### 3D positions to fake radiogram
################################################################

#### Run Simon Weis code on test tomogram (Rev Sci Inst. 2017)
#### Project position data to 2D (x-y) plane
#### 

import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

import module_fake_img_sim

#### directory and name of position data
dir_in = '../../pattern_in_real_images/'
data_in = 'particles_centroids_ed4.dat'
dir_out = (dir_in + 'images/')

#### Particle diameter - plot g(r) to get better estimate!!!
diamPart = 27
nPxImg = 512
noise_fac = 2. * 10**(-1.)

#### read data
pos_xyz = np.loadtxt((dir_in + data_in))
xPos = pos_xyz[:,0]
yPos = pos_xyz[:,1]

#### round to integer values
xPosPx = np.int32(np.floor(xPos))
yPosPx = np.int32(np.floor(yPos))
##import pdb; pdb.set_trace()



###############################################################
#### call module to create fake image (output range [0,1]
fake_img_full = module_fake_img_sim.create_fake_img\
	(xPosPx,yPosPx,diamPart,nPxImg) # ,dir_thicknessMap)

#### creat noise matrix of size of 'fake_img_full' 
noise = module_fake_img_sim.create_gaussian_noise(fake_img_full.shape)
noise = (noise + 5.) / 10. # shift 5 sigmas to positive

fake_img_noise_full = fake_img_full - noise * noise_fac

##### save fake images as uint16 png (FULL)
cv2.imwrite(dir_out + 'tomogram_fake_img_full.png',
	np.uint16(fake_img_full*(2**16-1)))	
cv2.imwrite(dir_out + 'tomogram_fake_img_noise_full' + 
	str('{:0>4d}'.format(int(1000*noise_fac))) + '.png',
	np.uint16(fake_img_noise_full*(2**16-1)))	


### crop half a particle diameter from rim
##  otherwise half moon fake paritcle pops up once a particle moves close to image edge
# fake_img = fake_img_full\
# 	[np.int(np.floor(diamPart/2) + 1) : nPxImg-np.int(np.floor(diamPart/2) + 1),\
# 	np.int(np.floor(diamPart/2) + 1) : nPxImg-np.int(np.floor(diamPart/2) + 1)]
fake_img_crop = fake_img_full[127 : 383, 127 : 383]
fake_img_noise = fake_img_noise_full[127 : 383, 127 : 383]

##### save fake images as uint16 png (FULL)
cv2.imwrite(dir_out + 'tomogram_fake_img_crop.png',
	np.uint16(fake_img_crop*(2**16-1)))	

cv2.imwrite(dir_out + 'tomogram_fake_img_noise_' + 
	str('{:0>4d}'.format(int(1000*noise_fac))) + '_crop.png',
	np.uint16(fake_img_noise*(2**16-1)))	


	

