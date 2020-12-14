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






