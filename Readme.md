Synthetic radiograms by Manuel Baur:
----------------------------------------------------------

As part of my doctoral studies, I have developed simple particle simulations.
(My PhD thesis is published here: https://opus4.kobv.de/opus4-fau/frontdoor/index/index/docId/14491)

The particle simulations were used to generate synthetic X-ray radiograms.
These X-ray radiograms were then used to study if an analysis technique,
which is analogous to Differential Dynamic Microscopy, 
is applicable to X-ray radiograms.

The code in this repository can be used to generate time series of synthetic X-ray radiograms.
Input are data files of the particle positions, 
which can be generated with the particle simulations 
(https://github.com/ManuelBaur/Particle_simulations.git),
which output the x-y-z position of the particles over time.

To generate the synthetic radiograms run:
main_artificial_radiogram.py

At every particle position from the position file a spherical particle is placed.
First output is a 'thickness map', i.e. the penetration length of an X-ray beam
in z-dirction through the particles. 
E.g. if two particles line up behind each other in z-direction the maximal length of the
beam through those two particles is twice the particle diameter.
Implemented is a monochromatic parallel X-ray beam in z-direction. 
In a second step the final gray value in the synthetic radiogram is calculated from the 
'thickness map' by applying Lambert-Beers law.
The images of the thickness map and the final synthetic radiograms are saved.
These steps are done for all time steps.




## These particle positions can then be used as input to generate synthetic X-ray radiograms. 
## 
## ##### main_sim3D.py 
## The script main_sim3D.py can be used to run the particle simulations.
## One can adjust the number and speed of the particles.
## Additionally one can choose different types of particle dynamics: 
## I.e. dircted motion and Brownian motion and compositions of both.
## At the current status NO particle-particle interactions are implemented.
## So the initial type of paricle dynamics (e.g. purely directed motion) 
## is not affected over the simulation time.
## 
## There are serveral more scripts in this repository:
## 
## #### analyze_velocity_distribution.py
## It calcualtes the mean and the std of the velocity distribution and
## plots the distributions.
## For directed motion this is a sharp delta peak, 
## for Brownian motion this is Gaussian distribution. 



