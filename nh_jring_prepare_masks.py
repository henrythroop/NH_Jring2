#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:50:48 2017

@author: throop
"""

# General python imports

import pdb
import glob
import math       # We use this to get pi. Documentation says math is 'always available' 
                  # but apparently it still must be imported.
from   subprocess import call
import warnings
import pdb
import os.path
import os
import subprocess

import astropy
from   astropy.io import fits
from   astropy.table import Table
import astropy.table   # I need the unique() function here. Why is in in table and not Table??
import matplotlib
import matplotlib.pyplot as plt # pyplot
from   matplotlib.figure import Figure
import numpy as np
import astropy.modeling

import spiceypy as sp
#from   itertools import izip    # To loop over groups in a table -- see astropy tables docs
from   astropy.wcs import WCS
from   astroquery.vo_conesearch import conesearch
from   astropy import units as u           # Units library
from   astropy.coordinates import SkyCoord # To define coordinates to use in star search
#from   photutils import datasets
from   scipy.stats import mode
from   scipy.stats import linregress
from   astropy.visualization import wcsaxes
import time
from   scipy.interpolate import griddata
from   importlib import reload            # So I can do reload(module)

from skimage.io import imread, imsave

from astropy.convolution import Box1DKernel, Gaussian1DKernel, convolve

from   scipy.stats import linregress

import re # Regexp
import pickle # For load/save

from   matplotlib.figure import Figure

# HBT imports

import hbt

# =============================================================================
# This file does something very simple: takes a list of images (FITS), and write them out as PNGs.
# These PNGs can then be marked up in Photoshop, to make image masks which are used for removing stray light.
# In theory this program needs to be run once to create the files, and then never again.
# =============================================================================

# To make the masks in Photoshop:
#  Load the .png
#  Image -> 8 bits/channel
#  Add a layer on top of it (not a layer mask). Dial down opacity.
#  Paint it all white
#  Selectively paint black over the stray regions
#  Put back up the opacity.
#  Save as PNG
 
file_pickle = 'nh_jring_read_params_571.pkl' # Filename to read to get filenames, etc.
dir_out     = '/Users/throop/data/NH_Jring/out/' # Directory for saving of parameters, backplanes, etc.

dir_masks = dir_out.replace('out', 'masks')

lun = open(dir_out + file_pickle, 'rb')
t = pickle.load(lun)
lun.close()

# Process the group names. Some of this is duplicated logic -- depends on how we want to use it.

groups = astropy.table.unique(t, keys=(['Desc']))['Desc']

stretch_percent = 90    
stretch = astropy.visualization.PercentileInterval(stretch_percent) # PI(90) scales to 5th..95th %ile.

index_imagesets = [hbt.frange(0,7), # First set: take all images 7/0 .. 7/7. Sum them.
                   hbt.frange(8,15),
                   hbt.frange(16,23),
                   hbt.frange(24,31),
                   hbt.frange(32,35),
                   hbt.frange(36,39),
                   hbt.frange(40,42),
                   hbt.frange(52,57),
                   hbt.frange(61,63),
                   hbt.frange(91,93),
                   hbt.frange(94,96)
                   ]

index_imagesets = [hbt.frange(58,60)]
index_group = 7

index_imagesets = [hbt.frange(54,107)]
index_group = 8

index_imagesets = [hbt.frange(0,14)]
index_group = 5

plt.set_cmap('Greys_r')

power = 5

groupmask = t['Desc'] == groups[index_group]       
t_group = t[groupmask]  # 

for index_imagesets_i in index_imagesets:
    index_start = np.amin(index_imagesets_i)
    index_end = np.amax(index_imagesets_i)
    
    file_out = dir_masks + "mask_{}_{}-{}_image.png".format(index_group, 
                                 index_start, index_end)

    images = []
    
    for index_image in index_imagesets_i:
        t_image = t_group[index_image]  # Grab this, read-only, since we use it a lot.
        file_in = t_image['Filename']
        
        image = hbt.read_lorri(file_in, frac_clip = 1., bg_method = 'None')  # Read the image
    
        image = hbt.lorri_destripe(image)
        
        images.append(image)                                                 # Stuff this image onto the end of a list.
 
    images = np.array(images)                                     # Now we have a 3D Numpy array with all the image data
    images_sum = np.sum(images,axis=0)                                       # And sum down into a 2D array.
    
    images_proc = stretch(hbt.remove_sfit(images_sum, degree=power))
        
#    plt.imshow(images_sum)
#    plt.title("{}/{}-{} RAW".format(index_group, index_start, index_end))
#    plt.show()
    
    plt.imshow(images_proc)
    plt.title("{}/{}-{} - sfit({})".format(index_group, index_start, index_end, power))
    plt.show()
    
    imsave(file_out, images_proc)
#    
#    lun = open(file_out, 'wb')      # binary mode is important
#    w = png.Writer(1024, 1024, greyscale=True)
#    w.write(lun, 255*image_proc)
#    lun.close()
    print("Wrote: {}".format(file_out))


# =============================================================================
# Now read the masks back, and make some plots!
# This is for testing the subtraction algorithms.
# =============================================================================

for index_imagesets_i in index_imagesets:  # XX Need to rewrite the looping logic here.

    power = 5
    
    index_image = 1
    
    t_image = t_group[index_image]  # Grab this, read-only, since we use it a lot.
    file_in = t_image['Filename']
    
    file_mask = dir_masks + "mask_{}_{}.png".format(index_group, index_image)

    # Read the original image
    
    image =  hbt.read_lorri(file_in, frac_clip = 1., bg_method = 'None')
    
    # Read the mask (made in photoshop)
    
    mask = imread(file_mask)
    mask = (mask > np.mean(mask))  # Sometimes Photoshop mask is not quite binary... make it that way.
    
    print("Read: {}".format(file_mask))

    # Apply the mask to the image
    
    image_masked = image.copy()
    image_masked[mask == 0] = math.nan
    
    # Do an sfit to the masked image, and the original
    
    sfit_image_masked = hbt.sfit(image_masked,degree=power)
    sfit_image        = hbt.sfit(image,       degree=power)
    
    image_masked_proc = stretch(hbt.remove_sfit(image_masked, degree=power))
    image_proc =        stretch(hbt.remove_sfit(image,        degree=power))

    # Display them
    
    plt.imshow(stretch(image))
    plt.title('Original')
    plt.show()
    
    plt.imshow(stretch(hbt.remove_sfit(image, degree=power)))
    plt.title('Original - sfit')
    plt.show()
    
    plt.imshow(stretch(image_masked))
    plt.title('Masked')
    plt.show()
    
    plt.imshow(stretch(image_masked - sfit_image_masked))
    plt.title('Masked - sfit(masked)')
    plt.show()

    plt.imshow(stretch(image - sfit_image))
    plt.title('Original - sfit(orig)')
    plt.show()
    
    plt.imshow(stretch(image - sfit_image_masked))
    plt.title('Original - sfit(masked)')
    plt.show()
    